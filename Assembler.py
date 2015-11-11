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

		#loads file
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
					node1 = self.graph.lookup(kmer[:k-1]) #prefix
					node2 = self.graph.lookup(kmer[1:]) #suffix
					edge = self.graph.new_edge(node1, node2, kmer)

	def eulerian_path(self):
		"""Constructs a eulerian
			path on the graph using
			Heirholzer's algorithm
		"""
		# init
		currentPath = []
		finalPath = []
		print self.graph.nodeDict["AT"]
		edge = self.graph.get_unvisited(self.graph.nodeDict["AT"])
		# add all edges to stack in linear fashion
		while edge != None:
			edge.visited = True
			currentPath.append(edge)
			edge = self.graph.get_unvisited(edge[1]) # next node/edge
		# get all other unvisted and construct final path
		while len(currentPath) > 0:
			edge = currentPath.pop()
			finalPath.append(edge)
			edge = self.graph.get_unvisited(edge[0]) # previous node/edge
			# loop for unvisited edges again
			while edge != None:
				edge.visited = True
				currentPath.append(edge)
				edge = self.graph.get_unvisited(edge[1]) # next node/edge

		# print result by appending to front
		sequence = ''
		while len(finalPath) > 0:
			edge = finalPath.pop()
			if len(finalPath) == 0: # last edge
				sequence += edge.contents # add all
			else:
				sequence += edge.contents[0] # add first only

		return sequence





# Command-line driver for assembly
if __name__ == '__main__':
	filename = argv[1]
	k = argv[2]
	assembly = Assembler(filename, k)
	assembly.assemble()