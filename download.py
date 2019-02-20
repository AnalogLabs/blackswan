# DOWNLOAD.py
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

THROTTLE = 0.001  #number of seconds to wait between chunks while downloading to blockchain; prevents breaking IPC socket

greeting = """
B Y T E L O CK

Save and retrieve binary data on the Ethereum blockchain.
By using this software, you agree to the Analog Labs License available at analog.earth
(C) 2018 - present Omar Metwally, MD

"""
print(greeting)
start_index = 0
end_index = 0
output_file = input('Enter an output file name: ')
start_index = input('Enter a start index: ')
start_index = int(start_index)
end_index = input('Enter a terminal index: ')
end_index = int(end_index)
assert(start_index < end_index)

bci = BCInterface(mainnet=True)
bci.load_contract()
print(bci.contract.call().get_chunk(bci.eth_accounts[0],0))
sleep(2)

i = start_index
fo = ''
while i < end_index:
        z = bci.contract.call().get_chunk(bci.eth_accounts[0],i).decode('utf-8').strip()
        print(i, z)
        if '\n' in z:
                print("CRLF found!")
        z = z.replace('\n','')
        fo+= z
        sleep(THROTTLE)
        i+=1

print('Saving to file...')
myfile = open(output_file,'w+')

num_chars = len(fo)
line_index = 0
char_index = 0
line = ''
for c in fo:
        line += c
        line_index+=1
        char_index+=1
        if len(line) == 64 :
                print(line_index, line)
                myfile.write(line+'\n')
                line_index = 0
                line = ''
        if char_index == num_chars:
                print(char_index, line)
                myfile.write(line+'\n')

