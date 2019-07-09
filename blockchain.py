import hashlib
import json
from datetime import datetime


class Transaction:

    def __init__(self, from_address, to_address, amount):
        self.from_address = from_address
        self.to_address = to_address
        self.amount = amount


class Block:

    def __init__(self, t_stamp, transactions_list, prev_hash='0'*64):
        self.nonce = 0
        self.t_stamp = t_stamp
        self.transactions_list = transactions_list
        self.prev_hash = prev_hash
        self.curr_hash = self.calc_hash()

    def calc_hash(self):
        """Calculates the current hash for the current block"""

        data = {"nonce": self.nonce,
                "t_stamp": str(self.t_stamp),
                "transaction_list": str(self.transactions_list),
                "prev_hash": str(self.prev_hash)
                }
        block_data = json.dumps(data, sort_keys=True).encode()
        return hashlib.sha256(block_data).hexdigest()

    def mine_block(self, diffi):
        """ Mine the block """
        while self.curr_hash[:diffi] != str('').zfill(diffi):
            self.nonce += 1
            self.curr_hash = self.calc_hash()

    def __str__(self):
        """Prints the current block's details"""
        output_string = "nonce: " + str(self.nonce) + "\n" \
                        "t_stamp: " + str(self.t_stamp) + "\n" \
                        "transaction_list: " + str(self.transactions_list) + "\n" \
                        "prev_hash: " + str(self.prev_hash) + "\n" \
                        "curr_hash: " + str(self.curr_hash) + "\n"

        return output_string


class BlockChain:

    def __init__(self):
        """
        Instantiate the BlockChain with the genesis block
        mining_reward is the reward that the miner will get
        difficulty is the hash difficulty with no. of initial zeroes in the hash
        """
        self.chain = [self.generate_genesis_block(), ]
        self.pending_transactions = []
        self.mining_reward = 500
        self.difficulty = 3

    def generate_genesis_block(self):
        """Generates the Genesis block with the given date"""
        return Block('06/07/2019', [Transaction(None, None, 0), ])

    def get_last_block(self):
        """Get the last block in the block chain"""
        return self.chain[-1]

    def mine_pending_transaction(self, miner_address):
        """
        Generate the block processing the pending transactions
        Also reward the miner with the mining_reward
        """
        block = Block(datetime.now(), self.pending_transactions, self.get_last_block().curr_hash)
        block.mine_block(self.difficulty)
        print('Block is mined. Reward: ', self.mining_reward)
        self.chain.append(block)
        self.pending_transactions = [Transaction(None, miner_address, self.mining_reward)]

    def create_transaction(self, trans):
        """Creates transaction and add it to the list of the pending transactions
         to be processed when the next block is mined"""
        self.pending_transactions.append(trans)

    def print_blocks(self):
        """Prints all the blocks with their block No. , previous hash and the current hash"""
        i = 1
        for b in self.chain:
            print()
            print('block no: ' + str(i))
            print('prev_hash: ' + b.prev_hash)
            print('curr_hash: ' + b.curr_hash)
            i += 1

    def get_balance(self, address):
        """Return the balance with the given address"""
        balance = 0
        for b in self.chain:
            for t in b.transactions_list:
                if t.to_address == address:
                    balance += t.amount

                if t.from_address == address:
                    balance -= t.amount

        return balance

    def is_chain_valid(self):
        """Checks if the chain is valid and not tempered"""
        for i in range(1, len(self.chain)):
            prev_b = self.chain[i-1]
            curr_b = self.chain[i]

            if curr_b.curr_hash != curr_b.calc_hash():
                print("Invalid Block")
                return False

            if curr_b.prev_hash != prev_b.curr_hash:
                print("Invalid Chain")
                return False

        return True


my_coin = BlockChain()
miner1_address = 'add12323'

print("Starting Mining")
my_coin.mine_pending_transaction(miner1_address)

# the mining_reward is added to the pending_transaction_list. Hence currently the balance is 0
print("miner balance with address {} is ".format(miner1_address), my_coin.get_balance(miner1_address))

print("\nStarting Mining")
my_coin.mine_pending_transaction(miner1_address)
print("miner balance with address {} is ".format(miner1_address), my_coin.get_balance(miner1_address))


# Transactions to be added to the next block
my_coin.create_transaction(Transaction(miner1_address, 'add2', 100))
my_coin.create_transaction(Transaction('add2', miner1_address, 20))

print("\nStarting Mining")
my_coin.mine_pending_transaction(miner1_address)

# printing the miner's balanced
print("miner balance with address {} is ".format(miner1_address), my_coin.get_balance(miner1_address))

my_coin.print_blocks()

