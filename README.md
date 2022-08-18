# NanoNm

Machine Methods used to detect the 2'-O-methylation in Nanopore directive RNA-seq

# Step1. Training the 2'-O-methylation model from the Nanopore directive RNA-seq of rRNA.
# $id means sample of each fast5 file
# 1.1 split the multiple fast5 to single fast5 files
multi_to_single_fast5  -i ${id}.fast5 -s $id  --recursive -t 40
# 1.2 base calling using guppy_basecaller
guppy_basecaller -i ${id}/ -s ${id}_guppy --num_callers 40 --recursive --fast5_out --config rna_r9.4.1_70bps_hac.cfg  --cpu_threads_per_caller 10
# 1.3 resquiggle the signal of fast5 files to each transcript
tombo resquiggle --rna --overwrite  ${id}_guppy/workspace/  human_uniq.rRNA.fa    --processes 40 --fit-global-scale --include-event-stdev 
# 1.4 feature calling of each transcripts
find  ${id}_guppy/workspace/ -name "*.fast5" >${id}_guppy.list
python ./software/nanom6A_2021_3_18/extract_raw_and_feature_fast_AUCG.py  --cpu=30 --fl=${id}_guppy.list -o ${id}_guppy.feature --clip=5
# 1.5 mapping the reads to the rRNA
minimap2  -ax map-ont -uf -k14 -x splice -t 20 human_uniq.rRNA.fa    ${id}_guppy.feature.feature.fa|samtools view -@ 20 -bS - |samtools sort -@ 20 -     >${id}.rRNA.sort.bam
sam2tsv -r /home/ch220806/Public/hg19/human_uniq.rRNA.fa   ${id}.rRNA.sort.bam >${id}.rRNA.sort.bam.tsv
# 1.6 Extract the features of fast5 files of Nm sites in mRNA
python  /home/ch220806/2-O-Me/HEK293_RNA_fast5/fast5/pass/filter_get.fast5.py  -i ${id}.rRNA.sort.bam.tsv -b rRNA.Nm1.bed  -f ${id}_guppy.feature.feature.tsv -o ${id}.fast5.rRNA    .signal.txt   >${id}.rRNA.feature.anno.txt
