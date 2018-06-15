import reader
import tools
import alignmentDigit

geneList = dict()

for name in ["./SARS_ena_genome.fasta"]:
    tmp = reader.read(name, True)
    for gene in tmp:
        mRNA = tools.transcription(tmp[gene])
        amino = tools.translation(mRNA)
        geneList[gene] = amino
    
orf = reader.read("./ORF_CoV.fasta")
blosum = alignmentDigit.open_blosum("./BLOSUM62.txt")

print("gene,ORF,local")
for gene in geneList:
    for o in orf:
        print(gene, end=",")
        print(o, end=",")
        local = alignmentDigit.solve_map_local(geneList[gene], orf[o], blosum)
        print(local)
