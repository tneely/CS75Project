"""
File name: Assembler.py
Info: CS75 Final Project
Authors: Stephanie Her, Lauren Mitchell, 
		Taylor Neely, and Erin Connolly
Date created: 30/10/2015
Date last modified: 30/10/2015
Python version: 2.7
"""

###############
### IMPORTS ###
###############
from Graph import Graph
from Loader import Loader

############
### CODE ###
############
class Assembler:
	
	def __init__(self, filename, k):

		self.graph = Graph()

		#loads file and REMOVES ANY REPEATS
		reads = Loader.load(filename)
		# create set of possible nodes
		nodeSet = set()
		for read in reads:
			for i in range(len(read)-(k-1)+1):
				nodeSet.add(read[i:i+(k-1)])
		# create nodes
		for kmer in nodeSet:
			self.graph.new_node(kmer)
		# create edges
		for read in reads:
			for i in range(len(read)-k+1):
				kmer = read[i:i+k]
				if kmer[:k-1] in nodeSet and kmer[1:] in nodeSet:
					node1 = self.graph.lookup(kmer[:k-1])
					node2 = self.graph.lookup(kmer[1:])
					self.graph.new_edge(node1, node2, kmer)

# Command-line driver for assembly
if __name__ == '__main__':
	filename = argv[1]
	k = argv[2]
	assembly = Assembler(filename, k)
	assembly.assemble()