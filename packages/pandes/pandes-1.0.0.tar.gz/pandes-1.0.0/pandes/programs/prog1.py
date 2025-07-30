def get_code():
    return '''
import csv
with open("sports.csv") as f:
    file = csv.reader(f)
    data = list(file)
    specific = data[1][:-1]
    general = [['?' for i in range(len(specific))] for j in range(len(specific))]
    for i in data:
        if i[-1] == "yes":
            for j in range(len(specific)):
                if i[j] != specific[j]:
                    specific[j] = "?"
                    general[j][j] = "?"
        elif i[-1] == "no":
            for j in range(len(specific)):
                if i[j] != specific[j]:
                    general[j][j] = specific[j]
                else:
                    general[j][j] = "?"
        print("Step" + str(data.index(i)+1) + " of algorithm\\n")
        print(specific)
        print(general)
    gh = []
    for i in general:
        for j in i:
            if j != "?":
                gh.append(i)
                break
    print("Specific:\\n", specific)
    print("General:\\n", gh)
'''
