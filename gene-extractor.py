# TODO:
# Make code find the all the right lines then get the information

# LINKS
# https://www.ncbi.nlm.nih.gov/genome/?term=Arabidopsis+thaliana
# https://www.ncbi.nlm.nih.gov/data-hub/taxonomy/3702/


import re
import json
import sys


def find_valid_genes_indexes(file_path):
    if file_path is None or file_path == "":
        raise Exception('File path must be given!')

    extension = file_path.split(".")[-1:]
    if len(extension) <= 0 or extension[0] != "gbff":
        raise Exception('File extension must be .gbff!')

    genes = []
    valid = False

    with open(file_path, 'r') as file:
        for line in file:
            split = line.split()

            if len(split) == 2 and split[0] == "gene":

                if len(genes) > 0 and not valid:
                    genes.pop()

                valid = False
                indexes = re.findall(r'\d+', split[1])

                if len(indexes) == 2:
                    genes.append({"begin": int(indexes[0]), "end": int(indexes[1])})

            if len(split) == 2 and split[0] == "CDS":
                valid = True

    return genes


def arrange_sequence(file_path, indexes):
    if len(indexes) <= 0:
        raise Exception('No valid gene found!')

    valid_interval, valid_gene = False, False
    sequence = ""
    sequences = []

    with open(file_path, 'r') as file:
        for line in file:
            split = line.split()

            if len(split) == 1 and split[0] == "//":
                valid_interval = False

            if valid_interval:
                index = int(split[0])

                if len(indexes) > 0 and indexes[0]["begin"] <= index + 60:
                    split.pop(0)
                    line = "".join([str(s) for s in split])
                    cut = indexes[0]["begin"] - index

                    if cut <= 0:

                        if index + 60 >= indexes[0]["end"]:
                            cut = indexes[0]["end"] - index
                            sequence = "%s%s" % (sequence, line[:cut])
                            indexes.pop(0)
                            sequences.append(sequence)
                            sequence = ""

                        else:
                            sequence = "%s%s" % (sequence, line)

                    else:
                        sequence = "%s%s" % (sequence, line[cut:])

            if len(split) == 1 and split[0] == "ORIGIN":
                valid_interval = True

    return sequences


def write_genes_sequences(sequences):
    if len(sequences) <= 0:
        raise Exception('No sequence found!')

    with open("genes.json", "w") as outfile:
        json.dump(sequences, outfile)


def run(file_path):
    try:
        genes_indexes = find_valid_genes_indexes(file_path)
        sequences = arrange_sequence(file_path, genes_indexes)
        write_genes_sequences(sequences)
        print("Gene extraction succeeded! %d sequences found. Check the .json file at the application folder." %
              len(sequences))

    except Exception as e:
        print("Error! Could not extract genes!")
        print("%s : %s" % ("Error information", str(e)))


if __name__ == '__main__':
    run(sys.argv[1])
