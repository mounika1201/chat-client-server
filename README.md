How to Run
------------
* python 3 is required to run this project
------------
* Run the chat-server
    * command: `make run` (defaults to python, default port is 4711)
    * Running with different interpreters `make run PYTHON_INTERPRETER=python3`
    
* Run the chat-client
    * command: `make run HOST=127.0.0.1 PORT=4711`
    * Running with different interpreters `make run PYTHON_INTERPRETER=python3 PIP_INTERPRETER=pip3 HOST=127.0.0.1 PORT=4711`