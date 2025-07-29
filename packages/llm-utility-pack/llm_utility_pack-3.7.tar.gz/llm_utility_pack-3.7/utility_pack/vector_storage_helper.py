from concurrent.futures import ThreadPoolExecutor, as_completed
import lmdb, struct, pickle, os, atexit, hashlib, io
import scipy.sparse as sp
import numpy as np

class LmdbStorage:
    def __init__(self, path, map_size=20*1024*1024*1024): # e.g. 20GB by default
        self.env = lmdb.open(path, map_size=map_size)
        atexit.register(self.close)

    def _int_to_bytes(self, x):
        """
        Converts an integer to 8-byte signed little-endian format.
        If x is outside the signed 64-bit range, wraps it safely.
        """
        MAX_UINT64 = 2**64
        MAX_INT64 = 2**63

        # Ensure x is within 0 to 2^64 - 1
        x = x % MAX_UINT64

        # Convert to signed range if necessary
        if x >= MAX_INT64:
            x -= MAX_UINT64

        return struct.pack('<q', x)

    def store_data(self, data, identifiers, batch_size=5000):
        total = len(data)
        with self.env.begin(write=True) as txn:
            for i in range(0, total, batch_size):
                batch_data = data[i:i+batch_size]
                batch_ids = identifiers[i:i+batch_size]
                with txn.cursor() as curs:
                    for vec, id in zip(batch_data, batch_ids):
                        curs.put(
                            self._int_to_bytes(id) if isinstance(id, int) else id.encode(),
                            pickle.dumps(vec)
                        )

    def get_data(self, identifiers):
        datas = []
        with self.env.begin() as txn:
            for id in identifiers:
                data = txn.get(self._int_to_bytes(id) if isinstance(id, int) else id.encode())
                if data:
                    datas.append(pickle.loads(data))
                else:
                    datas.append(None)
        return [ v for v in datas if v is not None ]
        
    def store_vectors(self, data, identifiers, batch_size=5000):
        total = len(data)
        with self.env.begin(write=True) as txn:
            for i in range(0, total, batch_size):
                batch_data = data[i:i+batch_size]
                batch_ids = identifiers[i:i+batch_size]
                with txn.cursor() as curs:
                    for vec, id in zip(batch_data, batch_ids):
                        curs.put(
                            self._int_to_bytes(id) if isinstance(id, int) else id.encode(),
                            np.array(vec, dtype=np.float32).tobytes()
                        )
    
    def store_sparse_vectors(self, data, identifiers):
        """
        Serializes and stores rows of a SciPy sparse matrix.

        :param data: A single scipy.sparse matrix.
        :param identifiers: A list of identifiers, one for each row in the data matrix.
        """
        if not sp.issparse(data):
            raise TypeError("Input data must be a SciPy sparse matrix.")
        
        # Use Compressed Sparse Row format for efficient row slicing
        csr_data = data.tocsr()
        num_rows = csr_data.shape[0]

        if num_rows != len(identifiers):
            raise ValueError("The number of rows in the sparse matrix must match the number of identifiers.")

        with self.env.begin(write=True) as txn:
            with txn.cursor() as curs:
                for i in range(num_rows):
                    # Slice one row, which results in a new (1, N) sparse matrix
                    row_slice = csr_data[i]
                    
                    # Serialize the single-row sparse matrix to bytes
                    buffer = io.BytesIO()
                    sp.save_npz(buffer, row_slice)
                    data_bytes = buffer.getvalue()
                    
                    # Store in LMDB
                    identifier = identifiers[i]
                    key = self._int_to_bytes(identifier) if isinstance(identifier, int) else identifier.encode()
                    curs.put(key, data_bytes)
    
    def get_vectors(self, identifiers):
        datas = []
        with self.env.begin() as txn:
            for id in identifiers:
                data = txn.get(self._int_to_bytes(id) if isinstance(id, int) else id.encode())
                if data:
                    datas.append(np.frombuffer(data, dtype=np.float32))
                else:
                    datas.append(None)
        return [v for v in datas if v is not None]
    
    def get_sparse_vectors(self, identifiers):
        """
        Retrieves sparse vectors, deserializes them, and stacks them into a single sparse matrix.

        :param identifiers: A list of identifiers to retrieve.
        :return: A scipy.sparse.csr_matrix containing the found vectors, or None if none are found.
        """
        retrieved_rows = []
        with self.env.begin() as txn:
            for id in identifiers:
                key = self._int_to_bytes(id) if isinstance(id, int) else id.encode()
                data_bytes = txn.get(key)
                if data_bytes:
                    buffer = io.BytesIO(data_bytes)
                    # Load the single-row sparse matrix
                    sparse_row = sp.load_npz(buffer)
                    retrieved_rows.append(sparse_row)
        
        # If we found any vectors, stack them into a single sparse matrix
        if retrieved_rows:
            return sp.vstack(retrieved_rows, format='csr')
        
        return None

    def delete_data(self, identifiers):
        with self.env.begin(write=True) as txn:
            for id in identifiers:
                txn.delete(self._int_to_bytes(id) if isinstance(id, int) else id.encode())

    def get_data_count(self):
        with self.env.begin() as txn:
            return txn.stat()['entries']

    def sync(self):
        self.env.sync()

    def close(self):
        self.env.close()

