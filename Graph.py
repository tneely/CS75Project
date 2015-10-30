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

		def __init__(self, contents, adjacents = None):
			self.contents = contents
			self. adjacents = adjacents

		def __getitem__(self, n):
	        """The nth adjacent node in
	        	the adjacents list
	        Returns:
	          Object: Node
	        """
	        return self.adjacents[pos]

	    def __len__(self):
	        """The number of adjacents
	        Returns:
	          int
	        """
	        return len(self.adjacents)

	    def __str__(self):
	        """The contents of the node"""
	        return self.contents
### NODE CLASS ###
##################

    def __init__(self, stuff):
        self.stuff = stuff
        
    def __str__(self):
    	"""Print out nodes and 
    		their adjacents? 
    	"""