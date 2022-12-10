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
        avg_hashpower = TOTAL_HASHPOWER*10e9 #/len([miner.hashPower for miner in p.NODES])*10e9
        print(avg_hashpower)
        file1 = open("diff.txt","r+")
        data = file1.read().split(';')
        difficulty = float(data[0]) #22012.4941572/10 
        hashtime = float(data[1])
        iteration = int(data[2])
        file1.close()
        print(iteration)
        if iteration == 1000: 
            avg_hashpower = avg_hashpower * 2
            hashtime = difficulty*  2**32 / (avg_hashpower)
        #hashtime = difficulty * 2**32 / (avg_hashpower)
        #print(avg_hashpower)
        #print(hashtime)

        pid = PID(50, 0, 0, setpoint=60)

        control = pid(hashtime)
        
        
     
        file1 = open("diff.txt","w+")
        file1.write(str(control) + ";" + str(hashtime + control * 2**32 / (avg_hashpower) * 0.01) + ";" + str(iteration+1))
        file1.close()
        file1 = open("avg_hashpower.csv","a+")
        #file1.write(str(avg_hashpower) + ";" + str(hashtime + control * 2**32 / (avg_hashpower) * 0.001) + ";" + str(control)+ "\n")
        file1.write(str(avg_hashpower)+",")
        file1.close()
        file1 = open("hashtime.csv","a+")
        file1.write(str(hashtime + control * 2**32 / (avg_hashpower) * 0.01)+',')
        file1.close()

        #print("control" , control)
        print("hashtime1 ", hashtime + control * 2**32 / (avg_hashpower) * 0.01)
        return hashtime + control * 2**32 / (avg_hashpower) * 0.01




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
