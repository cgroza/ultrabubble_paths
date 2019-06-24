import offsetbasedgraph  as ob
import offsetbasedgraph.graphtraverser
import pyvg
import pyvg.conversion
import pyvg.graphstats
import pyvg.alignmentcollection
import pyvg.alignment
import os
from offsetbasedgraph import NumpyIndexedInterval

# load vg graph
if not os.path.exists("data/chr21.npy"):
    g = pyvg.conversion.json_file_to_obg_numpy_graph("data/chr21.json")
    g.to_numpy_file("data/chr21.npy")

# offsetbasedgraph
# load fast numpy backend graph
g = ob.Graph.from_file("data/chr21.npy")
# enables snarls traversal
# traverser = offsetbasedgraph.graphtraverser.GraphTravserserBetweenNodes(g)
# returns the subgraph between nodes start, end
# subgraph = traverser.get_snarl_subgraph(95969074, 95969075)

# load vg alignments as intervals
# a = pyvg.conversion.vg_json_file_to_intervals("data/NA12878_H3K4me1_chr21.json", g)
# a_collection = ob.IntervalCollection(a)


# load snarls
# snarls  = pyvg.Snarls.from_vg_snarls_file("data/snarls")
# variant_path_snarls  = pyvg.Snarls.from_vg_snarls_file("data/snarls_variant_paths")
# traversals = pyvg.Snarls.from_vg_snarls_file("data/snarl_traversals")

# retrieve the snarl subgraphs
# for s in snarls.snarls :
#     print(traverser.get_snarl_subgraph(s.start.node_id, s.end.node_id))

# for s in snarls.snarls :
#     if abs(s.start.node_id - s.end.node_id) > 10:
#         print(s)

# type: ULTRABUBBLE
# start {
#   node_id: 97521794
# }
# end {
#   node_id: 97521816
# }
# type: ULTRABUBBLE
# start {
#   node_id: 96657778
# }
# end {
#   node_id: 96657792
# }

# Insertion ultrabubble
# g = pyvg.Graph.from_file("data/chr21.json")
# g.edges_from_node(96657778)
# g.edges_from_node(96657792)

# linear_path = NumpyIndexedInterval.from_file("data/chr21_linear_pathv2.interval")

# count = pyvg.graphstats.count_variants_in_graph(g, linear_path)

# NOTE: useful function. Only need to find traversal paths in an ultrabubble. Try on a WGS alignment.
wgs_alignments = pyvg.alignmentcollection.AlignmentCollection.from_vg_json_file("data/chr21_wgs.json", g)
# alignments = wgs_alignments.get_alignments_on_node(96657778)

path = [96657778, 96657779, 96657780, 96657781,
 96657782, 96657783, 96657784, 96657785,
 96657786, 96657787, 96657788, 96657789,
 96657790, 96657791, 96657792]
alignments = {}
for node in path:
    alignments[node] = wgs_alignments.get_alignments_on_node()
