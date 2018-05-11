def open_blosum(file_name="./BLOSUM50.txt"):
    blosum = dict()
    f = open(file_name, 'r')
    names = list()

    for line in f.readlines():
        if line[0] == '#':
            continue
        if len(line.split()) == 24:
            names = line.split()
            for name in names:
                blosum[name] = dict()
        else:
            for i, score in enumerate(line.split()[1:]):
                blosum[line.split()[0]][names[i]] = int(score)
    return blosum

def solvel_map_global(d1, d2, blosum, go_through=-8):
    d1 = " " + d1
    d2 = " " + d2
    answer = [[[0, ""] for y in range(len(d2))] for x in range(len(d1))]

    for i in range(1, len(d1)):
        answer[i][0] = [answer[i-1][0][0] + go_through, "↑"]
    for j in range(1, len(d2)):
        answer[0][j] = [answer[0][j-1][0] + go_through, "←"]

    for i, ch_i in enumerate(d1):
        if i==0: continue
        for j, ch_j in enumerate(d2):
            if j==0: continue
            answer[i][j] = [answer[i-1][j-1][0] + blosum[ch_i][ch_j], "↖"]

            if answer[i][j][0] < answer[i][j-1][0] + go_through:
                answer[i][j] = [answer[i][j-1][0] + go_through, "←"]
            elif answer[i][j][0] == answer[i][j-1][0] + go_through:
                answer[i][j][1] += "←"

            if answer[i][j][0] < answer[i-1][j][0] + go_through:
                answer[i][j] = [answer[i-1][j][0] + go_through, "↑"]
            elif answer[i][j][0] == answer[i-1][j][0] +go_through:
                answer[i][j][1] += "↑"
    return answer

def solve_map_local(d1, d2, blosum, go_through=-8):
    d1 = " " + d1
    d2 = " " + d2
    answer = [[[0, "*"] for y in range(len(d2))] for x in range(len(d1))]

    for i, ch_i in enumerate(d1):
        if i==0: continue
        for j, ch_j in enumerate(d2):
            if j==0: continue
            answer[i][j] = [answer[i-1][j-1][0] + blosum[ch_i][ch_j], "↖"]

            if answer[i][j][0] < answer[i][j-1][0] + go_through:
                answer[i][j] = [answer[i][j-1][0] + go_through, "←"]
            elif answer[i][j][0] == answer[i][j-1][0] + go_through:
                answer[i][j][1] += "←"

            if answer[i][j][0] < answer[i-1][j][0] + go_through:
                answer[i][j] = [answer[i-1][j][0] + go_through, "↑"]
            elif answer[i][j][0] == answer[i-1][j][0] + go_through:
                answer[i][j][1] += "↑"

            if answer[i][j][0] < 0:
                answer[i][j] = [0, "*"]
    return answer

