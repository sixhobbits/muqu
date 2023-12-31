from muqu import MuQu

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

