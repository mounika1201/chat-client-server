How to Run
------------
* python 3 is required to run this project
* Each client and server directories has Makefile to install the required dependencies and to run the project
------------
* Run make install in each directory (chat-client or chat-server), to make sure you have all the packages installed to the run the script
    * By default script runs using python and pip interpreters
    * If you want to change the interpreters run using eg: make install PYTHON_INTERPRETER=python3 PIP_INTERPRETER=pip3
    
* Run the chat-server
    * command: `make run` (defaults to python and pip interpreters)
    * Running with different interpreters `make run PYTHON_INTERPRETER=python3`
    
* Run the chat-client
    * command: `make run HOST=127.0.0.1 PORT=4711`
    * Running with different interpreters `make run PYTHON_INTERPRETER=python3 PIP_INTERPRETER=pip3 HOST=127.0.0.1 PORT=4711`