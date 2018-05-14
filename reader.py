def cut_it(name):
    if name[0] == ">":
        name = name[1:]
    return name.split()[0]

def read(file_name="MERS_Korea_genome.fasta", full_name=False):
    gene_list = dict()
    pasta_file = open(file_name, "r").readlines()

    name = ""
    gene = ""
    for line in pasta_file:
        tmp = line.strip()
        if tmp[0] == ">":
            if name != "":
                gene_list[name] = gene
            if full_name:
                name = tmp
            else:
                name = cut_it(tmp)
            gene = ""
        else:
            gene += tmp
    return gene_list

if __name__ == "__main__":
    gene_list = read()
    for i, name in enumerate(gene_list):
        print(i, name)
