import hashlib

class ConsistentHashing:
    def __init__(self, nodes, replica_count=3):
        self.replica_count = replica_count
        self.circle = {}
        self.sorted_keys = []
        
        for node in nodes:
            self.add_node(node)
            
    def add_node(self, node):
        for i in range(self.replica_count):
            replica_key = self._get_replica_key(node, i)
            hashed_key = self._hash(replica_key)
            self.circle[hashed_key] = node
            self.sorted_keys.append(hashed_key)
            
        self.sorted_keys.sort()
        
    def remove_node(self, node):
        for i in range(self.replica_count):
            replica_key = self._get_replica_key(node, i)
            hashed_key = self._hash(replica_key)
            
            del self.circle[hashed_key]
            self.sorted_keys.remove(hashed_key)
            
    def get_node(self, key):
        if not self.circle:
            return None
        
        hashed_key = self._hash(key)
        for node_hash in self.sorted_keys:
            if hashed_key <= node_hash:
                return self.circle[node_hash]
        
        return self.circle[self.sorted_keys[0]]
        
    def _hash(self, key):
        return int(hashlib.md5(key.encode()).hexdigest(), 16)
        
    def _get_replica_key(self, node, replica_index):
        return f"{node}-{replica_index}"
        
# Example usage
nodes = ["Node1", "Node2", "Node3"]
ch = ConsistentHashing(nodes)

# Add a new node
ch.add_node("Node4")

# Get node for a key
print(ch.get_node("Key1"))  # Output: Node1

# Remove a node
ch.remove_node("Node2")

# Get node for a key after removing a node
print(ch.get_node("Key1"))  # Output: Node1
