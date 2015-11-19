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

	def __init__(self, sequence):
		self.sequence = sequence
		self.inEdges = []
		self.outEdges = []

	def __getitem__(self, n):
		"""The nth letter in the
			sequence
			Returns:
				String
		"""
		return self.sequence[pos]

	def __len__(self):
		"""The length of the sequence
			Returns:
				int
		"""
		return len(self.sequence)

	def __str__(self):
		"""The contents of the node"""
		return self.sequence

	def add_outgoing(self, other, edge):
		"""Adds other nodes to 
			adjacent list of this
			node, and vice versa
		"""
		self.outEdges.append(edge)
		other.inEdges.append(edge)
### NODE CLASS ###
##################

##################
### EDGE CLASS ###
class Edge:

	def __init__(self, inNode, outNode, sequence):
		self.sequence = sequence
		self.inNode = inNode
		self.outNode = outNode
		self.reads = []
		self.visited = False

	def __getitem__(self, n):
		"""The nth letter in
			the sequence
			Returns:
				String
		"""
		return self.sequence[n]

	def __len__(self):
		"""The number of adjacents
			Returns:
				int
		"""
		return len(self.sequence)

	def __str__(self):
		"""The contents of the edge"""
		return self.sequence
### EDGE CLASS ###
##################

##################
### READ CLASS ###
class Read:

	def __init__(self, sequence, idnum):
		self.sequence = sequence
		self.id = idnum
		self.edges = []

	def __getitem__(self, n):
		"""The nth edge in
			the edge list
			Returns:
				edge
		"""
		return self.edges[n]

	def change_x(self, x, z):
		"""Changes the last edge in edges
			to new z edge if x is that last edge
			Adjusts edges involved
			Returns:
				True if changed, false otherwise
		"""
		if self.edges[-1] == x:
			self.edges[-1] = z
			#add read to new edge
			z.reads.append(self)
			#remove read from edge
			x.reads.remove(self)
			return True
		return False

	def change_y(self, y, z):
		"""Changes the first edge in edges
			to new z edge if y is that first edge
			Adjusts edges involved
			Returns:
				True if changed, false otherwise
		"""
		if self.edges[0] == y:
			self.edges[0] = z
			#add read to new edge
			z.reads.append(self)
			#remove read from edge
			y.reads.remove(self)
			return True
		return False

	def change_xy(self, x, y, z):
		"""Changes consecutive x,y edges in path.
			Adjusts edges involved
			Returns:
				True if changed, false otherwise
		"""
		foundXY = False
		# look for all xy pairs
		for i in range(len(self.edges)-1):
			# if pair found...
			if self.edges[i] == x and self.edges[i+1] == y:
				foundXY = True
				# add z, remove x,y
				self.edges[i] == z
				del self.edges[i+1]
				#add read to new edge
				z.reads.append(self)
				#remove read from edge
				x.reads.remove(self)
				y.reads.remove(self)

		return foundXY

	def update(self, x, y, z):
		"""Runs all change functions
			Adjusts edges involved
			Returns:
				True if any changed, false otherwise
		"""
		# compute each separately to avoid short circuit
		changed = [self.change_xy(x,y,z), self.change_x(x,z), self.change_y(y,z)]
		# return if any changed
		return any(changed)
