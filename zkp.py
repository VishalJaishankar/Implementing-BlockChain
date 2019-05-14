import hashlib
import random
primes = [472882049,492876847,492876863,512927357,512927377,533000389, 533000401,553105243 ,553105253,573259391]

class Alice(object):
    '''
    Alice is an abstraction of a sender who wants to prove authority 
    to Bob(verifier) without giving him any information about the data Sender has
    '''
    def __init__(self,msg):
        self.msg = str(msg)
        result = hashlib.sha1(self.msg.encode())
        self.x = int(result.hexdigest(),16)%1000 

        self.p = 472882049
        self.g = 4
        self.y = (self.g**self.x)%self.p
        self.r = random.randint(0,self.p-1)
        self.h =  (self.g**self.r)%self.p
        self.b = None #given by bob
        self.s = None
    def print_dets(self):
        print(self.x,self.y,self.r,self.p,self.g,self.h,self.b,self.s)

class Bob(object):
    '''
    Abstraction of Verifier who checks the validity of the user trying to add a block
    to the blockchain
    '''
    def __init__(self):
        self.g = None
        self.p = None
        self.h = None
        self.b = None
        self.s = None

    def print_dets(self):
        print(self.p,self.g,self.h,self.b,self.s)

class Channel(object):
    def __init__(self,Alice,Bob):
        self.Alice = Alice
        self.Bob = Bob
    
    def set_p_g(self):
        self.Bob.g = self.Alice.g
        self.Bob.p = self.Alice.p
    
    def exchange_h(self):
        self.Bob.h = self.Alice.h
    
    def exchange_b(self):
        # bob sends a random bit
        if random.randint(0,100)%2==0:
            self.Bob.b = 1
            self.Alice.b =1
        else:
            self.Bob.b = 0
            self.Alice.b =0
    def exchange_s(self):
        #alice computes s then send to bob
        self.Alice.s = (self.Alice.r+(self.Alice.b * self.Alice.x))%(self.Alice.p - 1)
        self.Bob.s = self.Alice.s
    def Bob_final(self):
        lhs = ((self.Bob.g)**(self.Bob.s))%self.Bob.p
        rhs = ((self.Alice.h)*((self.Alice.y)**(self.Alice.b)))%(self.Alice.p)
        return lhs == rhs
        




# this is able to validate 
'''
Achived:
Kind of a Server client architecture using a Channel class that connects the two
Problems:
    setting of p and g which should be the generator of prime p
    

'''
'''
def main():
    a = Alice("hello")
    b = Bob()
    c = Channel(a,b)

    c.set_p_g()
    a.print_dets()
    b.print_dets()

    c.exchange_h()
    a.print_dets()
    b.print_dets()

    c.exchange_b()
    a.print_dets()
    b.print_dets()

    c.exchange_s()
    a.print_dets()
    b.print_dets()

    print(c.Bob_final())

if __name__ == '__main__':
    main()
'''