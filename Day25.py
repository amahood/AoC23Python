"""
Potential Approach:
- Build up list of all edges - DONE
- Build algo make graph from edges - DONE
- BUild BFS to find number of cells each cell can get to 
- Run all the above by removing 3 different edges, but number of combinations is going to be too high, something 3^
"""

import copy

class edge:
    def __init__(self, left, right):
        self.left = left
        self.right = right

class node:
    def __init__(self, name):
        self.name = name
        self.neighbors = set()

def build_graph_from_edges(edges):
    nodes = set()
    for e in edges:
        #Check if a node exists for left, if not create it and add an edge to right
        nodes_for_left = list(filter(lambda x: x.name == e.left, nodes))
        if len(nodes_for_left) == 0:
            new_node = node(e.left)
            new_node.neighbors.add(e.right)
            nodes.add(new_node)
        else:
            nodes_for_left[0].neighbors.add(e.right)
        
        #Check if a node exists for right, if not create it and add an edge to left
        nodes_for_right = list(filter(lambda x: x.name == e.right, nodes))
        if len(nodes_for_right) == 0:
            new_node = node(e.right)
            new_node.neighbors.add(e.left)
            nodes.add(new_node)
        else:
            nodes_for_right[0].neighbors.add(e.left)
    return nodes

def find_number_of_connected_nodes(nodes, start_node):
    visited_set = set()
    frontier = set()
    frontier.add(start_node)
    while len(frontier) > 0:
        current_node_name = frontier.pop()
        current_node = list(filter(lambda x: x.name == current_node_name, nodes))[0]
        visited_set.add(current_node_name)
        for n in current_node.neighbors:
            if n not in visited_set:
                frontier.add(n)
    return len(visited_set)

f = open("Day25TestInput.txt")
#f = open("Day25Input.txt")

edges = set()

#Read in input and create edges for all connections
for l in f:
    temp = l.split(':')
    temp_r = temp[1].strip()
    temp_r = temp_r.split(' ')

    for r in temp_r:
        new_edge = edge(temp[0], r)
        edges.add(new_edge)
 
print("Number of edges = " + str(len(edges)))

looper = 0
found_halver = False
for i in range(len(edges)):
    for j in range(i+1, len(edges)):
        for k in range(j+1, len(edges)):
            #Remove 3 edges
            edgecopy = copy.deepcopy(edges)

            
            #node1 = str(list(edgecopy)[i].left) + "/" + str(list(edgecopy)[i].right)
            #edgecopy.remove(list(edgecopy)[i])
            #node2 = str(list(edgecopy)[j-1].left) + "/" + str(list(edgecopy)[j-1].right)
            #edgecopy.remove(list(edgecopy)[j-1])
            #node3 = str(list(edgecopy)[k-2].left) + "/" + str(list(edgecopy)[k-2].right)
            #edgecopy.remove(list(edgecopy)[k-2])
            
            edgecopy.remove(list(filter(lambda x: x.left == 'pzl' and x.right == 'hfx', edgecopy))[0])
            edgecopy.remove(list(filter(lambda x: x.left == 'cmg' and x.right == 'bvb', edgecopy))[0])
            edgecopy.remove(list(filter(lambda x: x.left == 'jqt' and x.right == 'nvd', edgecopy))[0])

            #Then go through the other existing code of building graph and doing BFS from each node
            nodes = set()
            nodes = build_graph_from_edges(edgecopy)
    
            reachable_count_set = set()
            #Find number of nodes we can reach from each node
            for n in nodes:
                reachable = find_number_of_connected_nodes(nodes, n.name)
                reachable_count_set.add(reachable)

            if len(reachable_count_set) == 2:
                print("Number of unique counts we can reach this round = " + str(len(reachable_count_set)))
                #print edges we removed
                #print("Edges removed: " + node1 + ", " + node2 + ", " + node3)
                product = reachable_count_set.pop() * reachable_count_set.pop()
                found_halver = True
                break
            looper += 1
        if found_halver:
            break
    if found_halver:
        break
print("Product of set sizes - " + str(product))





