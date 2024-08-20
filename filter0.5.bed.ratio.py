import sys,os,re
fl=sys.argv[1]
# ~ fl=sys.argv[1].rstrip("/")
# ~ fl1="%s/ratio.0.5.tsv"%(fl)
save_dict={}
# ~ result_45CM/ratio.0.5.tsv 
# ~ AT4G38840|chr04	18124995|419|671|0.624441132637854	18125012|292|794|0.3677581863979849	18125050|380|835|0.4550898203592814	18125056|453|845|0.5360946745562131	18125080|273|851|0.3207990599294947	18125301|283|815|0.347239263803681	18125342|22|799|0.02753441802252816	18125414|554|783|0.7075351213282248	18125480|185|725|0.25517241379310346
fl1=sys.argv[2]
output=open(fl1+".filter.bed","w")
for i in open(fl,"r"):
	ele=i.rstrip().split()
	name,chro=ele[0].split("|")
	for pos in ele[1:]:
		pos1=int(pos.split("|")[0])
		ratio = (pos.split("|")[3])
		coverage1 = (pos.split("|")[1])
		coverage2 = (pos.split("|")[2])
 		if ratio >= 0 and coverage2 >10:
			list1 = (chro,str(pos1),str(pos1+1),ratio,name,str(coverage1),str(coverage2))
			output.write("\t".join(list1))
			output.write("\n")
						
		#save_dict["%s|%s|%s"%(chro,pos,name)]=1
# ~ fl2="%s/genome_abandance.0.5.bed"%(fl)
output.close()
