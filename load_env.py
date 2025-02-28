import json, os, sys


def main(verbose=False):
	f = open('_environ.json')

	var = json.load(f)

	f.close()

	os.environ.update(**var)

	if verbose:
		print('environment loaded:\n', var) 


if __name__ == '__main__':

	VERBOSE = None
	if len(sys.argv)>1:
		print(sys.argv[1])
		VERBOSE = True
		
	main(VERBOSE)