class Alignment:
    def __init__(self, d1="", d2="", blosum_file="./BLOSUM50.txt"):
        self.gene1 = d1
        self.gene2 = d2
        self.blosum = open_blosum(blosum_file)
        self.solve()
        self.gene1, self.gene2 = "-"+d1, "-"+d2

    def solve(self):
        self.answer_global = solvel_map_global(self.gene1, self.gene2, self.blosum)
        self.answer_local = solve_map_local(self.gene1, self.gene2, self.blosum)
        self.find_alignment_global()
        self.find_alignment_local()

    def print_all(self):
        self.print_global()
        self.print_local()

    def print_global(self):
        print('Global Alignment')
        print('    ', '    '.join(self.gene2))
        for i, ch_i in enumerate(self.gene1):
            print(ch_i, end=' ')
            for j, ch_j in enumerate(self.gene2):
                print("%4d" % self.answer_global[i][j][0], end=' ')
            print()
        print()
        print('   ', '   '.join(self.gene2))
        for i, ch_i in enumerate(self.gene1):
            print(ch_i, end= ' ')
            for j, ch_j in enumerate(self.gene2):
                print("%3s" % self.answer_global[i][j][1], end=' ')
            print()

    def print_local(self):
        print('Local Alignment')
        print('    ', '    '.join(self.gene2))
        for i, ch_i in enumerate(self.gene1):
            print(ch_i, end=' ')
            for j, ch_j in enumerate(self.gene2):
                print("%4d" % self.answer_local[i][j][0], end=' ')
            print()
        print()
        print('   ', '   '.join(self.gene2))
        for i, ch_i in enumerate(self.gene1):
            print(ch_i, end=' ')
            for j, ch_j in enumerate(self.gene2):
                print("%3s" % self.answer_local[i][j][1], end=' ')
            print()

    def find_alignment_global(self):
        route =[[len(self.gene1)-1, len(self.gene2)-1, ""]]
        route_global = list()

        while len(route):
            x, y, tmp = route[0]
            route[:] = route[1:]
            if x == 0 and y == 0:
                route_global.append(tmp)
                continue
            if self.answer_global[x][y][1].find("↖") != -1:
                route.append([x-1, y-1, "↖"+tmp])
            if self.answer_global[x][y][1].find("←") != -1:
                route.append([x, y-1, "←"+tmp])
            if self.answer_global[x][y][1].find("↑") != -1:
                route.append([x-1, y, "↑"+tmp])

        self.subgene_global = list()
        for route in route_global:
            x, y = len(self.gene1)-1, len(self.gene2)-1
            subgene1, subgene2 = "", ""
            for ch in route[::-1]:
                if ch == "↖":
                    subgene1 = self.gene1[x] + subgene1
                    subgene2 = self.gene2[y] + subgene2
                    x, y = x-1, y-1
                elif ch == "←":
                    subgene1 = "-" + subgene1
                    subgene2 = self.gene2[y] + subgene2
                    x, y = x, y-1
                elif ch == "↑":
                    subgene1 = self.gene1[x] + subgene1
                    subgene2 = "-" + subgene2
                    x, y = x-1, y
            self.subgene_global.append((subgene1, subgene2))

    def find_alignment_local(self):
        maximum_position = list()
        for i in range(len(self.gene1)):
            for j in range(len(self.gene2)):
                if len(maximum_position) == 0:
                    maximum_position.append([i, j, self.answer_local[i][j][0]])
                elif maximum_position[0][2] == self.answer_local[i][j][0]:
                    maximum_position.append([i, j, self.answer_local[i][j][0]])
                elif maximum_position[0][2] < self.answer_local[i][j][0]:
                    maximum_position[:] = []
                    maximum_position.append([i, j, self.answer_local[i][j][0]])

        route = list()
        route_local = list()
        for x, y, z in maximum_position:
            route.append([x, y, ""])

        while len(route):
            x, y, tmp = route[0]
            route[:] = route[1:]
            if self.answer_local[x][y][1] == "*":
                route_local.append(tmp)
                continue
            if self.answer_local[x][y][1].find("↖") != -1:
                route.append([x-1, y-1, "↖"+tmp])
            if self.answer_local[x][y][1].find("←") != -1:
                route.append([x, y-1, "←"+tmp])
            if self.answer_local[x][y][1].find("↑") != -1:
                route.append([x-1, y, "↑"+tmp])

        self.subgene_local = list()
        for route in route_local:
            x, y = len(self.gene1)-1, len(self.gene2)-1
            subgene1, subgene2 = "", ""
            for ch in route[::-1]:
                if ch == "↖":
                    subgene1 = self.gene1[x] + subgene1
                    subgene2 = self.gene2[y] + subgene2
                    x, y = x-1, y-1
                elif ch == "←":
                    subgene1 = "-" + subgene1
                    subgene2 = self.gene2[y] + subgene2
                    x, y = x, y-1
                elif ch == "↑":
                    subgene1 = self.gene1[x] + subgene1
                    subgene2 = "-" + subgene2
                    x, y = x-1, y
            self.subgene_local.append((subgene1, subgene2))

    def show_alignment_global(self):
        for i, gene in enumerate(self.subgene_global):
            print(i+2)
            print(gene[0])
            print(gene[1])

    def show_alignment_local(self):
        for i, gene in enumerate(self.subgene_local):
            print(i+1)
            print(gene[0])
            print(gene[1])

if __name__ == "__main__":
    open_blosum()
    d1, d2 = "PAWHEAE", "HEAGAWGHEE"
    answer = Alignment(d1, d2)
    answer.show_alignment_local()
