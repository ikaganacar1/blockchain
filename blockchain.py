import hashlib
import datetime as date
import string
#kind of a replica of Bitcoin to learn basics of blockchain

class Block:
    def __init__(self,index,timestamp,data,previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        hash_str = f"{self.index}{self.timestamp}{self.timestamp}{self.nonce}{self.data}{self.previous_hash}"
        return hashlib.sha256(hash_str.encode()).hexdigest()
    

class Blockchain:
    difficulty = 2 
    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = [self.create_genesis_block()]
    
    def create_genesis_block(self):
        return Block(0,date.datetime.now(),"Genesis Block","0")
    
    def get_latest_block(self):
        return self.chain[-1]
    
    def add_block(self,block,proof):
        previous_hash = self.get_latest_block().hash

        if previous_hash != block.previous_hash:
            return False
        if not self.is_valid_proof(block,proof):
            return False
        
        block.hash = proof
        self.chain.append(block)
        return True

    def is_valid_proof(self, block, block_hash):
    
        return (block_hash.startswith('0' * Blockchain.difficulty) and
                block_hash == block.calculate_hash())

    def proof_of_work(self,block):
        block.nonce = 0

        computed_hash = block.calculate_hash()
        while not computed_hash.startswith('0'* Blockchain.difficulty):
            #print(computed_hash)
            block.nonce += 1
            computed_hash = block.calculate_hash()
            
        return computed_hash

    def add_new_transactions(self,transaction):
        self.unconfirmed_transactions.append(transaction)

    def mine(self):
        if not self.unconfirmed_transactions:
            return False
        
        while len(self.unconfirmed_transactions)!=0:
            last_block = self.get_latest_block()
            new_block = Block(index=last_block.index+1,
                            data=self.unconfirmed_transactions[0],
                            timestamp=date.datetime.now(),
                            previous_hash=last_block.hash)

            proof = self.proof_of_work(new_block)
            #print(proof)
            self.add_block(new_block,proof)
            self.unconfirmed_transactions.pop(0)

if __name__ == "__main__":
    # Create the blockchain
    blockchain = Blockchain()

    for letters in string.ascii_letters:
        blockchain.add_new_transactions(str(letters)) # for testing i used ascii letters
        
    blockchain.mine()

    # Print the contents of the blockchain
    for block in blockchain.chain:
        print("Block #" + str(block.index))
        print("Timestamp: " + str(block.timestamp))
        print("Data: " + str(block.data))
        print("Hash: " + block.hash)
        print("Previous Hash: " + block.previous_hash)
        print("Nonce: " + str(block.nonce))
        print("\n")
