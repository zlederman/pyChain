import time
import hashlib
import json
import random
import string
import ast

class BlockChain:
    def __init__(self):
        self.genesis_block = Block(
                                    1231006505, 
                                    "0000000000000000000000000000000000000000000000000000000000000000",
                                    Transactions([Transaction(
                                        "D06FE1B9B34919655BC0068844707EC6CD158981BAA275C1BC759B6A0B5DBD92",
                                        "3A53722CCECFB5DCFC0A931FCEF3A1FADDFBD5218F5E02E8D5CE38FAF7164A9A",
                                        69)
                                        ]),
                                    0)
        print(self.genesis_block)
        self.blockchain = [self.genesis_block]
        self.chain_len = 1
        self.UTXO_POOL = {
                "3A53722CCECFB5DCFC0A931FCEF3A1FADDFBD5218F5E02E8D5CE38FAF7164A92":69,
                "D06FE1B9B34919655BC0068844707EC6CD158981BAA275C1BC759B6A0B5DBD9A":0
                }
    
            
    def dump_chain(self):
        file = open("blockchain_"+str(time.time()))
        for block in self.blockchain:
            file.write(block.prettyPrint())
        file.close()
    
    def print_chain(self):
        for block in self.blockchain:
            block.prettyPrint()

    def add_test(self,txs):
        #"[{sender:###,reciever:###,Quantity:###,Msg:####}]
        valid_txs = self.validate(txs)
        block = self.assemble_block(valid_txs)
        
        return block

    def validate(self,txs):
        validated_txs = []
        for tx in txs:
            print(tx)
            tx_parsed = tx[1:len(tx)-2]
            tx_array = tx_parsed.split(',')
            
            tx_array = [attribute.split(':')[1] for attribute in tx_array]
            sender = tx_array[0]
            print(type(sender))
            quantity = int(eval(tx_array[2]))
            print(quantity)
            if self.UTXO_POOL[eval(sender)] - int(quantity) >= 0:
                validated_txs.append(tx)
        return validated_txs
            #eval into array of tuples 
            #push the sender hash into the utxo dict verif it has enough funds
            #If true then add how much they had to the reciever value

    def assemble_block(self,txs):
        txs = [json.loads(tx) for tx in txs]
        built_txs = []
        for tx in txs:
            built_txs.append(Transaction(tx["sender"], tx["reciever"], int(tx["quantity"]),tx["msg"]))

        prevHash = self.blockchain[-1].encoding
        index = self.chain_len
        new_block = Block(time.time(), prevHash, Transactions(built_txs),index)
        return new_block



class Block:
    def __init__(self,timestamp, prevHash, txs, index):
        self.time = timestamp
        self.prevHash = prevHash
        self.txs = self.stringify(txs)
        self.index = index
        self.encoding = self.encode()
         #this is were I will generate a merkel root

    def encode(self):
        digest = ""
        if self.time and self.prevHash and self.txs:
            digest = str(self.time) + self.prevHash + self.txs + str(self.index) 
        return hashlib.sha256(digest.encode('utf-8')).hexdigest()
   
    def prettyPrint(self):
        print(json.dumps(self.__dict__))
    
    def stringify(self,txs):
        tx_string = ""
        for tx in txs.txs:
            tx_string += str(vars(tx)) + ';'
        return tx_string
    
    def get_txs(self):
        tx_list = self.txs.split(';')
        ret = []
        for tx in tx_list:
            if tx != '':
                ret.append(eval(tx))

        return ret




class Transaction:
    def __init__(self,sender, reciever, quantity,msg=''):
        self.sender = sender
        self.reciever = reciever
        self.quantity = quantity
        self.msg = msg


class Transactions:
    def __init__(self,txs):
        self.txs = txs


class Address:
    def __init__(self):
        self.hash = self.generate_raw(seed=self.seed())
        self.address = self.hash.digest()
        self.address_hex = self.hash.hexdigest()

    def seed(self):
        t = int(time.time())
        return str(random.getrandbits(3000) - t)

    def generate_raw(self, seed = None):
        if seed == None: seed = seed()
        hash = hashlib.sha256(seed.encode())
        return hash
    #this is only the pk, later I need to implement a pubK


def main():
    me = Address().address_hex
    you = Address().address_hex
    bchain = BlockChain()
    bchain.print_chain()
    test_transaction = ['{"sender" :"3A53722CCECFB5DCFC0A931FCEF3A1FADDFBD5218F5E02E8D5CE38FAF7164A92","reciever":"E2AD351FE9CA36617D757452EFD2950014F0058C034766960DA41443583052C6","quantity":30, "msg":"yo whats poppin"}']

    print(test_transaction[0])
    bchain.print_chain()
    bchain.add_test(test_transaction)

if __name__ == "__main__":
    main()
