#!/usr/bin/env python

import argparse
import jinja2
import os

from util_functions import parse_fasta_seqs, write_to_fasta


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Create a RevBayes Rev input file from a template.")
    parser.add_argument(
        'template_path', type=str,
        help="Path to Rev template.")
    parser.add_argument(
        'fasta_path', type=str,
        help="Path to FASTA input alignment.")
    parser.add_argument(
        '--naive', type=str, required=True,
        help="The name of the naive sequence.")
    parser.add_argument(
        '--iter', type=int, required=True,
        help="The number of total MCMC iterations.")
    parser.add_argument(
        '--thin', type=int, required=True,
        help="The MCMC sampling frequency.")
    parser.add_argument(
        '--naive-correction', action='store_true', default=False,
        help="Should we apply the naive sequence correction?")
    parser.add_argument(
        '--output-path', type=str, required=True,
        help="The Rev output script file path.")
    parser.add_argument(
        '--output-fasta', type=str, required=True,
        help="The Rev output FASTA file path.")

    args = parser.parse_args()

    output_base = os.path.splitext(args.output_path)[0]
    id_seq = parse_fasta_seqs(args.fasta_path)

    assert args.naive in id_seq, "Sequence %r not found in FASTA file." % args.naive

    # Do we need to apply the naive sequence correction?
    naive_name = "naive" if args.naive_correction else "_naive_"

    if naive_name != args.naive:
        id_seq[naive_name] = id_seq[args.naive]
        del id_seq[args.naive]
        args.naive = naive_name

    write_to_fasta(id_seq, args.output_fasta)

    temp_vars = dict(
        fasta_path=args.output_fasta,
        naive=args.naive,
        iter=args.iter,
        thin=args.thin,
        basename=output_base
    )

    env = jinja2.Environment(loader = jinja2.FileSystemLoader('.'),
                             undefined=jinja2.StrictUndefined,
                             trim_blocks=True, lstrip_blocks=True)

    env.get_template(args.template_path).stream(**temp_vars).dump(args.output_path)
