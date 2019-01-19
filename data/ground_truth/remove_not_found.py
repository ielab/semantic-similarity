import fileinput

nf = [line.strip() for line in open("not_found")]

for line in fileinput.input():
    items = line.strip().split("\t")
    cui1 = items[1]
    cui2 = items[3]

    if cui1 in nf or cui2 in nf:
        print line.strip(), "not found"
    else:
        print line.strip()