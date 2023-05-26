#!/usr/bin/env python
import os,re,sys
from argparse import ArgumentParser
from umi_dedup_duplex import run_umi_extract_consensus
from alignment import run_align
from variant_monitor import run_monitor

def resolveConfig(configure_file):
    file = open(configure_file, 'r')
    count_lines = 0
    myDict = {}
    for line in file.readlines():
        line = line.strip()
        count_lines +=1
        if re.match(r'^#.*', line):
            continue
        match_key_value = re.match(r'^\s*([^=\s]+)\s*=\s*(.*)$', line)
        if match_key_value == None:
            continue
        key = match_key_value.group(1)
        value = match_key_value.group(2)
        if key == '' or value == '' :
            print("Could not find key or value at line %s.\n" %(count_lines))
            continue
        match_var_value = re.match(r'^\$\((.*)\)(.*)$', value)
        if match_var_value != None:
            variable_key = match_var_value.group(1)
            variable_value = match_var_value.group(2)
            if myDict.has_key(variable_key):
                value = myDict[variable_key] + variable_value
        myDict[key]=value
    return myDict

if __name__ == '__main__':
    # Parameters to be input.
    parser = ArgumentParser(description="MRD pipeline pyflow")
    parser.add_argument("-r1","--read1", action="store", dest="read1",
                        help="tumour read1 fastq", required=True)
    parser.add_argument("-r2","--read2", action="store", dest="read2",
                        help="tumour read2 fastq", required=True)
    parser.add_argument('-b', '--bed', action="store", dest="bed",
                        help='target region bed', required=True)
    parser.add_argument('-v', '--variant', action="store", dest="variant", 
                        help='monitor variant', required=True)
    parser.add_argument("-c", "--cfg", action="store", dest="cfg",
                        help="configure file", required=True)
    parser.add_argument("-o", "--output_dir", action="store", dest="output_dir",
                        help="output dir", required=True)
    parser.add_argument("-p", "--prefix", action="store", dest="prefix",
                        help="sample prefix", required=True)
    parser.add_argument("-u","--umi_pattern", action="store", dest="umi_pattern",
                        help="umi pattern, default 6N,6N", default="6N,6N")
    parser.add_argument('-f','--familysize', action="store", dest="familysize", 
                        help='Minimum molecular familysize, default 3', default=3)
    parser.add_argument('-m','--mindepth', action="store", dest="mindepth", 
                        help='Minimum depth for variant, default 1000', default=1000)
    parser.add_argument('--onlyduplex',action="store_true",  
                        help="Only use duplex sequence,default False", default=False)
    parser.add_argument("-s","--steps", action="store", dest="steps",
                        help="the steps you wanna perform, seperate by comma. \
                        options:umi,aln,monitor. default all", default="umi,aln,monitor")
    args = parser.parse_args()
    config = resolveConfig(args.cfg)
    steps='umi,aln,monitor'
    if args.steps:
        steps = args.steps
    # umi trim and dedup
    if 'umi' in steps:
        run_umi_extract_consensus(args.read1,args.read2,args.output_dir,args.umi_pattern,args.prefix,config)
    # align
    if 'aln' in steps:
        dedup_fq1 = '%s/%s_rmdup_R1.fastq.gz'%(args.output_dir, args.prefix)
        dedup_fq2 = '%s/%s_rmdup_R2.fastq.gz'%(args.output_dir, args.prefix)
        run_align(','.join([dedup_fq1,dedup_fq2]),args.prefix,args.output_dir,config)
    # variant monitor
    if 'monitor' in steps:
        genome = config['genome_fasta']
        bam = '%s/%s.sorted.bam'%(args.output_dir, args.prefix)
        run_monitor(genome,bam,args.bed,args.variant,args.prefix,args.familysize,args.mindepth,args.output_dir,args.onlyduplex)