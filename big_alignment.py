from alignment import open_blosum

def add_something(given, adder):
    answer = list()
    for element in given:
        answer.append((element[0]+adder[0], element[1]+adder[1]))
    return answer

def solve_map_global(d1, d2, blosum, go_through=-8):
    d1 = " " + d1
    d2 = " " + d2
    previous = [[0, [("","")]] for y in range(len(d2))]
    answer = previous[:] 

    for j, ch_j in enumerate(d2):
        if j==0: continue
        answer[j] = [answer[j-1][0]+go_through, add_something(answer[j-1][1], ("-", ch_j))]
    for i, ch_i in enumerate(d1):
        if i==0: continue
        for j in range(len(d2)): previous[j][:], answer[j][:] = answer[j][:], [0, [("", "")]]
        for j, ch_j in enumerate(d2):
            if j==0:
                answer[j] = [previous[j][0]+go_through, add_something(previous[j][1], (ch_i, "-"))]
                continue
            answer[j] = [previous[j-1][0]+blosum[ch_i][ch_j], add_something(previous[j-1][1], (ch_i, ch_j))]

            if answer[j][0] < answer[j-1][0] + go_through:
                answer[j] = [answer[j-1][0]+go_through, add_something(answer[j-1][1], ("-", ch_j))]
            elif answer[j][0] == answer[j-1][0] + go_through:
                answer[j][1].extend(add_something(answer[j-1][1], ("-", ch_j)))

            if answer[j][0] < previous[j][0] + go_through:
                answer[j] = [previous[j][0]+go_through, add_something(previous[j][1], (ch_i, "-"))]
            elif answer[j][0] == previous[j][0] + go_through:
                answer[j][1].extend(add_something(previous[j][1], (ch_i, "-")))
    return answer[-1]

def solve_map_local(d1, d2, blosum, go_through=-8):
    d1 = " " + d1
    d2 = " " + d2
    previous = [[0, [("", "")]] for y in range(len(d2))]
    answer = previous[:]
    maximum = [-1, [("", "")]]

    for j, ch_j in enumerate(d2):
        if j==0: continue
        answer[j] = [answer[j-1][0]+go_through, add_something(answer[j-1][1], ("-", ch_j))]
    for i, ch_i in enumerate(d1):
        if i==0: continue
        for j in range(len(d2)): previous[j][:], answer[j][:] = answer[j][:], [0, [("", "")]]
        for j, ch_j in enumerate(d2):
            if j==0:
                answer[j] = [previous[j][0]+go_through, add_something(previous[j][1], (ch_i, "-"))]
                continue
            answer[j] = [previous[j-1][0]+blosum[ch_i][ch_j], add_something(previous[j-1][1], (ch_i, ch_j))]
            
            if answer[j][0] < answer[j-1][0] + go_through:
                answer[j] = [answer[j-1][0]+go_through, add_something(answer[j-1][1], ("-", ch_j))]
            elif answer[j][0] == answer[j-1][0] + go_through:
                answer[j][1].extend(add_something(answer[j-1][1], ("-", ch_j)))
        
            if answer[j][0] < previous[j][0] + go_through:
                answer[j] = [previous[j][0]+go_through, add_something(previous[j][1], (ch_i, "-"))]
            elif answer[j][0] == previous[j][0] + go_through:
                answer[j][1].extend(add_something(previous[j][1], (ch_i, "-")))

            if answer[j][0] < 0:
                answer[j] = [0, [("", "")]]

            if answer[j][0] > maximum[0]:
                maximum = answer[j][:]
            elif answer[j][0] == maximum[0]:
                maximum[1].extend(answer[j][1])
    return maximum

if __name__ == "__main__":
    blosum = open_blosum()
    d1, d2 = "PAWHEAE", "HEAGAWGHEE"
    answer = solve_map_global(d1, d2, blosum)
    print(answer[0])
    for element in answer[1]:
        print()
        print(element[0])
        print(element[1])

    answer = solve_map_local(d1, d2, blosum)
    print(answer[0])
    for element in answer[1]:
        print()
        print(element[0])
        print(element[1])
