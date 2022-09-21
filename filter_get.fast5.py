###################################################################
# File Name: filter_vcf_by_bed.py
# Author: yanqiangli
#!/usr/bin/env python
# mail: liyq215@gmail.com
#=============================================================
'''This script was used to filter the vcf by the bed'''
import argparse
import joblib,sys,os,re,gzip
from collections import defaultdict
from xgboost.sklearn import XGBClassifier
from pysam import FastaFile
from tqdm import tqdm
import subprocess
import argparse


import joblib,sys,os,re,gzip



def get_capture_region(bed_input):
	dic={}
##chr1	941257	941257	NM_152486_SAMD11	0	+
	for line in bed_input:
#		if line.startswith("chr"):
		tmp=line.strip().split()
		id0 = '_'.join(tmp[0:2])
		if id0 in dic:
			dic[id0].append(tmp[3])
		else:
			dic[id0]=[tmp[3]]
			#print(tmp[0:2])
			#print('_'.join(tmp[0:2]))
	return dic
def read_feature(feature):
#90fa49a0-a362-4bce-83bb-798385a95234.fast5|12|N	A	GGAGG	0.42326189299203537|0.4607219745034687|0.5744907723063143|0.660557006699494|0.6546074030820928	0.19179788776554477|0.19655290326686622|0.17631421643671752|0.11950918008189451|0.14041563607300536	0.4409350904266922|0.4852299396933006|0.5798598449446912|0.6442887166052124|0.6140876830143431	54|58|6|50|16	GGAGG
#	out=open(feature,"r")
	dic2={}
	for line in feature:
		tmp=line.strip().split()
		dic2[tmp[0]]=line
		#print(tmp[0])
	return dic2


def filter_the_csv(bed_input,feature_input,csv_bam,output):
	dic=get_capture_region(bed_input)
	dic2=read_feature(feature_input)
	#for i in gzip.open(csv_bam,"r",encoding='utf-8'):
	#f= gzip.GzipFile(fileobj=csv_bam)
	for i in csv_bam:
	#		i=i.decode('utf-8','ignore').rstrip()
		#print(i)
	#i=i.rstrip()
                # ~ NR_002323.2 0       chr22   7541    A       I       31375381        a       M
		#i=i.decode('utf-8','ignore').rstrip()
		if i.startswith("#"):
        		continue
		ele=i.rstrip().split()
		if ele[3]=="." or ele[6]==".":
        		continue
		ids,chro,idspos,gpos=ele[0],ele[2],(ele[3]),ele[6]
		nm_pos1 = [chro,gpos]
		reads_pos1 = [ids,idspos,"N"]
		Nm_pos = '_'.join(nm_pos1)
		reads_pos = '|'.join(reads_pos1)
		#print(Nm_pos)
		#print(reads_pos)
		if Nm_pos in dic.keys():
			if reads_pos in dic2:
				print(Nm_pos,dic[Nm_pos],reads_pos,sep="\t")
			#print(dic2[reads_pos])
				output.write(dic2[reads_pos])
		else:
#        if ele[1]=="0":
#                strand="+"
#        elif ele[1]=="16":
#                strand="-"
#                lens=len(store[ids])
#                idspos=lens-pidspos-1
			continue



def main():
	parser=argparse.ArgumentParser(description=__doc__)
	parser.add_argument('-i','--input',help='The bam_csv need to be filtered',dest='csv_bam',required=True,type=open)
	parser.add_argument('-b',help='the bed of position',dest='bed_input',required=True,type=open)
	parser.add_argument('-f',help='the raw signal of fast5 ',dest='feature_input',required=True,type=open)
	parser.add_argument('-o','--output',help='the filtered feature output',dest="output",required=True,type=argparse.FileType('w'))
	args=parser.parse_args()
	filter_the_csv(args.bed_input,args.feature_input,args.csv_bam,args.output)

#with gzip.open('76.extract.sort.bam.tsv.gz','rt') as f:
# 	for i in f:
 #       	print(i)
if __name__=="__main__":
	main()
