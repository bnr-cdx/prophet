# Title
Individualized tumor-informed circulating tumor DNA (ctDNA) analysis for postoperative monitoring of non-small cell lung cancer (NSCLC)
# Install
please install these packages in python3 before running the pipeline:
re, os, sys, argparse, pysam, collections, multiprocessing, umi_tools, numpy, gzip, scipy, scikit_posthocs, sympy.
please supply correct path of genome and software in configure file.
# Usage
python3 mrd_pyflow.py -r1 test_R1.fastq.gz -r2 test_R2.fastq.gz -b test.target.region.bed -v test.tracking.variants.txt -c pipeline.cfg -o ./ -p test
# Contribution
BNR
