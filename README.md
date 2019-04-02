# Blackswan 
## Blockchain File System
```
Omar Metwally, MD
Principal Investigator
Analog Labs, Logisome, Inc. R&D
omar@analog.earth
www.analog.earth/blackswan
```


## Introduction
Using a public blockchain as a filesystem is a relatively costly method of storing data that confers the advantages of permanence and global accessibility by any computer with an internet connection [1]. A public blockchain is perpetuated by all nodes, which total an estimated 8,194 nodes at the time of writing, of which 2,675 (32.65%) are located in the United States, 1,068 nodes (13.03%) are located in Germany, and 661 nodes (8.07%) are located in China [2]. Because each node stores an identical copy of the blockchain either in its entirely or a cryptographic summary of the blockchain’s state, data stored in this manner are not susceptible to loss and corruption, as is the case with data stored on centralized servers [3]. Ensuring the permanence and authenticity of data is critical to the operation of corporations and governmental bodies, for instance to store information about customers, internal documents, and for enforcement of intellectual property laws. Analog Labs, the Research and Development Division of Logisome, Inc., benefits from the blockchain data structure’s properties in order to securely archive information generated by research activities and to make this information publicly accessible [4].


## Prerequisites
You’ll need to download and install the Ethereum client written in the Go programming language, also known as the "Go Ethereum client" [5].

## Methods
All data on a public blockchain can be freely downloaded by anyone running the client software. Files optionally can be encrypted using encryption ciphers before being uploaded to the blockchain as a way of restricting access to individuals capable of decryption. To encrypt data using the AES-256 cipher as implemented in the OpenSSL library:

```
openssl aes-256-cbc -a -salt -in file.txt -out file.txt.enc
```
Where file.txt is the name of the input file and file.txt.enc is the encrypted output file.

To decrypt *file.txt.enc*, run the same account, adding the flag ```-d``` just before ```-a```.

The code contained in *bytelock.py* chunks an input file into a sequence of 32 byte segments and uploads them one by one to the public Ethereum blockchain [4]. Each transaction is temporally separated by a user-defined time interval (120 seconds by default) to ensure that the chunks are mined in the correct order. 

A file can be downloaded from the public blockchain, once again in 32 byte chunks, and reconstituted in a similar manner.

### Bytelock.py script
Interaction with the public blockchain requires an internet connection and a running client. The following command entered in a Linux or Mac OS terminal starts the Go Ethereum client in interactive mode:

```
geth --syncmode light console
```
Clone or download the Blackswan repository and navigate to the local copy on your machine. In this example, the repository was cloned to the Desktop:

```
mkdir ~/Desktop/blackswan

cd ~/Desktop/blackswan

git init

git remote add origin https://github.com/AnalogLabs/blackswan

git pull origin master
```

### Upload
To upload *file.txt* in unencrypted form to the public blockchain, the Ethereum account that will be used must have sufficient funds and must be unlocked prior to running the script that uploads the file in 32 byte chunks. Run these commands at your own discretion only when you understand what they entail [5]. The zero numeral in this command specifies the zero-indexed Ethereum account on the local host: 

```
> eth.unlockAccount(eth.accounts[0])
```

In a separate Terminal window, run the bytelock.py script to chunk and sequentially upload the file, transaction by transaction, to the blockchain. Note that this requires a variable amount of funds and time and is generally a far more expensive, albeit permanent, way of storing information compared to the Interplanetary Filesystem (IPFS) [6]. 

```
python3 bytelock.py
```

The latter script will prompt the user to specify a file path and name as well as the Ethereum account password for the zero-indexed account. Note that this is not a secure way of handling passwords and is provided for demonstration purposes only. A more secure way would be to unlock the account using the client, as described above, and leaving the prompt blank (pressing Enter).

