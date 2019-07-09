import pyvg
from traverse import *
import pyvg.conversion
import sys

# graph json file
graph_json = sys.argv[1]
# obgraph numpy file
# protobuffer file from vg snarls
snarls_file = sys.argv[2]

g = pyvg.Graph.from_file(graph_json)

# load snarls
snarls  = pyvg.Snarls.from_vg_snarls_file(snarls_file)

for snarl in snarls.snarls:
    if abs(snarl.end.node_id - snarl.start.node_id) > 40 :
        print( str(snarl.start.node_id) + "\t" + str(snarl.end.node_id) + "\t" + "large")
        continue
    snarl_paths = find_paths_iterative(g, snarl.start.node_id, snarl.end.node_id)
    print( str(snarl.start.node_id) + "\t" + str(snarl.end.node_id) + "\t" + str(len(snarl_paths)))
