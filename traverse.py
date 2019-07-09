import pyvg

def is_ref_interval(path, ref_path):
    ref_nodes = set(ref_path.nodes_in_interval())
    # deletion path
    if len(path) <= 2:
        return False
    # other paths
    for node in path:
        if node not in ref_nodes:
            return False
    return True


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
    import pyvg.conversion
    import pyvg.alignmentcollection
    import offsetbasedgraph as ob
    import sys

    # graph json file
    graph_json = sys.argv[1]
    # obgraph numpy file
    obg_numpy = sys.argv[2]
    # json alignment file
    aln_json = sys.argv[3]
    # protobuffer file from vg snarls
    snarls_file = sys.argv[4]
    # file to .interval file describing the linear path
    linear_file = sys.argv[5]

    # g = pyvg.conversion.json_file_to_obg_numpy_graph("data/chr21.json")
    g = pyvg.Graph.from_file(graph_json)

    # obg = g.get_offset_based_graph()
    obg = ob.Graph.from_file(obg_numpy)
    
    wgs_alignments = pyvg.alignmentcollection.AlignmentCollection.from_vg_json_file(aln_json, obg)
    # wgs_alignments = pyvg.alignmentcollection.AlignmentCollection.from_vg_json_file("data/chr21_wgs.json", obg)

    # load snarls
    snarls  = pyvg.Snarls.from_vg_snarls_file(snarls_file)
    # load chr21 ref path
    chr21_ref = ob.NumpyIndexedInterval.from_file(linear_file)

    for snarl in snarls.snarls:
        #if abs(snarl.end.node_id - snarl.start.node_id) > 10:
        snarl_paths = find_paths_iterative(g, snarl.start.node_id, snarl.end.node_id)
        for path in snarl_paths:
            reads = 0
            for node in path:
                alignments = wgs_alignments.get_alignments_on_node(node)
                reads = reads + len(alignments)
            print( str(snarl.start.node_id) + "\t" + str(snarl.end.node_id) + "\t" + str(is_ref_interval(path, chr21_ref)) + "\t" + str(reads))
