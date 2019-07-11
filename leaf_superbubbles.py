import sys

nodes = open(sys.argv[1], "r")
tree = {(0, sys.maxsize, ""): []}

# Here we assume a max subtree size for superbubble parent nodes
MAX_TREE_DEPTH = 500
def is_leaf(root, bubble):
    children = list(root.values())[0]
    # only search the tail of the list since the intervals arrive in topological order

    for child in children[-MAX_TREE_DEPTH:]:
        c = list(child)[0]
        # found a parent node one level deeper
        # return as a new parent
        if bubble[0] >= c[0] and bubble[1] <= c[1]:
            return child
    return False


def insert_bubble(root, bubble):
    prev_root = root        # save the root
    root = is_leaf(root, bubble)
    # bubble is not a child, add as child of the root
    if not root:
        list(prev_root.values())[0].append({bubble : []})
        return prev_root
    # bubble is a child, explore the tree deeper to find the leaf
    insert_bubble(root, bubble)

def leafs(root):
    # check if leaf node
    children = list(root.values())[0]
    # no children, output as leaf node
    if len(children) == 0:
        r = list(root)[0]
        print(str(r[0]) + " " + str(r[1]) + " " + str(r[2]))
    # has children, explore tree
    else:
        # DEBUG
        # if(root is not tree):
        #     print(root)
        for child in children:
            leafs(child)

i = 0
for line in nodes:
    fields = line.split()
    cur_src = int(fields[0])
    cur_sink = int(fields[1])
    cur_paths = int(fields[2])

    insert_bubble(tree, (cur_src, cur_sink, cur_paths))
    if i % 10000 == 0:
        sys.stderr.write("Processed " + str(i) + "\n")
    i = i + 1

leafs(tree)
