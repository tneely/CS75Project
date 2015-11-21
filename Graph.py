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
from copy import *
from math import *

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
        return self.sequence[n]

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
            if self in x.reads:
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
            if self in y.reads:
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
                self.edges[i] = z
                self.edges[i+1] = None
                #add read to new edge
                z.reads.append(self)
                #remove read from edge
                if self in x.reads:
                    x.reads.remove(self)
                if self in y.reads:
                    y.reads.remove(self)
        #remove edges where edge = none
        self.edges = [x for x in self.edges if x != None]

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

    def __init__(self, seqs, k, threshold=5):
        """Takes reads from Loader and kmer
            length to initialize deBruijn Graph
        """
        self.nodeList = []
        self.nodeDict = {} # lookup by contents
        self.edgeList = []
        self.edgeDict = {} # lookup by contents
        self.readList = []
        self.k = k
        self.seqs = seqs
        self.threshold = threshold #for error correction
        self.correctedseqs, self.kmers = self.error_correct(self.threshold)

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
        #make sure nodes are still live
        if len(inNode.outEdges) == 0 or len(midNode.inEdges) == 0 or \
            len(midNode.outEdges) == 0 or len(outNode.inEdges) == 0:
            return None
        #get new sequence for edge
        yLen = len(y.sequence)
        seq = x.sequence + y.sequence[self.k-1:]
        #create new edge
        z = self.new_edge(inNode, outNode, seq)
        #update nodes, paths
        if x in inNode.outEdges:
            inNode.outEdges.remove(x)
        if x in midNode.inEdges:
            midNode.inEdges.remove(x)
        if y in midNode.outEdges:
            midNode.outEdges.remove(y)
        if y in outNode.inEdges:
            outNode.inEdges.remove(y)
        for read in self.readList:
            read.update(x,y,z)

        return z

    def is_mergeable(self, p, x, y): #x is an edge1, y is edge2, p is preceding edge
        isSpanned = False
        for read in x.reads:
            if read in y.reads:
                isSpanned = True
        # is there a read that contains conflicting information?
        isConflicted = False
        for read in x.reads:
            #starting from preceding, follow path
            for i in range(len(read.edges)-2):
                #look for x
                if read.edges[i] == x:
                    #matching start
                    if (p == None and i == 0) or p == read.edges[i-1]:
                        #conflicting end
                        if y != read.edges[i+1]:
                            isConflicted = True
                    #conflicting start
                    else:
                        #matching end
                        if y == read.edges[i+1]:
                            isConflicted = True

            return isSpanned and not isConflicted

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

    def error_correct(self, threshold):
        """Corrects the reads and saves them in the graph
        """
        list_sequences = []
        freqdict = {}
        for read in self.seqs:
            one_sequence_kmers = []
            for i in range(len(read)-(self.k)+1):
                # print read[i:i+(self.k)]
                one_sequence_kmers.append(read[i:i+(self.k)])
                #add the occurances to the dictionary
                if read[i:i+(self.k)] not in freqdict:
                    freqdict[read[i:i+(self.k)]] = 1
                else:
                    freqdict[read[i:i+(self.k)]] += 1
            list_sequences.append(one_sequence_kmers)

        seqlist = deepcopy(list_sequences)
        #loop through the reads of the list sequence
        for read in seqlist:
        #for every kmer in each list
            for i in range(len(read)):
                kmer = read[i]
        #look up in the freqdict and check if occurences is greater than or equal to threshold
                ocurrences = freqdict[kmer]
                if ocurrences < threshold:
        #if its less, loop to the next k-1 kmers and check if they are also less than threshold
        #if k/2 of those kmers are also below threshold, need to change something, otherwise just keep it
                    cutoff = ceil((len(kmer)/2.0))
                    #print cutoff
                    for j in range(len(kmer)):#loop through k-1 kmers after it
                        if i+j >= len(read):
                            break
                        if freqdict[read[i+j]] < threshold:
                            cutoff -= 1
            #if too many neighbors are all under the threshold, need to find a way to change something
                        #print cutoff
                        if cutoff <= 0:
                            choices = ["A", "C", "G", "T"]
                            bestScore = 0
                            indexToChange = -1 #index within the kmer that needs to be changed
                            kmersToChange = -1 #first kmer that needs to be changed
                            letter = -1 #index of letter to be switched to in choices

                            #only loop through second half of the letters in the kmer
                            for x in range(int(ceil(len(kmer)/2.0))): #is this that you are checking to see which letter
                                # we are not just always gonna pick the last one?
                                index = -1 - x
                                #print index
                                #keep track of scores of substituting each letter
                                scores = [0, 0, 0, 0]
                                for y in range(len(kmer) - x):
                                    #print x, y
                                    #loop through the kmers that also include the letter to compare scores
                                    kmerIndex = (i) + y # i is index of kmer, x is letter choice, y is continuous after kmer
                                    #print kmerIndex #used to be i-x + y
                                    # wait is this so that you backtrack so it is at the end? if so brilliant
                                    if kmerIndex >= len(read) or kmerIndex < 0:
                                        continue
                                    for n in range(len(choices)):
                                        option = str(read[kmerIndex])
                                        #print option
                                        optionlist = list(option)
                                        new_index = index - y # used to have a -x
                                        if new_index < -len(kmer):
                                            new_index += len(kmer)
                                        optionlist[new_index] = choices[n] #index - y
                                        optionsbacktostring = ''.join(optionlist)
                                        option = optionsbacktostring
                                        #print option
                                        #option = option.replace(option[index], choices[n])
                                        if option in freqdict:
                                            #add in the differences of occurances for the replacement and original
                                            scores[n] += (freqdict[option] - freqdict[read[kmerIndex]])
                                        #????? how should we deal with things not even in the dictionary??
                                        else:
                                            scores[n] -= 10
                                #for that letter in the original kmer, change it if the score of a certain combo is best
                                #print scores

                                for n in range(len(scores)):
                                    if scores[n] > bestScore:
                                        bestScore = scores[n]
                                        #print bestScore
                                        indexToChange = len(kmer) - 1 - x
                                        kmersToChange = (i-x)#first one to change - index is len
                                        #print kmersToChange
                                        letter = n
                            if bestScore == 0:
                                #the original is still the best option, keep it
                                continue
                            else:
                                #change the kmer if need be
                                for p in range(len(kmer)): #changed to -x
                                    if (p + kmersToChange) < len(read):
                                        #print p + kmersToChange
                                        #print read[kmersToChange + p]
                                        freqdict[read[kmersToChange + p]] -= 1
                                        listofkmer = list(read[kmersToChange + p])
                                        listofkmer[-(p + 1)] = choices[letter] # -(p+1)
                                        backtostring = ''.join(listofkmer)
                                        read[kmersToChange + p] = backtostring
                                        if freqdict.has_key(read[kmersToChange + p]):
                                            freqdict[read[kmersToChange + p]] += 1
                                        else:
                                            freqdict[read[kmersToChange + p]] = 1
                                    #read[kmersToChange + p] = read[kmersToChange + p].replace(read[kmersToChange + p][-p], choices[letter])
                                        #print read[kmersToChange + p]
        return seqlist, list_sequences

def results(original, start, end): #list of lists
    total_kmers = 0.0
    originalerrors = 0.0
    correctederrors = 0.0
    introducederrors = 0.0
    innacuratecorrection = 0.0
    for i in range(len(original)):
        for j in range(len(original[i])):
            total_kmers += 1
            original_kmer = original[i][j]
            start_kmer = start[i][j]
            end_kmer = end[i][j]
            print original_kmer != start_kmer
            print original_kmer, start_kmer
            if original_kmer != start_kmer:
                originalerrors += 1
                if original_kmer == end_kmer:
                    correctederrors += 1
                else:
                    innacuratecorrection += 1
            if original_kmer != end_kmer and original_kmer == start_kmer:
                introducederrors += 1
    print "Percent original errors:"
    print originalerrors, originalerrors/total_kmers * 100
    print "Percent corrected:"
    print correctederrors, correctederrors/originalerrors * 100
    print "Introduced errors:"
    print introducederrors, introducederrors/total_kmers * 100
    print "Inaccurate correction:"
    print innacuratecorrection, innacuratecorrection/originalerrors * 100






