import json, os, sys

VERBOSE = False
if len(sys.argv)>1:
	print(sys.argv[1])
	VERBOSE = True


f = open('_environ.json')

var = json.load(f)

f.close()



os.environ.update(**var)

print('environment loaded:\n', var) if VERBOSE else None

