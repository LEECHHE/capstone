import argparse
from k2 import K2
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--dataset", help="path of dataset", type=str, dest='dataset')
	parser.add_argument("--delimiter", help="delimiter of input file", default=',', dest='delimiter')
	args = parser.parse_args()
	
	if not args.dataset:
		print("Invalid path : "+path)
		sys.exit(0)
	k2 = K2(args)
	k2.run()