class ShardedLmdbStorage:
    """
    A sharded wrapper for LmdbStorage that splits data across multiple shards.
    Each shard is an instance of LmdbStorage stored in a subdirectory under a base path.
    """
    def __init__(self, base_path, num_shards=5, map_size=70*1024*1024*1024):
        """
        :param base_path: Base directory where shard subdirectories will be created.
        :param num_shards: Number of shards.
        :param map_size: Map size for each LMDB environment.
        """
        self.num_shards = num_shards
        self.shards = {}
        for shard_idx in range(num_shards):
            shard_path = os.path.join(base_path, f"shard_{shard_idx}")
            os.makedirs(shard_path, exist_ok=True)
            self.shards[shard_idx] = LmdbStorage(shard_path, map_size=map_size)

    def _get_shard_for_id(self, identifier):
        identifier_str = str(identifier).encode('utf-8')
        h = hashlib.md5(identifier_str).hexdigest()
        return int(h, 16) % self.num_shards

    def store_data(self, data, identifiers, batch_size=5000):
        """
        Stores data items by grouping them by shard.
        """
        # Group data and identifiers by shard index
        shard_data = {i: [] for i in range(self.num_shards)}
        shard_ids = {i: [] for i in range(self.num_shards)}
        for vec, identifier in zip(data, identifiers):
            shard = self._get_shard_for_id(identifier)
            shard_data[shard].append(vec)
            shard_ids[shard].append(identifier)
        # Call store_data on each shard that has items
        for shard, lmdb_storage in self.shards.items():
            if shard_data[shard]:
                lmdb_storage.store_data(shard_data[shard], shard_ids[shard], batch_size=batch_size)
    
    def get_data(self, identifiers):
        """
        Retrieves data items by grouping identifiers by shard.
        Returns a list of found data in the same order as identifiers.
        """
        id_to_data = {}
        shard_ids = {i: [] for i in range(self.num_shards)}
        for identifier in identifiers:
            shard = self._get_shard_for_id(identifier)
            shard_ids[shard].append(identifier)
        for shard, lmdb_storage in self.shards.items():
            if shard_ids[shard]:
                data_list = lmdb_storage.get_data(shard_ids[shard])
                for identifier, data in zip(shard_ids[shard], data_list):
                    id_to_data[identifier] = data
        return [id_to_data.get(identifier, None) for identifier in identifiers]

    def store_vectors(self, data, identifiers, batch_size=5000):
        """
        Stores vector data by grouping them by shard.
        """
        shard_data = {i: [] for i in range(self.num_shards)}
        shard_ids = {i: [] for i in range(self.num_shards)}
        for vec, identifier in zip(data, identifiers):
            shard = self._get_shard_for_id(identifier)
            shard_data[shard].append(vec)
            shard_ids[shard].append(identifier)
        for shard, lmdb_storage in self.shards.items():
            if shard_data[shard]:
                lmdb_storage.store_vectors(shard_data[shard], shard_ids[shard], batch_size=batch_size)

    def store_sparse_vectors(self, data, identifiers):
        """
        Distributes rows of a sparse matrix across shards for storage.
        """
        if not sp.issparse(data):
            raise TypeError("Input data must be a SciPy sparse matrix.")
        
        csr_data = data.tocsr()
        
        # Group row slices and identifiers by shard index
        shard_rows = {i: [] for i in range(self.num_shards)}
        shard_ids = {i: [] for i in range(self.num_shards)}

        for i, identifier in enumerate(identifiers):
            shard_idx = self._get_shard_for_id(identifier)
            shard_rows[shard_idx].append(csr_data[i])
            shard_ids[shard_idx].append(identifier)

        # For each shard, stack its rows and store them
        for shard_idx, lmdb_storage in self.shards.items():
            if shard_rows[shard_idx]:
                # Stack the collected rows for this shard into a single matrix
                shard_matrix = sp.vstack(shard_rows[shard_idx], format='csr')
                lmdb_storage.store_sparse_vectors(shard_matrix, shard_ids[shard_idx])

    def get_vectors(self, identifiers):
        """
        Retrieves vector data items by grouping identifiers by shard.
        Returns a list of vectors in the same order as identifiers.
        """
        id_to_vector = {}
        shard_ids = {i: [] for i in range(self.num_shards)}
        for identifier in identifiers:
            shard = self._get_shard_for_id(identifier)
            shard_ids[shard].append(identifier)
        for shard, lmdb_storage in self.shards.items():
            if shard_ids[shard]:
                vectors = lmdb_storage.get_vectors(shard_ids[shard])
                for identifier, vector in zip(shard_ids[shard], vectors):
                    id_to_vector[identifier] = vector
        return [id_to_vector.get(identifier, None) for identifier in identifiers]

    def get_sparse_vectors(self, identifiers):
        """
        Retrieves sparse vectors from across shards and reconstructs them in the correct order.
        """
        id_to_vector_row = {}
        shard_ids = {i: [] for i in range(self.num_shards)}

        # Group identifiers by the shard they belong to
        for identifier in identifiers:
            shard_idx = self._get_shard_for_id(identifier)
            shard_ids[shard_idx].append(identifier)

        # Retrieve from each shard
        for shard_idx, lmdb_storage in self.shards.items():
            if shard_ids[shard_idx]:
                # This returns a single sparse matrix for the retrieved vectors from this shard, or None
                retrieved_matrix = lmdb_storage.get_sparse_vectors(shard_ids[shard_idx])
                
                # Corrected line: Check for None explicitly instead of truthiness.
                if retrieved_matrix is not None:
                    # Map each identifier to its corresponding row in the retrieved matrix
                    for i, identifier in enumerate(shard_ids[shard_idx]):
                        id_to_vector_row[identifier] = retrieved_matrix[i]
        
        # Reconstruct the final list of rows in the original order
        ordered_rows = [id_to_vector_row.get(identifier) for identifier in identifiers]
        final_rows = [row for row in ordered_rows if row is not None]
        
        if final_rows:
            return sp.vstack(final_rows, format='csr')
            
        return None

    def delete_data(self, identifiers):
        """
        Deletes data items by grouping identifiers by shard.
        """
        shard_ids = {i: [] for i in range(self.num_shards)}
        for identifier in identifiers:
            shard = self._get_shard_for_id(identifier)
            shard_ids[shard].append(identifier)
        for shard, lmdb_storage in self.shards.items():
            if shard_ids[shard]:
                lmdb_storage.delete_data(shard_ids[shard])

    def get_data_count(self):
        """
        Returns the total count of entries across all shards.
        """
        total = 0
        for lmdb_storage in self.shards.values():
            total += lmdb_storage.get_data_count()
        return total

    def sync(self):
        """
        Synchronizes all LMDB environments.
        """
        for lmdb_storage in self.shards.values():
            lmdb_storage.sync()

    def close(self):
        """
        Closes all LMDB environments.
        """
        for lmdb_storage in self.shards.values():
            lmdb_storage.close()

    # Parallelized versions of the methods
    def store_data_parallel(self, data, identifiers, batch_size=5000, max_workers=None):
        """
        Stores data items by grouping them by shard, using parallel execution.
        """
        shard_data = {i: [] for i in range(self.num_shards)}
        shard_ids = {i: [] for i in range(self.num_shards)}
        for vec, identifier in zip(data, identifiers):
            shard = self._get_shard_for_id(identifier)
            shard_data[shard].append(vec)
            shard_ids[shard].append(identifier)
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            for shard, lmdb_storage in self.shards.items():
                if shard_data[shard]:
                    futures.append(executor.submit(lmdb_storage.store_data, shard_data[shard], shard_ids[shard], batch_size))
            for future in as_completed(futures):
                future.result()  # Ensure all futures complete

    def get_data_parallel(self, identifiers, max_workers=None):
        """
        Retrieves data items by grouping identifiers by shard, using parallel execution.
        """
        shard_ids = {i: [] for i in range(self.num_shards)}
        for identifier in identifiers:
            shard = self._get_shard_for_id(identifier)
            shard_ids[shard].append(identifier)
        
        results = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(self.shards[shard].get_data, shard_ids[shard]): shard for shard in shard_ids if shard_ids[shard]}
            for future in as_completed(futures):
                results.extend(future.result())
        return results

    def store_vectors_parallel(self, data, identifiers, batch_size=5000, max_workers=None):
        """
        Stores vector data by grouping them by shard, using parallel execution.
        """
        shard_data = {i: [] for i in range(self.num_shards)}
        shard_ids = {i: [] for i in range(self.num_shards)}
        for vec, identifier in zip(data, identifiers):
            shard = self._get_shard_for_id(identifier)
            shard_data[shard].append(vec)
            shard_ids[shard].append(identifier)
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            for shard, lmdb_storage in self.shards.items():
                if shard_data[shard]:
                    futures.append(executor.submit(lmdb_storage.store_vectors, shard_data[shard], shard_ids[shard], batch_size))
            for future in as_completed(futures):
                future.result()  # Ensure all futures complete

    def get_vectors_parallel(self, identifiers, max_workers=None):
        """
        Retrieves vector data items by grouping identifiers by shard, using parallel execution.
        """
        shard_ids = {i: [] for i in range(self.num_shards)}
        for identifier in identifiers:
            shard = self._get_shard_for_id(identifier)
            shard_ids[shard].append(identifier)
        
        results = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(self.shards[shard].get_vectors, shard_ids[shard]): shard for shard in shard_ids if shard_ids[shard]}
            for future in as_completed(futures):
                results.extend(future.result())
        return results
