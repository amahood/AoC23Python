"""
Potential Approach:
- Build up list of all edges - DONE
- Build algo make graph from edges - DONE
- BUild BFS to find number of cells each cell can get to 
- Run all the above by removing 3 different edges, but number of combinations is going to be too high, something 3^
"""

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

#Build graph from edges - LIEKLY NEED TO ENCAPSULATE THIS INTO A FUNCTION TO CALL AFTER REMOVING EDGES
nodes = set()
nodes = build_graph_from_edges(edges)
    
#Should have graph at this point
print("Number of nodes = " + str(len(nodes)))

node_testing = "jqt"
number_we_can_reach = find_number_of_connected_nodes(nodes, node_testing)
#Now need to build BFS to find number of nodes each node can reach
print("Number we can reach from test node to test BFS - " + str(number_we_can_reach))