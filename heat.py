# let's go to miami to catch the heat

# bst, but good
# classes are cancelled

def insert(data, tree, func, year):
	key, val = func(data)
	if not val:
		return
	# traverse
	while tree and key != tree[2]:
		tree = tree[key > tree[2]]
	if tree:
	# add value to key
		tree[3][year].add(val)
	elif not year:
	# add key to tree
		tree.extend([[],[], key, [{val},set()]])
		
def tolist(tree):
	if tree:
		# we have a two sets and want to add all pairs between sets
		l = [(one, two) for one in tree[3][0] for two in tree[3][1]]
		return tolist(tree[0]) + l + tolist(tree[1])
	return []

# file handling

# line to key
def get_kv(l):
	# we need the 13th column but quotes mix it up
	key, val, commas, quotes = "", "", 0, False
	for c in l:
		if c == '\"':
			quotes = not quotes
		elif c == ',' and not quotes:
			commas += 1
		elif commas == 13:
			key += c
		elif commas == 1 and (c.isupper() or c.isspace()):
			val += c
		elif commas == 14:
			# shorten val
			for f in ["FOR", "PRES", "AMER"]:
				if f in val:
					val = val[:val.find(f)]
			for r in ["FRIENDS OF", "COMMITTEE", "TO ELECT", "INC", "CAMPAIGN"]:
				val = val.replace(r,"")
			val.strip()
			return key, val

# make the dictionary
def getd():
	# csv -> bst
	csvs = ["2016_2700s.csv","2020_2800s.csv"]
	tree = []
	[insert(line, tree, get_kv, n) for n in [0,1] for line in open(csvs[n],"r")]
	
	# bst -> list
	dnrs = [donr for donr in tolist(tree) if all(donr)] # ensure donations both cycles
	
	# list -> dict
	sxtn, twnt = set([donr[0] for donr in dnrs]), set([donr[1] for donr in dnrs])
	d = { s : { t : 0 for t in twnt } for s in sxtn } # init to zero
	for donr in dnrs:
		d[donr[0]][donr[1]] += 1 # compute frequencies 
		
	# frequency -> log of log of frequency
	d = { s : { t : d[s][t].bit_length().bit_length() for t in twnt } for s in sxtn }
			
	return d

# we need a few imports to make the map

import pandas
import seaborn
import matplotlib.pyplot as plt

def heat():

	df = pandas.DataFrame.from_dict(getd())
	
	plt.rcParams['figure.figsize'] = [10, 10]
	plt.rcParams['figure.dpi'] = 100
	plt.tick_params(axis='both', which='major', labelsize=10, labelbottom = False, bottom=False, top = False, left = False, labeltop=True)
	plt.style.use("dark_background")
	
	p = seaborn.heatmap(df, cmap=seaborn.color_palette("mako", as_cmap=True))
	p.get_figure().savefig("heat.png",bbox_inches='tight',transparent=True)
	
heat()