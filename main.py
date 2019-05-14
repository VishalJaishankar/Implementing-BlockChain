from hashlib import sha256
import random
import datetime
from  zkp import Alice,Bob,Channel

class Block(object):
    '''
    This Describes the structure of the Block 
    '''
    def __init__(self,index,timestamp,amount,client,previousHash = ''):
        '''
        This describes the Time ,amount and the client that initiated the transation from the bank 
        '''
        self.index = index
        self.timestamp = timestamp
        self.amount = amount
        self.previousHash = previousHash
        self.client = client
        self.nonce = random.randint(0,1000000)
        self.hash = self.calculateHash()
        
        #random number
    def calculateHash(self):
        string =str(self.nonce)+str(self.index) + str(self.previousHash) + str(self.timestamp)+str(self.amount)+self.client
        my_bytes = string.encode('utf-8')
        return sha256(my_bytes).hexdigest()

    
    #this is proof of work showing that the miner has done some computation worth some reward
    # begin with a certain amount of zeros
    def mine_block(self,difficulty):
        while self.hash[0:difficulty]!="0"*difficulty:
            self.hash = self.calculateHash()
            self.nonce += 1
        #Note the above is eddless loop since hash wont change so use nonce
        print("Blocked Mined!",self.hash)
    #does the ZKP
    def verify(self):
        a = Alice(self.amount)
        b = Bob()
        c = Channel(a,b)
        c.set_p_g()
        c.exchange_h()
        c.exchange_b()
        c.exchange_s()
        return c.Bob_final()

class BlockChain(object):
    '''
    Defined as array of Blocks
    '''
    def __init__(self,difficulty):
        self.chain = [self.createGenesis()]
        self.difficulty = difficulty
    def createGenesis(self):
        return Block(0,0,"Genesis","Vishal","0")
    
    def get_latest_block(self):
        return self.chain[len(self.chain)-1]

    def add_block(self,newBlock):
        '''
        Before adding a new Block we will verify the transaction by ZKP
        '''
        
        newBlock.previousHash = self.get_latest_block().hash
        newBlock.mine_block(self.difficulty)
        newBlock.hash = newBlock.calculateHash()
        self.chain.append(newBlock)

    def print_amounts(self):
        for block in self.chain:
            print(block.index," ",block.timestamp," ",block.amount," ",block.client," ",block.hash,block.previousHash)


    def is_chain_valid(self):
        for i in range(len(self.chain)):
            currBlock = self.chain[i]
            prevBlock = self.chain[i-1]
            if i!=0:    #skip over the genesis block
                #first see if the hash is still valid
                # this ensures the amount was modified or not
                if currBlock.hash!=currBlock.calculateHash():
                    return False
                # check previous hash property
                if currBlock.previousHash!=prevBlock.hash:
                    return False
        
        return True
                



def main():
    now = datetime.datetime.now()
    vishalcoin = BlockChain(2)

    while True:
        choice = input("If you wish to Start Transaction ,Press 1\n If you want to check validity of Chain , press 2\nIf you wish to print the Chain ,Press 3\n If you are bored and want to quit, Press 4\n")
        if int(choice) == 1:
            client = input("Enter the client name\n")
            time = now.isoformat()
            amount = input("Enter the amount you want to transfer\n")
            print("Creating Block\n")
            newB = Block(len(vishalcoin.chain),time,amount,client)

            print("Validating Block\n")
            if newB.verify()==True:
                print("Block Verified\n")
            else:
                print("Unauthorized entry\n") 
            
            print("Adding Block to Chain by Doing Proof of Work\n")
            vishalcoin.add_block(newB)
            print("Block Added successfully\n")
        if int(choice) == 2:
            if vishalcoin.is_chain_valid()==True:
                print("Chain is Valid!\n")
            else:
                print("Chain has been modified :(\n")
        if int(choice) == 3:
            vishalcoin.print_amounts()
        if int(choice) == 4:
            break
   # print(vishalcoin.is_chain_valid())
    # vishalcoin.add_block(Block(1,"28/12/1233",123,"Mark"))
    # vishalcoin.add_block(Block(2,"29/12/1233",3121,"Grace"))
    # vishalcoin.add_block(Block(3,"30/12/1233",3123,"Adam"))
    
    #vishalcoin.print_amounts()
    # print(len(vishalcoin.chain))
    #print(vishalcoin.is_chain_valid())





if __name__ == '__main__':
    main()