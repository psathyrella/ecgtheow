#!/usr/bin/env python

import argparse
import os
import yaml


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Parse partis cluster data and generate 'healthy' seeded sequences.")
    parser.add_argument(
        'data_dir', type=str,
        help="Path to partis data directory.")
    parser.add_argument(
        '--sample', type=str, required=True,
        help="The name of the sample.")
    parser.add_argument(
        '--seed', type=str, required=True,
        help="The name of the seed sequence.")
    parser.add_argument(
        '--inferred-naive-name', type=str, required=True,
        help="""What do we call the partis-inferred naive sequence when we inject it among the other (input) sequences.""")
    parser.add_argument(
        '--output-path', type=str, required=True,
        help="Path to output FASTA file.")

    args = parser.parse_args()
    args.data_dir = args.data_dir.rstrip("/")

    # Load the YAML file.
    with open(args.data_dir + '/info.yaml', 'r') as f:
        yaml_dict = yaml.load(f)

    sample = yaml_dict["samples"][args.sample]
    locus = sample["meta"]["locus"]
    partition_path = sample["seeds"][args.seed]["partition-file"]

    os.system("export PARTIS=${PWD%/}/lib/cft/partis;" +\
              "lib/cft/bin/process_partis.py" +\
              " --partition-file " + partition_path +\
              " --seqs-out " + args.output_path +\
              (" --parameter-dir " + sample["parameter-dir"] if sample.get("glfo-dir") else "") +\
              " --locus " + locus +\
              " --inferred-naive-name inferred_naive" +\
              " --remove-frameshifts --remove-stops" +\
              " --remove-mutated-invariants --indel-reversed-seqs")
