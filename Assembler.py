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

class ListNode:

	def __init__(self, content = None, next=None, last=None):
		self.content = content
		self.next = next
		self.last = last



class DLL:

	def __init__(self):
		self.sentinel = ListNode
		self.sentinel.next = self.sentinel
		self.sentinel.last = self.sentinel

	def append(node):
		node.last = self.sentinel.last
		node.next = self.sentinel
		self.sentinel.last.next = node
		self.sentinel.last = node

	def remove(node):
		node.last.next = node.next
		node.next.last = node.last

	def insert(node1, node2):
		"""Places node1 after node2"""
		node1.last = node2
		node1.next = node2.next
		node2.next.last = node1
		node2.next = node1

	def pop():
		"""Removes first node from DLL
			Returns:
				ListNode
		"""
		node = self.sentinel.next
		self.sentinel.next = node.next
		node.next.last = self.sentinel

		return node


class Assembler:
	
	def __init__(self, filename, k):

		self.graph = Graph()
		self.dll = DLL()

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
					self.dll.append(ListNode(kmer))

	def eulerian_path(self):
		"""Constructs a eulerian
			path on the graph using
			Heirholzer's algorithm
		"""
		edge = self.dll.pop()
		start = edge[0]
		next = edge[1]

		# loop until cycle back
		while next != start:




# Command-line driver for assembly
if __name__ == '__main__':
	filename = argv[1]
	k = argv[2]
	assembly = Assembler(filename, k)
	assembly.assemble()