### READ CLASS ###
##################
class Graph:

	def __init__(self, seqs, k):
		"""Takes reads from Loader and kmer 
			length to initialize deBruijn Graph
		"""
		self.nodeList = []
		self.nodeDict = {} # lookup by contents
		self.edgeList = []
		self.edgeDict = {} # lookup by contents
		self.readList = []

		for s in range(len(seqs)):
			#get seq
			seq = seqs[s]
			# make read
			read = Read(seq, s)
			self.readList.append(read)
			# make edges and nodes
			for i in range(len(seq)-k+1):
				#get info
				kmer = seq[i:i+k]
				prefix = kmer[:k-1]
				suffix = kmer[1:]
				# get/create prefix node
				if prefix in self.nodeDict:
					pNode = self.nodeDict[prefix]
				else:
					pNode = self.new_node(prefix)
				# get/create suffix node
				if suffix in self.nodeDict:
					sNode = self.nodeDict[suffix]
				else:
					sNode = self.new_node(suffix)
				# get/create edge
				if kmer in self.edgeDict:
					edge = self.edgeDict[kmer]
				else:
					edge = self.new_edge(pNode, sNode, kmer)
				# expand read path
				read.edges.append(edge)
				# expand edge reads
				edge.reads.append(read)


	def __str__(self):
		"""Print out nodes and 
			their adjacents?
		"""
		out = ""
		for edge in self.edgeList:
			out = out + str(edge) + ": " + str(edge.inNode) + ", " + str(edge.outNode) + "\n"

		return out

	def new_node(self, sequence):
		node = Node(sequence)
		self.nodeList.append(node)
		self.nodeDict[sequence] = node

		return node

	def new_edge(self, inNode, outNode, sequence):
		edge = Edge(inNode, outNode, sequence)
		self.edgeList.append(edge)
		inNode.add_outgoing(outNode, edge)
		self.edgeDict[sequence] = edge

		return edge

	"""UNSURE IF THIS STILL WORKS"""
	def get_unvisited(self, node):
		# get edges for node
		for edge in node.outEdges:
			if not edge.visited:
				return edge
		# couldn't find unvisited edge
		return None

	def merge(self, x, y):
		"""Merges two adjacents
			edges, x and y.
		"""
		#get nodes involved
		inNode = x.inNode
		midNode = x.outNode
		outNode = y.outNode
		# sanity check
		if inNode == outNode:
			print x, y
			print inNode, outNode
		#make sure nodes are still live
		if len(inNode.outEdges) == 0 or len(midNode.inEdges) == 0 or \
			len(midNode.outEdges) == 0 or len(outNode.inEdges) == 0:
			return None
		#get new sequence for edge
		seq = x.sequence + y.sequence[-1]
		#create new edge
		z = self.new_edge(inNode, outNode, seq)
		#update nodes, paths
		inNode.outEdges.remove(x)
		midNode.inEdges.remove(x)
		midNode.outEdges.remove(y)
		outNode.inEdges.remove(y)
		for read in self.readList:
			read.update(x,y,z)

		return z

	def is_mergeable(self, x, y, skipCurls): #x is an edge1, y is edge2
		#skip curl edges
		# if skipCurls:
		# 	for read in self.readList:
		# 		freqs = {x:0, y:0}
		# 		for edge in read.edges:
		# 			if edge in freqs:
		# 				freqs[edge] += 1
		# 		if freqs[x] > 1 or freqs[y] > 1:
		# 			print "oops"
		# 			return False
		freqDictx = {}
		freqDicty = {}
		for read in x.reads:
			if freqDictx.has_key(read.id):
				freqDictx[read.id] += 1
			else:
				freqDictx[read.id] = 1
		for read in y.reads:
			if freqDicty.has_key(read.id):
				freqDicty[read.id] += 1
			else:
				freqDicty[read.id] = 1
		for idnum in freqDictx:
			if idnum in freqDicty and freqDictx[idnum] != freqDicty[idnum]:#if the number of a certain read in x does not equal amount for same read in y
				return False
		for read in x.reads: #if a path starts in x
			if x == read[0]:
				return False
		return True

	def clean(self):
		"""Removes stray edges and 
			nodes from the graph.
		"""
		#remove empty nodes
		toRemove = []
		for node in self.nodeList:
			if len(node.inEdges) == 0 and len(node.outEdges) == 0:
				toRemove.append(node)
		#remove
		for node in toRemove:
			self.nodeList.remove(node)

		#remove empty edges
		toRemove = []
		for edge in self.edgeList:
			if len(edge.reads) == 0:
				toRemove.append(edge)
			elif edge.inNode not in self.nodeList:
				toRemove.append(edge)
			elif edge.outNode not in self.nodeList:
				toRemove.append(edge)
		#remove
		for edge in toRemove:
			self.edgeList.remove(edge)