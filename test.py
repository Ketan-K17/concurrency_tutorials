import collections
dq = collections.deque('123456')
print("Deque: {}".format(dq))
dq.rotate(3) # shift right
print("Deque: {}".format(dq))
dq.rotate(-2) # shift left
print("Deque {}".format(dq))