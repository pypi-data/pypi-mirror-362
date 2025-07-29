Codicent Python Library
=======================

This library provides a Python interface to the Codicent API.

### Installation
------------
To install using pip, run:
```bash
pip install git+https://github.com/izaxon/codicent-py.git
```

To use this library, simply import it into your Python script:
```python
from codicentpy import Codicent
```

### Usage
-----

### Initialization

Create a `Codicent` object with your API token and optional SignalR host:
```python
codicent = Codicent("YOUR_API_TOKEN")
```
### Uploading a file

Upload a file to Codicent:
```python
file_id = codicent.upload(open("example.txt", "rb"))
print(file_id)
```
### Posting a message

Post a message to Codicent:
```python
message_id = codicent.post_message("Hello, world!", type="info")
print(message_id)
```
### Getting messages

Get a list of messages from Codicent:
```python
messages = codicent.get_messages(start=0, length=10)
print(messages)
```

### Get AI chat reply

Sends a message to the Codicent chat (AI) and waits for the reply:
```python
reply = codicent.get_chat_reply("What can you help me with?")
print(reply)
```


Methods
-------

### `__init__`

Initialize the `Codicent` object with a Codicent API token.

### `upload`

Upload a file to Codicent.

* `file`: The file to upload.

Returns the ID of the uploaded file.

### `post_message`

Post a message to Codicent.

* `message`: The message to post.
* `parent_id`: The ID of the parent message (optional).
* `type`: The type of message (default: "info").

Returns the ID of the posted message.

### `get_messages`

Get a list of messages from Codicent.

* `start`: The starting index (default: 0).
* `length`: The number of messages to retrieve (default: 10).
* `search`: A search query (optional).
* `after_timestamp`: A timestamp to retrieve messages after (optional).
* `before_timestamp`: A timestamp to retrieve messages before (optional).

Returns a list of message objects.

### `get_chat_reply`

Sends a message to the Codicent chat (AI) and waits for the reply.

* `message`: The message to send.

### `post_chat_reply`

Posts a message to the Codicent AI chat and returns the reply.

* `message`: The message to send.

Returns a dictionary with:
  - id: The message ID.
  - content: The reply message content.

### Running Tests
To run tests, first install the required dependencies:
```bash
pip install -r requirements.txt
```
Then execute:
```bash
pytest
```

### Building
To build the package, run:
```bash
python setup.py sdist bdist_wheel
```
