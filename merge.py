import pandas, sys

init = pandas.read_csv(sys.argv[1], sep = "\t", header = None, index_col = False)

for path in sys.argv[2:]:
    df = pandas.read_csv(path, sep = "\t", header = None, index_col = False)
    init[3] = init[3] + df[3]
init.to_csv("merged.tsv", sep = "\t", header = False, columns = [0, 1,2,3], index = False)

