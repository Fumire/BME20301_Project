def transcription(dna):
    change = {"A":"U", "C":"G", "G":"C", "T":"A"}
    ans = ""
    for ch in dna:
        ans += change[ch]
    return ans

def complementary(gene):
    change = {"A":"T", "C":"G", "G":"C", "T":"A", "U":"A"}
    ans = ""
    for ch in gene:
        ans += change[ch]
    return ans

codon_table = {'UUU':'F', 'UUC':'F', 'UUA':'L', 'UUG':'L', 'CU':'L', 'AUU':'I', 'AUC':'I', 'AUA':'I', 'AUG':'M', 'GU':'V', 'UC':'S', 'CC':'P', 'AC':'T', 'GC':'A', 'UAU':'Y', 'UAC':'Y', 'UAA':'*', 'UAG':'*', 'CAU':'H', 'CAC':'H', 'CAA': 'Q', 'CAG':'Q', 'AAU':'N', 'AAC':'N', 'AAA':'K', 'AAG':'K', 'GAU':'D', 'GAC':'D', 'GAA':'E', 'GAG':'E', 'UGU':'C', 'UGC':'C', 'UGA':'*', 'UGG':'W', 'CG':'R', 'AGU':'S', 'AGC':'S', 'AGA':'R', 'AGG':'R', 'GG':'G'}

def translation(gene):
    poly_amino = ""
    while len(gene) >= 3:
        if gene[:3] == 'AUG':
            break
        else:
            gene = gene[1:]
    while len(gene) >= 3:
        tmp, gene = gene[:3], gene[3:]
        if tmp[:2] in codon_table:
            poly_amino += codon_table[tmp[:2]]
        elif codon_table[tmp] == "*":
            break
        else:
            poly_amino += codon_table[tmp]

    if poly_amino == "":
        return list()
    else:
        ans = [poly_amino]
        ans.extend(translation(gene))
        return ans

def difference(gene1, gene2):
    ans = 0
    assert len(gene1) == len(gene2)
    for i in range(len(gene1)):
        if gene1[i] != gene2[i]:
            ans += 1
    return ans

def similarity(gene1, gene2):
    ans = 0
    assert len(gene1) == len(gene2)
    for i in range(len(gene1)):
        if gene1[i] == gene2[i]:
            ans += 1
    return ans

def findSimilar(gene1, gene2):
    if len(gene1) > len(gene2):
        return findSimilar(gene2, gene1)

    ans = -1
    for i in range(len(gene2)-len(gene1)+1):
        tmp = similarity(gene1, gene2[i:i+len(gene1)])
        if tmp > ans:
            ans = tmp
    return ans/len(gene1)

if __name__ == "__main__":
    gene1 = "ACT"
    gene2 = "AAAA"
    print(findSimilar(gene1, gene2))
