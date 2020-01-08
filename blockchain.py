from datetime import datetime
from random import randint
import hashlib
import json
import jsonpickle


class Block:
    def __init__(self, data, previous_hash=''):
        self.timestamp = ""
        self.data = data
        self.previous_hash = previous_hash
        self.hash = ""
        self.miningstrenght = 1
        # random number for proof of work
        self.block_nonce = randint(1,10000000)

    def calculateHash(self):
        hash = str(self.previous_hash) + \
            str(self.timestamp) + \
            str(self.data) + \
            str(self.block_nonce)
        encoded_hash = hash.encode(encoding='UTF-8', errors='strict')
        calculatedHash = hashlib.sha256(encoded_hash).hexdigest()
        return calculatedHash

    def setDifficulty(self, strength):
        self.strength = strength

    def cryptomine(self):
        # building the padding proof of work zeros
        zeroproofstring = ""
        for check in range(0, self.miningstrenght):
            # proof of work for prepadding
            zeroproofstring = zeroproofstring + "0"
            check = len(zeroproofstring)
        # mining the block
        while (self.hash[0:self.miningstrenght] != zeroproofstring):
            self.block_nonce = self.block_nonce + 1
            self.hash = self.calculateHash()
            self.timestamp = str(datetime.now())
        print("Solution for block found. Mined coin value: ", self.hash)


class Transaction:
    def __init__(self, sender, reciver, coins):
        self.reciver = reciver
        self.sender = sender
        self.coins = coins
        self.data = "None"


class Blockchain:
    def __init__(self):
        self.chain = [self.createGenesisBlock()]
        self.init_time = datetime.now()
        self.pendingTransactions = []
        self.reward = 10

    def createGenesisBlock(self):
        genesisblock = Block([Transaction("GENESIS", "GENESIS", "GENESIS")],"NULL")
        genesisblock.hash=genesisblock.calculateHash()
        return genesisblock

    def getLastBlock(self):
        return self.chain[len(self.chain) - 1]

    def minePendingBlocks(self, rewardto):
        block = Block(self.pendingTransactions)
        block.previous_hash = self.getLastBlock().hash
        block.cryptomine()
        print("Sucessufully mined")
        self.chain.append(block)
        # null the pending transactions 
        self.pendingTransactions = [Transaction(rewardto,"null", self.reward)]

    def createTransaction(self, transaction):
        self.pendingTransactions.append(transaction)

    def addBlock(self, block):
        block.previous_hash = self.getLastBlock().hash
        block.cryptomine()
        self.chain.append(block)

    def calculateBalance(self, address):
        balance = 0
        for block in self.chain:
            for trans in block.data:
                if(trans.sender == address):
                    balance -= trans.coins
                elif(trans.reciver == address):
                    balance += trans.coins
        return balance

    def validitycheck(self):
        for i in range(0, len(self.chain)):
            i = + 1
            actualBlock = self.chain[i]
            previousBlock = self.chain[i - 1]

            if(actualBlock.hash != actualBlock.calculateHash()):
                return False
            elif(actualBlock.previous_hash != previousBlock.hash):
                return False
            else:
                return True

# POC code for mainfilling the transacions and Block mining 

########################################## MAIN POC 
Mycoin = Blockchain()
Mycoin.createTransaction(Transaction("address001", "address002", 100))
Mycoin.createTransaction(Transaction("address001", "address002", 50))
Mycoin.minePendingBlocks("marek-address")
Mycoin.createTransaction(Transaction("address001", "address002", 100))
Mycoin.createTransaction(Transaction("address001", "marek-address", 50))
Mycoin.minePendingBlocks("marek-address")
Mycoin.createTransaction(Transaction("address001", "address002", 100))
Mycoin.createTransaction(Transaction("address001", "marek-address", 50))
Mycoin.minePendingBlocks("marek-address")
Mycoin.createTransaction(Transaction("address001", "address002", 100))
Mycoin.createTransaction(Transaction("address001", "marek-address", 50))
Mycoin.minePendingBlocks("marek-address")
########################################## END POC 

print("\nBlockchain data:\n")
print(json.dumps(json.loads(jsonpickle.encode(Mycoin)), indent=4, sort_keys=True))
# Get my account balance 
marek = Mycoin.calculateBalance("marek-address")
print(marek)
# blockchain validity check in block hashes. 
print("\n Chain status:", Mycoin.validitycheck())
