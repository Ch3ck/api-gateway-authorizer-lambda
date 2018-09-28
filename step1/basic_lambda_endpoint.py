from __future__ import print_function

import json

print('Loading basic lambda endpoint')


def lambda_handler(event, context):
	try:
		print("Hello world!")
		print("value1 = " + event['key1'])
		print("value2 = " + event['key2'])
		print("value3 = " + event['key3'])

		return event['key1']  # Echo back the first key value
	except:
		print('Something went wrong')
		return None