### Download
Downloading information from the blockchain does not require an unlocked account or any funds. The Blackswan contract [bxs.sol](https://github.com/AnalogLabs/blackswan/blob/master/source/bxs.sol) utilizes the following methods to query the number of records in the ledger and to retrieve a record:

```
get_record(address _author, uint _index) public view returns(string memory _desc)
get_num_records(address _author) public view returns (uint)
update_record(uint _index, string memory _desc, uint start_index, uint endindex) public returns (bool) 
```

The latter methods are described in more detail below. These are called pythonically when the following script is run and need not be executed outside this context:

```
python3 download.py
```
The latter script prompts the user for an output file name, a start index, and a terminal index, the latter two corresponding to the index of the first and last chunks on the blockchain. The get_chunk method is iteratively called to download each chunk sequentially, and the chunks are concatenated and saved as the output file name. 


### Record Struct
A *Record* is a Solidity struct that describes an entry in the Blackswan ledger. Each Record comprises the following entities:

```
struct Record {
	address author;  // the owner of the Record
	string desc;	 // a description
	uint start_index;  // the index of the chunk on the blockchain at which the file begins
	uint end_index;   // the index of last chunk of a file on the blockchain 
}
```
Example (note that this example uses the Blockchain Interface (BCInterface) helper class to inerface with the Ethereum client (*geth*):
```
cd ~/Desktop/blackswan
python3
>>> from bcinterface import *
>>>  bci = BCInterface(mainnet=True, mac=True)  # set mac=False on Ubuntu
>>> bci.load_contract()
>>> bci.howdy_ho()  # sanity check
>>> bci.contract.transact(bci.tx).new_record("Zero-Gravity Stove I.P. Disclosure", 0, 7805)
```

### Query number of records
To query the number of records in the ledger:

```
function get_num_records(address _author) public view returns (uint)
```
Example:
```
>>> bci.contract.call().get_num_records("0x3036a12f56af68165e625b99cd12d2070f0d9a90")
>>> 324
```

### Create a new record
To register a new record on the blockchain without actually uploading a file (this can also be used to upload short text blocks):
```
function new_record(string memory _desc, uint _start_index, uint _end_index) public returns (bool)
```
Example:
```
>>> bci.contract.transact(bci.tx).new_record("Zero-Gravity Stove I.P. Disclosure", 0, 7805)
```
Note that the start chunk cannot override a pre-existing record, otherwise the transaction will fail and the data will not be overwritten.

### Update a record
```
function update_record(uint _index, string memory _desc, uint _start_index, uint _end_indx) public returns (bool)
```
Example:
```
>>> bci.contract.transact(bci.tx).update_record(52, "3D printed bicycle frame", 1136, 10879)
```

### Query a record
To query a record at a specific index:
```
function get_record(address _author, uint _index) public view returns (string memory_desc, uint _start_index, uint _end_index)
```
Example:
```
>>> bci.contract.call().get_record("0x3036a12f56af68165e625b99cd12d2070f0d9a90", 13)
```

### Query the total number of chunks 
Returns the total number of chunks uploaded by a user:
```
function get_num_chunks(address _owner)
```
Example:
```
>>> bci.contract.call().get_num_chunks("0x3036a12f56af68165e625b99cd12d2070f0d9a90")
>>> 7996
```

### Query a chunk
Return a chunk (bytes32) at a specified index:
```
function get_chunk(address _owner, uint _index) public view returns (bytes32 _data)
```
Example:
```
>>> bci.contract.call().get_chunk("0x3036a12f56af68165e625b99cd12d2070f0d9a90", 52)
```

### Update a chunk
Re-write the contents of an existing chunk at a specified index:
```
function update_chunk(uint _index, bytes32 _data) public returns (bool)
```
```
chunk_data = ...
>>> bci.contract.transact(bci.tx).update_chunk(6782, chunk_data)
```

## References
* Trolling for a Wealthier World. Omar Metwally. October 16th, 2017. https://omarmetwally.blog/2017/10/16/trolling-for-a-wealthier-world/

* Ethereum Node Tracker. https://etherscan.io/nodetracker

* On the Economics of Knowledge Creation and Sharing. Omar Metwally. September 12th, 2017. http://adsabs.harvard.edu/abs/2017arXiv170907390M. 
arXiv:1709.07390.

* Black Swan Intellectual Property Ledger. Analog Labs. https://github.com/AnalogLabs/blackswan. 

* Go-Ethereum Command Line Options. https://github.com/ethereum/go-ethereum/wiki/Command-Line-Options. 

* Interplanetary Filesystem. https://ipfs.io/. 


## Contribute
Please take a look at the [contribution documentation](https://github.com/simbel/simbel/blob/master/docs/CONTRIBUTING.md) for information on how to report bugs, suggest enhancements, and contribute code. If you or your organization use Blackswan to do something great, please share your experience! 

## Code of conduct
In the interest of fostering an open and welcoming environment, we as contributors and maintainers pledge to making participation in our project and our community a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation. Read the full [Contributor Covenant](https://github.com/analoglabs/blackswan/blob/master/docs/CODE_OF_CONDUCT.md). 

## Acknowledgements
This project builds on work by the [Ethereum](https://www.ethereum.org) and [web3.py](https://github.com/pipermerriam/web3.py) communities. 

## License
[Analog Labs License](https://www.analog.earth/license)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions: 

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software. 

This work, and all derivatives of this work, must remain in the public domain.

Authors of commercial derivatives and applications of this work must offer to all members of the public the opportunity for stakeholdership in said works in the form of ERC20-based token(s), in an equal and fair manner that does not discriminate based on age, body size, disability, ethnicity, gender identity and expression, nationality, personal appearance, race, religion, sexual identity and orientation, level of experience, institutional or political affiliation, or material means. 

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


