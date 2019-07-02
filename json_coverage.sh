#!/bin/bash
# perhaps we could take the vg file and generate these here
GRAPH_JSON=$1
ALN_JSON=$2
SNARLS=$3
LINEAR_INTERVAL=$4

# split alignment json in 50M line subsets
split -l 50000000 $ALN_JSON --additional-suffix=ALN_FRAG

for file in *ALN_FRAG
do
echo << SCRIPT
#!/bin/bash
#SBATCH --cpus-per-task=1
#SBATCH --time=12:00:00
#SBATCH --job-name=${file}_cov
#SBATCH --mem=150G
#SBATCH --account=rrg-bourqueg-ad

module unload mugqic/python
module load python/3.7.0

python3 traverse.py $file $GRAPH_JSON $SNARLS $LINEAR > count_$file.tsv
SCRIPT
done

# merge the files with merge.sh

