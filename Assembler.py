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
from Graph import *
from Loader import Loader
import sys

############
### CODE ###
############
class Assembler:
    def __init__(self, filename, k):

        #loads file
        reads = Loader.load(filename)
        #gets graph
        self.graph = Graph(reads, k)
        self.k = k

    def make_superpath(self):
        """loops to make superpaths in graph"""
        # try without curls
        while self.superpath_helper(True):
            self.graph.clean()
        # try with curls
        # while self.superpath_helper(False):
        #     self.graph.clean()
        self.graph.clean()

    def superpath_helper(self, linear):
        """Does actual merging"""
        for read in self.graph.readList:
            for i in range(len(read.edges)-1):
                #get preceding if possible
                if i > 0:
                    p = read.edges[i-1]
                else:
                    p = None
                #get x,y
                x = read.edges[i]
                y = read.edges[i+1]
                #check if edges can be merged
                if self.graph.is_mergeable(p,x,y,linear):
                    #make sure merge worked
                    if self.graph.merge(x,y):
                        return True

        return False

    def is_eulerian(self):
        """Checks whether or not the graph is eulerian"""
        # count semi-balanced nodes (|indegree - outdegree| = 1)
        semis = 0
        for node in self.graph.nodeList:
            diff = abs(len(node.outgoing)-len(node.incoming))
            # if not balanced or semi-balanced, it is not euler
            if diff > 1:
                return False
            elif diff == 1:
                semis += 1
        # not eulerian if more than 2 semi-balanced nodes
        if semis > 2:
            return False

        return True

    def balance(self):
        """Connects semi-balanced nodes to eachother
            This function only works if the graph is eulerian!
            Returns False if failed. Returns True on success.
        """
        # find unbalanced nodes
        semis = []
        for node in self.graph.nodeList:
            diff = abs(len(node.outgoing)-len(node.incoming))
            if diff == 1:
                semis += [node]
        # can we do it?
        if len(semis) != 2:
            print("Too many unbalanced: %i. The graph is not eulerian.")%len(semis)
            return False
        # find balance
        if len(semis[0].incoming) > len(semis[0].outgoing): # e.g. needs an outgoing to balance
            # 0 -> 1
            self.graph.new_edge(semis[0], semis[1], semis[0].contents)
        else:
            # 1 -> 0
            self.graph.new_edge(semis[1], semis[0], semis[1].contents)
        # balance found
        return True


    def eulerian_path(self):
        """Constructs a eulerian
            path on the graph using
            Heirholzer's algorithm
        """
        # init
        currentPath = []
        finalPath = []
        # try to start on semi-balanced with less incoming
        edge = None
        for node in self.graph.nodeList:
            diff = abs(len(node.outEdges)-len(node.inEdges))
            if diff == 1 and len(node.inEdges) < len(node.outEdges):
                edge = self.graph.get_unvisited(node)
        # just pick first if failed
        if not edge: edge = self.graph.get_unvisited(self.graph.nodeList[0])
        # add all edges to stack in linear fashion
        while edge != None:
            edge.visited = True
            currentPath.append(edge)
            edge = self.graph.get_unvisited(edge.outNode) # next node/edge
        # get all other unvisted and construct final path
        while len(currentPath) > 0:
            edge = currentPath.pop()
            finalPath.append(edge)
            edge = self.graph.get_unvisited(edge.inNode) # previous node/edge
            # loop for unvisited edges again
            while edge != None:
                edge.visited = True
                currentPath.append(edge)
                edge = self.graph.get_unvisited(edge.outNode) # next node/edge

        # print result by appending to front
        sequence = ''
        while len(finalPath) > 0:
            edge = finalPath.pop()
            if len(finalPath) == 0: # last edge
                sequence += edge.sequence # add all
            else:
                sLen = len(edge.sequence)
                sequence += edge.sequence[:sLen-self.k+1] # add first only

        return sequence


def test(filename, k):
    assembly = Assembler(filename, int(k))
    assembly.make_superpath()
    print assembly.graph
    assembly.eulerian_path()

def test_errorcorrection(filename, badfilename, k, threshold):
    reads = Loader.load(filename)
    graph = Graph(reads, k)
    reads2 = Loader.load(badfilename)
    grapherrors = Graph(reads2, k, threshold)
    results(graph.kmers, grapherrors.kmers, grapherrors.correctedseqs)

#test("data/simple.fastq", 6)
test_errorcorrection("data/hemoglobin.fastq", "data/hemoglobin.fastq", 3, 4)


#Command-line driver for assembly
if __name__ == '__main__':
    filename = sys.argv[1]
    k = sys.argv[2]
    assembly = Assembler(filename, int(k))
    assembly.make_superpath()
    # print assembly.graph
    print assembly.eulerian_path()