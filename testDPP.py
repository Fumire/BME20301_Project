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

dpp4 = reader.read("./DPP4.fasta", True)
blosum = alignmentDigit.open_blosum("./BLOSUM50.txt")

print("gene,DPP4,local,global")
for gene in geneList:
    for d in dpp4:
        print(gene, end=",")
        print(d, end=",")
        local = alignmentDigit.solve_map_local(geneList[gene], dpp4[d], blosum)
        glob = alignmentDigit.solve_map_global(geneList[gene], dpp4[d], blosum)
        print(local, end=",")
        print(glob)
