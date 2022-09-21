# NanoNm

# Machine Learning Methods used to detect the 2'-O-methylation in Nanopore direct RNA-seq

# Step0. Install the conda environment first
conda env create -f Nanopore.environment.yml #install conda environment

# Step1. Extract the features of Nanopore directive RNA-seq of rRNA.
# $id means sample of each fast5 file
# 1.1 split the multiple fast5 to single fast5 files
multi_to_single_fast5  -i ${id}.fast5 -s $id  --recursive -t 40
# 1.2 base calling using guppy_basecaller
guppy_basecaller --input_path $id --save_path $id_guppy --num_callers 40 --recursive --fast5_out --config rna_r9.4.1_70bps_hac.cfg  --cpu_threads_per_caller 10
# 1.3 resquiggle the signal of fast5 files to each transcript
tombo resquiggle --rna --overwrite  ${id}\_guppy/workspace/  human_uniq.rRNA.fa    --processes 40 --fit-global-scale --include-event-stdev 
# 1.4 feature calling of each transcripts
find  ${id}\_guppy/workspace/ -name "*.fast5" >${id}_guppy.list
python extract_raw_and_feature_fast_AUCG.py  --cpu=30 --fl = ${id}_guppy.list -o ${id}_guppy.feature --clip=5
# 1.5 mapping the reads to the rRNA
minimap2  -ax map-ont -uf -k14 -x splice -t 20 human_uniq.rRNA.fa    ${id}_guppy.feature.feature.fa|samtools view -@ 20 -bS - |samtools sort -@ 20 -     >${id}.rRNA.sort.bam
sam2tsv -r ./rRNA/human_uniq.rRNA.fa   ${id}.rRNA.sort.bam >${id}.rRNA.sort.bam.tsv
# 1.6 Extract the features of fast5 files of Nm sites in rRNA
python  filter_get.fast5.py  -i ${id}.rRNA.sort.bam.tsv -b rRNA.Nm1.bed  -f ${id}_guppy.feature.feature.tsv -o ${id}.fast5.rRNA.signal.txt   >${id}.rRNA.feature.anno.txt

# Step2 Training the 2'-O-methylation model from the Nanopore directive RNA-seq of rRNA.
cat kmer.txt|xargs -i -e echo "python train_model_scale_pos_weight_Nm.py  {} >>Auc.scale1.txt & " |sh

# Step3 Predict the 2'-O-methylation in the mRNA
python predict_sites_Nm.final1.py   --model ./model --cpu 20  -i all -o C4_2_all.Nm -r  gencode.v27.transcripts.fa  -g GRCh38.p13.genome.fa  -b hg38.gene2transcripts.txt  
