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
class Graph:

##################
### NODE CLASS ###
	class Node:

		def __init__(self, contents, adjacents = None): # Not sure what the best way to track adj is, within node or in edge class?
			self.contents = contents
			self.adjacents = adjacents

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
	    	self.adjacents.append(other)
	    	other.adjacents.append(self)
### NODE CLASS ###
##################

##################
### EDGE CLASS ###
	class Edge:

		def __init__(self, contents = None, node1, node2):
			self.contents = contents
			self.adjacents = [node1, node2]

		def __getitem__(self, n):
	        """The nth adjacent node in
	        	the adjacents list [0,1]
	        Returns:
	          Object: Node
	        """
	        return self.adjacents[pos]

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

    def __init__(self):
        self.nodeList = []
        self.edgeList = []
        
    def __str__(self):
    	"""Print out nodes and 
    		their adjacents? 
    	"""
    	pass

    def new_node(self, contents, adjacents = None):
    	node = Node(contents, adjacents)
    	self.nodeList.append(node)

    	return node

    def new_edge(self, contents = None, node1, node2):
    	edge = Edge(contents, node1, node2)
    	self.edgeList.append(edge)

    	return edge

    def del_node(self, node):
    	nodeList.remove(node)

    def del_edge(self, edge):
    	edgeList.remove(edge)