#!/usr/bin/python3
import sys
processing = __import__('1-batch_processing')

try:
    users = processing.batch_processing(50)
    for user in users:
        print(user)
except BrokenPipeError:
    sys.stderr.close()
