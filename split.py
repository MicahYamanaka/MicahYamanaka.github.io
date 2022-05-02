thecsv = "2020_2800s.csv"
splits = 2

def split():
	countr = 0
	out_fs = [open(thecsv.replace(".csv", "_" + str(i) + ".csv"),"w") for i in range(splits)]
	for line in open(thecsv,"r"):
		out_fs[countr].write(line)
		countr = (countr + 1) % splits

def combine():
	countr = 0
	in__fs = [open(thecsv.replace(".csv", "_" + str(i) + ".csv"),"r") for i in range(splits)]
	out_f_ = open(thecsv,"w")
	for f in in__fs:
		for line in f:
			out_f_.write(line)

combine()