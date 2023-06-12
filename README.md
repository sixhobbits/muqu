# MuQu - Micro Queue

MuQu (pronounced Moo-Kyoo, an abbreviated form of microqueue or µq) is a very simple queue service, built as as an abstraction layer on top of AWS SQS. 

It is much more limited than SQS, but you will have to make fewer choices and won't have to mess around with permissions.

It is designed to create scalable architecture with the power of AWS SQS (unlimited storage), but without the complexity (no policies).

Every queue is FIFO. Every queue has an associated dead-letter queue where items go after too many failures. Every queue has a name. Everything that goes on the queue is in JSON format. 

You can have a server / producer putting work on a queue and worker taking items off the queue. To scale up, just add more worker processes (e.g. Python scripts with while True loops that perform "get" operations and run in TMUX panes on a $5 VPS).

## Set up

* Install the library with pip
* Create an IAM user
* Configure credentials

```python
import mu
muqu.connect(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY) # pass credentials in explicitly
```

## Create a queue

```python
# create a queue with a name
muqu.create("work_to_be_done")
```
## Put an item on the queue

```python
# prepare data
import json
d = {url: "https://google.com"}
data = json.dumps(d)

# add work to the queue
muqu.push("work_to_be_done", data)
```

## Get an item off the queue

```python
import json
data = muqu.get("work_to_be_done")
d = json.loads(data)
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

