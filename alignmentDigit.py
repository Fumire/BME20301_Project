from alignment import open_blosum

def solve_map_global(d1, d2, blosum, go_through=-8):
    d1 = " " + d1
    d2 = " " + d2
    answer = [[0 for y in range(len(d2))] for x in range(len(d1))]

    for i in range(1, len(d1)):
        answer[i][0] = answer[i-1][0] + go_through
    for j in range(1, len(d2)):
        answer[0][j] = answer[0][j-1] + go_through

    for i, ch_i in enumerate(d1):
        if i==0: continue
        for j, ch_j in enumerate(d2):
            if j==0: continue
            answer[i][j] = answer[i-1][j-1] + blosum[ch_i][ch_j]

            if answer[i][j] < answer[i][j-1] + go_through:
                answer[i][j] = answer[i][j-1] + go_through
            if answer[i][j] < answer[i-1][j] + go_through:
                answer[i][j] = answer[i-1][j] + go_through

    return answer[len(d1)-1][len(d2)-1]

def solve_map_local(d1, d2, blosum, go_through=-8):
    d1 = " " + d1
    d2 = " " + d2
    real_answer = 0
    answer = [[0 for y in range(len(d2))] for x in range(len(d1))]

    for i, ch_i in enumerate(d1):
        if i==0: continue
        for j, ch_j in enumerate(d2):
            if j==0: continue
            answer[i][j] = answer[i-1][j-1] + blosum[ch_i][ch_j]

            if answer[i][j] < answer[i][j-1] + go_through:
                answer[i][j] = answer[i][j-1] + go_through
            if answer[i][j] < answer[i-1][j] + go_through:
                answer[i][j] = answer[i-1][j] + go_through
            if answer[i][j] < 0:
                answer[i][j] = 0
            if real_answer < answer[i][j]:
                real_answer = answer[i][j]
    return real_answer

if __name__ == "__main__":
    pass
