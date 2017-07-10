# Guidelines

Please only commit changes to Jupyter/Sage notebooks after clearing output.


# Example usage

First we process the BEAST runs into ancestors with their counts:

    python/trees_to_counted_ancestors.py --burnin 100 --seed BF520.1-igh runs/2017-07-10/BF520.1-h-IgH.family_0.healthy.tre.seedpruned.100.ids.trees data/2017-07-10/BF520.1-h-IgH.family_0.healthy.tre.seedpruned.100.ids.fasta

(this takes about 10 mins on my chromebook; to try it out use ten.trees instead).

Now tabulate the mutations:

    python/tabulate_mutations.py runs/2017-07-10/BF520.1-h-IgH.family_0.healthy.tre.seedpruned.100.ids.aa_lineage.fasta

This makes `runs/2017-07-10/BF520.1-h-IgH.family_0.healthy.tre.seedpruned.100.ids.aa_lineage.muts.csv`, which tabulates the mutations from naive in a format `[old AA][1-indexed position][new AA]`.

Now start sage with `sage -n jupyter` in the ecgtheow root directory.
Open `sage/sage.ipynb`.