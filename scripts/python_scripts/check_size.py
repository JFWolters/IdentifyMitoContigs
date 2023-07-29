import sys

inFileName = sys.argv[1]

mean_size = float(sys.argv[2])

sd_size = float(sys.argv[3])



max_size = mean_size + 5*sd_size

min_size = mean_size - 5*sd_size

inFile = open(inFileName,"r")

lines = inFile.readlines()

inFile.close()

lines.pop(0) #remove header

lines = [line.rstrip("\n").split("\t") for line in lines]

at_least_one_true = False

for line in lines:
    gene=line[1]
    size=int(line[2])
    
    if size > min_size and size < max_size:
        at_least_one_true = True

if at_least_one_true == False:
    sys.stdout.write("TRUE")
else:
    sys.stdout.write("FALSE")
