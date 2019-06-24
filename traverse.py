import pyvg

g = pyvg.Graph.from_file("data/chr21.json")

def find_paths_recursive(graph, start, end, path = [], paths = []):
    path = path.copy()
    path.append(start)
    if start == end:
        paths.append(path)
        return
    for out_node in g.edges_from_node(start):
        find_paths_recursive(graph, out_node, end, path, paths)
    return paths



def find_paths_iterative(graph, start, end):
    path = list()
    paths = list()
    # keeps a stack of branching points to backtrack to after reaching the end node
    node_stack = list()
    # must copy the returned list. otherwise, edges will be lost due to pop()
    node_stack.append((start, graph.edges_from_node(start).copy()))
    while len(node_stack) > 0:
        current_node = node_stack.pop()
        path.append(current_node[0])
        # end of ultrabubble
        if current_node[0] == end:
            # save the path and revert to last branch point
            paths.append(path.copy())
            path = path[:path.index(node_stack[-1][0])]
            continue
        # branch point
        if len(current_node[1]) > 0:
            # move one out_node from the adjacency list to top of the stack
            next_node = current_node[1].pop()
            node_stack.append(current_node)
            node_stack.append((next_node, graph.edges_from_node(next_node).copy()))
    return paths

snarl_paths = find_paths_iterative(g, 96657778, 96657792)
for path in snarl_paths:
    for node in path:
        print(node)
