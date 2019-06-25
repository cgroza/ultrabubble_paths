import pyvg
import pyvg.conversion


def find_paths_recursive(graph, start, end, path = None, paths = None):
    if path is None:
        path = []
    if paths is None:
        paths = []

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
            # need to check if there are still edges to be followed
            if len(node_stack) > 0 and  len(node_stack[-1]) > 0:
                path = path[:path.index(node_stack[-1][0])]
                continue
            # no edges, break out of loop
            break
        # branch point
        if len(current_node[1]) > 0:
            # move one out_node from the adjacency list to top of the stack
            next_node = current_node[1].pop()
            # add it back to the stack it still has remaining edges after removing one
            if len(current_node[1]) > 0:
                node_stack.append(current_node)
            node_stack.append((next_node, graph.edges_from_node(next_node).copy()))
    return paths

if __name__ == "__main__":
    print("Loading graph")
#    g = pyvg.conversion.json_file_to_obg_numpy_graph("data/chr21.json")
    g = pyvg.Graph.from_file("data/chr21.json")

    # load snarls
    print("Loading snarls")
    snarls  = pyvg.Snarls.from_vg_snarls_file("data/snarls")

    for snarl in snarls.snarls:
        if abs(snarl.end.node_id - snarl.start.node_id) > 10:
            print("Snarl:")
            print(snarl)
            snarl_paths = find_paths_iterative(g, snarl.start.node_id, snarl.end.node_id)
            print(snarl_paths)
