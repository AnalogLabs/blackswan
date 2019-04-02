# BYTELOCK.py
# Save and retrieve binary data on the Ethereum blockchain
# Author: Omar Metwally, MD
# omar@analog.earth
# Analog Labs License

# Copyright (c) 2018-present 
# Omar Nabil Metwally, MD
# omar@analog.earth

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# This work, and all derivatives of this work, must remain in the public domain.

# Authors of commercial derivatives and applications of this work must offer to all members 
# of the public the opportunity for stakeholdership in said works in the form of ERC20-based token(s), 
# in an equal and fair manner that does not discriminate based on age, body size, disability, 
# ethnicity, gender identity and expression, nationality, personal apperance, race, religion, 
# sexual identity and orientation, level of experience, institutional affiliation, or material means. 

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from bcinterface import *
from time import sleep

CHUNK_SIZE = 32  # size of chunk in bytes
TIMEOUT = 60*2  #number of seconds to wait between chunks while uploading to blockchain
DEFAULT_NEW_CHUNK_GAS = 49777
DEFAULT_UPDATE_CHUNK_GAS = 29812

eth_password = ''

greeting = """
B Y T E L O CK

Save and retrieve binary data on the Ethereum blockchain.
By using this software, you agree to the Analog Labs License available at analog.earth
(C) 2018 - present Omar Metwally, MD

"""
print(greeting)
filename = input("Enter a file path and name: ")
eth_password = input("Enter your Ethereum password: ")

b = None

with open(filename) as imageFile:
    f = imageFile.read()
    b = bytearray(f, 'utf-8')

print("Length of binary file in bytes: ",len(b))

i = 0
file_in_bytes = []

while i < len(b):
	
	file_in_bytes.append( hex( b[i] ) )

	i+=1

print("Chunk size: ",CHUNK_SIZE)
print("Number of chunks: ", str(len(b)/CHUNK_SIZE))
i = 0
while i*CHUNK_SIZE < len(b):
    index = i
    bytes32_data = str(file_in_bytes[ i*CHUNK_SIZE: i*CHUNK_SIZE+CHUNK_SIZE]).replace("'","\"")

    #print("Index: ",index)
    #print("bytes32 data: ", bytes32_data)
    i+=1

answer = input("Would you like to upload this file to the Ethereum blockchain? (y/N)\n> ")
if answer[0].lower() == 'y':
    bci = BCInterface(mainnet=True)
    bci.load_contract()

    i=0
    while i*CHUNK_SIZE < len(b):
        index = i
        bytes32_data = file_in_bytes[ i*CHUNK_SIZE: i*CHUNK_SIZE+CHUNK_SIZE]
        bytes32_arg = bci.web3.toHex( b[i*CHUNK_SIZE: i*CHUNK_SIZE+CHUNK_SIZE] ) 
        '''
        for l in bytes32_data:
            print(l[2:])
            bytes32_arg += l[2:]
        '''
        
        num_chunks = bci.contract.call().get_num_chunks(bci.eth_accounts[bci.account_index])
        #print("Number of chunks: ",num_chunks)
        #print("Index: ",index)
        #print("bytes32 data: ", bytes32_arg)

        if index < num_chunks:
            #bci.set_gas(DEFAULT_NEW_CHUNK_GAS)
            #print("updating chunk at index ",index)
            #bci.contract.transact(bci.tx).update_chunk(index, bytes32_arg)
            print("skipping index ", index)
            pass
        else:
            #bci.set_gas(DEFAULT_UPDATE_CHUNK_GAS)
            print("uploading new chunk: ", bytes32_arg)
            #try:
            bci = BCInterface(mainnet=True)
            bci.load_contract()
            bci.unlock_account(eth_password)
            bci.set_gas(50000)
            bci.contract.transact(bci.tx).new_chunk(index, bytes32_arg)
            #except:
            #print('upload to blockchain failed.')
            sleep(TIMEOUT)

        i+=1



