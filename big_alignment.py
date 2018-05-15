import os
from alignment import open_blosum

def add_something(given, adder):
    answer = list()
    for element in given:
        answer.append((element[0]+adder[0], element[1]+adder[1]))
    return answer

def write_file_num(file_name, data):
    f = open("num" + file_name + ".data", "w")
    f.write(str(data))
    f.close()

def write_file_list(file_name, data):
    f = open("list" + file_name + ".data", "w")
    for element in data:
        f.write("'" + element[0] + "'")
        f.write(" ")
        f.write("'" + element[1] + "'")
        f.write("\n")
    f.close()

def read_file_num(file_name):
    data = open("num" + file_name + ".data", "r").readlines()
    return int(data[0].split()[0])

def read_file_list(file_name):
    data = open("list" + file_name + ".data", "r").readlines()
    answer = list()
    for element in data:
        touch = element.split()
        answer.append((touch[0][1:-1], touch[1][1:-1]))
    return answer

def write_file(file_name, data):
    write_file_num(file_name, data[0])
    write_file_list(file_name, data[1])

def read_file(file_name):
    return [read_file_num(file_name), read_file_list(file_name)]

def big_solve_map_global(d1, d2, blosum, go_through=-8):
    if len(d1) > len(d2): return big_solve_map_global(d2, d1, blosum, go_through)
    d1 = " " + d1
    d2 = " " + d2
    answer = [0, [("", "")]]

    write_file("0+0", answer)
    for i, ch_i in enumerate(d1):
        if i==0: continue
        upper = read_file(str(i-1)+"+0")
        upper = [upper[0]+go_through, add_something(upper[1], (ch_i, "-"))]  
        write_file(str(i)+"+0", upper)
    for j, ch_j in enumerate(d2):
        if j==0: continue
        left = read_file("0+"+str(j-1))
        left = [left[0]+go_through, add_something(left[1], ("-", ch_j))]
        write_file("0+"+str(j), left)
    for i, ch_i in enumerate(d1):
        if i==0: continue
        for j, ch_j in enumerate(d2):
            if j==0: continue
            diagonal = read_file(str(i-1)+"+"+str(j-1))
            upper = read_file(str(i-1)+"+"+str(j))
            left = read_file(str(i)+"+"+str(j-1))

            answer = [diagonal[0]+blosum[ch_i][ch_j], add_something(diagonal[1], (ch_i, ch_j))]
            
            if answer[0] < left[0] + go_through:
                answer = [left[0]+go_through, add_something(left[1], ("-", ch_j))]
            elif answer[0] == left[0] + go_through:
                answer[1].extend(add_something(left[1], ("-", ch_j)))

            if answer[0] < upper[0] + go_through:
                answer = [upper[0]+go_through, add_something(upper[1], (ch_i, "-"))]
            elif answer[0] < upper[0] + go_through:
                answer[1].extend(add_something(upper[1], (ch_i, "-")))

            write_file(str(i)+"+"+str(j), answer)
        os.system("rm -f num" + str(i-1) + "*")
        os.system("rm -f list" + str(i-1) + "*")
    os.system("rm -f *.data")
    return answer

def big_solve_map_local(d1, d2, blosum, go_through=-8):
    if len(d1) > len(d2): return big_solve_map_local(d2, d1, blosum, go_through)
    d1 = " " + d1
    d2 = " " + d2
    answer = [0, [("", "")]]
    maximum = [-1, [("", "")]]

    write_file("0+0", answer)
    for i, ch_i in enumerate(d1):
        if i==0: continue
        upper = read_file(str(i-1)+"+0")
        upper = [upper[0]+go_through, add_something(upper[1], (ch_i, "-"))]
        write_file(str(i)+"+0", upper)
    for j, ch_j in enumerate(d2):
        if j==0: continue
        left = read_file("0+"+str(j-1))
        left = [left[0]+go_through, add_something(left[1], ("-", ch_j))]
        write_file("0+"+str(j), left)
    for i, ch_i in enumerate(d1):
        if i==0: continue
        for j, ch_j in enumerate(d2):
            if j==0: continue
            diagonal = read_file(str(i-1)+"+"+str(j-1))
            upper = read_file(str(i-1)+"+"+str(j))
            left = read_file(str(i)+"+"+str(j-1))
            
            answer = [diagonal[0]+blosum[ch_i][ch_j], add_something(diagonal[1], (ch_i, ch_j))]
            
            if answer[0] < left[0] + go_through:
                answer = [left[0]+go_through, add_something(left[1], ("-", ch_j))]
            elif answer[0] == left[0] + go_through:
                answer[1].extend(add_something(left[1], ("-", ch_j)))
            
            if answer[0] < upper[0] + go_through:
                answer = [upper[0]+go_through, add_something(upper[1], (ch_i, "-"))]
            elif answer[0] < upper[0] + go_through:
                answer[1].extend(add_something(upper[1], (ch_i, "-")))
            
            if answer[0] < 0:
                answer = [0, [("", "")]]

            if answer[0] > maximum[0]:
                maximum[:] = answer[:]
            elif answer[0] == maximum[0]:
                maximum[1].extend(answer[1])

            write_file(str(i)+"+"+str(j), answer)
        os.system("rm -f num" + str(i-1) + "*")
        os.system("rm -f list" + str(i-1) + "*")
    os.system("rm -f *.data")
    return answer

if __name__ == "__main__":
    blosum = open_blosum()
    d1, d2 = "PAWHEAE", "HEAGAWGHEE"
    answer = big_solve_map_global(d1, d2, blosum)
    print(answer[0])
    for element in answer[1]:
        print()
        print(element[0])
        print(element[1])

    answer = big_solve_map_local(d1, d2, blosum)
    print(answer[0])
    for element in answer[1]:
        print()
        print(element[0])
        print(element[1])
