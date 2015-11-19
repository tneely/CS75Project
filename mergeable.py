__author__ = 'laurenmitchell'

"""
Edge - in_node, out_node, seq - str, reads - list
Node - inEdges - list, outEdges - lis, seq - str

"""
def is_mergeable(x, y): #x is an edge1, y is edge2
    for in_node in x.in_nodes: # if x is a curl edge, but don't wanna count it if there are still others
        for out_node in x.out_nodes:
            if in_node == out_node:
                return False
    for in_node in y.in_nodes: #if y is a curl edge
        for out_node in y.out_nodes:
            if in_node == out_node:
                return False
    freqDictx = {}
    freqDicty = {}
    for read in x.reads:
        if freqDictx.has_key(read.name):
            freqDictx[read.name] += 1
        else:
            freqDictx[read.name] = 1
    for read in y.reads:
        if freqDicty.has_key(read.name):
            freqDicty[read.name] += 1
        else:
            freqDicty = 1
    for read in freqDictx:
        if freqDictx[read.name] != freqDicty[read.name]:#if the number of a certain read in x does not equal amount for same read in y
            return False
    for read in x.reads: #if a path starts in x
        if x == read[0]:
            return False
    return True
