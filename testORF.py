import reader
import tools
import alignmentDigit

geneList = dict()

for name in ["./Common_cold.fasta", "./MERS_Korea_genome.fasta", "./SARS_ena_genome.fasta"]:
    tmp = reader.read(name, True)
    for gene in tmp:
        mRNA = tools.transcription(tmp[gene])
        amino = tools.translation(mRNA)
        geneList[gene] = amino
    
orf = reader.read("./ORF_CoV.fasta")
blosum = alignmentDigit.open_blosum("./BLOSUM50.txt")

print("gene,ORF,local,global")
for gene in geneList:
    for o in orf:
        print(gene, end=",")
        print(o, end=",")
        local = alignmentDigit.solve_map_local(geneList[gene], orf[o], blosum)
        glob = alignmentDigit.solve_map_global(geneList[gene], orf[o], blosum)
        print(local, end=",")
        print(glob)
