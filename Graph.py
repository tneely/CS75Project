"""
File name: Graph.py
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


############
### CODE ###
############

##################
### NODE CLASS ###
class Node:

	def __init__(self, contents):
		self.contents = contents
		self.outgoing = []
		self.incoming = []

	def __getitem__(self, n):
		"""The nth adjacent node in
			the adjacents list
			Returns:
				Object: Node
		"""
		return self.adjacents[pos]

	def __len__(self):
		"""The number of adjacent nodes
			Returns:
				int
		"""
		return len(self.adjacents)

	def __str__(self):
		"""The contents of the node"""
		return self.contents

	def add_adj(self, other):
		"""Adds other nodes to 
			adjacent list of this
			node, and vice versa
		"""
		self.outgoing.append(other)
		other.incoming.append(self)
### NODE CLASS ###
##################

##################
### EDGE CLASS ###
class Edge:

	def __init__(self, node1, node2, contents = None):
		self.contents = contents
		self.adjacents = [node1, node2]
		self.visited = False

	def __getitem__(self, n):
		"""The nth adjacent node in
			the adjacents list [0,1]
			Returns:
				Object: Node
		"""
		return self.adjacents[n]

	def __len__(self):
		"""The number of adjacents
			Returns:
				int (2)
		"""
		return len(self.adjacents)

	def __str__(self):
		"""The contents of the edge"""
		return self.contents
### EDGE CLASS ###
##################

class Graph:

	def __init__(self):
		self.nodeList = []
		self.nodeDict = {} # lookup by contents
		self.edgeList = []
		self.edgeDict = {} # lookup by starting vert

	def __str__(self):
		"""Print out nodes and 
			their adjacents?
		"""
		out = ""
		for edge in self.edgeList:
			out = out + str(edge) + ": " + str(edge[0]) + ", " + str(edge[1]) + "\n"

		return out

	def new_node(self, contents):
		node = Node(contents)
		self.nodeList.append(node)
		self.nodeDict[contents] = node

		return node

	def new_edge(self, node1, node2, contents = None):
		edge = Edge(node1, node2, contents)
		self.edgeList.append(edge)
		node1.add_adj(node2)
		if node1 in self.edgeDict:
			self.edgeDict[node1].append(edge)
		else:
			self.edgeDict[node1] = [edge]

		return edge

	def get_unvisited(self, node):
		# check if node in dict (wont for last)
		if node not in self.edgeDict:
			return None
		# get edges for node
		edges = self.edgeDict[node]
		for edge in edges:
			if not edge.visited:
				return edge
		# couldn't find unvisited edge
		return None

	def del_node(self, node):
		nodeList.remove(node)

	def del_edge(self, edge):
		edgeList.remove(edge)

	def lookup(self, contents):
		return self.nodeDict[contents]