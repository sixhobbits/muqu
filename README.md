# MuQu - Micro Queue

MuQu (pronounced Moo-Kyoo, an abbreviated form of microqueue or µq) is a very simple queue service, built as as an abstraction layer on top of AWS SQS. 

It is much more limited than SQS, but you will have to make fewer choices and won't have to mess around with permissions.

It is designed to create scalable architecture with the power of AWS SQS (unlimited storage), but without the complexity (no policies).

Every queue is FIFO. Every queue has an associated dead-letter queue where items go after too many failures. Every queue has a name. Everything that goes on the queue is JSON, but you interact with them mainly as Python dictionaries.

You can have a server / producer putting work on a queue and worker taking items off the queue. To scale up, just add more worker processes (e.g. Python scripts with while True loops that perform "get" operations and run in TMUX panes on a $5 VPS).

## Set up

* Install the library with pip
* Create an IAM user
* Configure credentials

## Usage

The code below creates a queue, pushes an item to it, gets the item off it, and deletes the queue.

Usually, you would create the queue once-off, push items onto the queue from your server code and get/remove items with one or more worker scripts.

```python
from muqu import MuQu

# for demo purposes only
# rather grab them from environment variables or a .env file
aws_access_key_id = ""
aws_secret_access_key = ""

muqu = MuQu(aws_access_key_id, aws_secret_access_key)

queue_name = "test-queue-3"
muqu.create_queue(queue_name)

d = {"message": "hello"}

muqu.push(queue_name, d)
m = muqu.fetch(queue_name)
print("got message")
print(m["data"])
if m:
    muqu.remove(queue_name, m)
muqu.delete_queue(queue_name)
```

## Create a queue

```python
# create a queue with a name
muqu.create("my-queue")
```
## Put an item on the queue

```python
data = {"url": "https://google.com"}
muqu.push("my-queue", data)
```

## Get an item off the queue

```python
data = muqu.get("my-queue")
```

## Delete an item from the queue
muqu.delete(data)

## Peek at a queue

```python
# get an item but immediately make it visible to real workers again
data = muqu.peek("work_to_be_done")
```

## Delete a queue

```python
# delete the queue, not data from it
muqu.delete("work_to_be_done")
```

