import numpy as np
from InputsConfig import InputsConfig as p
from Models.Bitcoin.Node import Node
from Models.Consensus import Consensus as BaseConsensus
import random
from simple_pid import PID


class Consensus(BaseConsensus):

    """
	We modelled PoW consensus protocol by drawing the time it takes the miner to finish the PoW from an exponential distribution
        based on the invested hash power (computing power) fraction
    """
    def Protocol(miner):
        ##### Start solving a fresh PoW on top of last block appended #####
        TOTAL_HASHPOWER = sum([miner.hashPower for miner in p.NODES])
        hashPower = miner.hashPower/TOTAL_HASHPOWER ## Change this to hash power in 
        avg_hashpower = TOTAL_HASHPOWER*10e9#/len([miner.hashPower for miner in p.NODES])*10e9
        print(avg_hashpower)
        file1 = open("diff.txt","r+")
        #print("jk" , float(file1.read().split(';')[0]))
        data = file1.read().split(';')
        difficulty = float(data[0]) #22012.4941572/10 
        hashtime = float(data[1])
        file1.close()
        #hashtime = difficulty * 2**32 / (avg_hashpower)
        print(hashtime)

        # hash power is hashes per second, therefore 10 hashes per second and a Binterval of 30 sec gives us 300 hashes 
        #random.expovariate(hashPower * 1/p.Binterval) this one is different; they were measuring hash power in percent of total hashpower; therefore estimating 20% of interval 
        

        # Target hashtime is p.Binterval
        # Variance in computational power and randomness in the guesses can be seen as noise
        # PID controller will aim to reach the target hashtime in the face of variance present from the Variance in computational power and randomness in the hash guesses
        
        pid = PID(50, 0.1, 0.4, setpoint=60)
        #pid.output_limits = (20, 200)    # Output value will be between 0 and 10`
        # Assume we have a system we want to control in controlled_system
        #v = controlled_system.update(0)
        #print(hashtime)
    
        while True== False:
            # Compute new output from the PID according to the systems current value
            control = pid(hashtime)
            print("Inside" , hashtime)
            
            hashtime += control * 2**32 / (avg_hashpower) * 0.0001
            print("kdmk" , hashtime)
            # Feed the PID output to the system and get its current value
            #v = controlled_system.update(control)
            
        #withnoise = random.expovariate(1/hashtime)
        #print("hashtime withnoise" , withnoise)
        control = pid(hashtime)

        file1 = open("diff.txt","w+")
        file1.write(str(control) + ";" + str(hashtime + control * 2**32 / (avg_hashpower) * 0.01))
        file1.close()
        print("control" , control)
        print("HASHTIME" , hashtime )
        
        return hashtime + control * 2**32 / (avg_hashpower) * 0.0001




    """
	This method apply the longest-chain approach to resolve the forks that occur when nodes have multiple differeing copies of the blockchain ledger
    """
    def fork_resolution():
        BaseConsensus.global_chain = [] # reset the global chain before filling it

        a=[]
        for i in p.NODES:
            a+=[i.blockchain_length()]
        x = max(a)

        b=[]
        z=0
        for i in p.NODES:
            if i.blockchain_length() == x:
                b+=[i.id]
                z=i.id

        if len(b) > 1:
            c=[]
            for i in p.NODES:
                if i.blockchain_length() == x:
                    c+=[i.last_block().miner]
            z = np.bincount(c)
            z= np.argmax(z)

        for i in p.NODES:
            if i.blockchain_length() == x and i.last_block().miner == z:
                for bc in range(len(i.blockchain)):
                    BaseConsensus.global_chain.append(i.blockchain[bc])
                break
