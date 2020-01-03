HOST=127.0.0.1
PORT=4711
PYTHON_INTERPRETER=python
PIP_INTERPRETER=pip

install:
	$(PYTHON_INTERPRETER) setup.py --pip $(PIP_INTERPRETER)

run:
	$(PYTHON_INTERPRETER) chat-client.py --ip-address $(HOST) --port $(PORT)
