# TODO:
# Make code find the all the right lines then get the information (maybe will improve performance)

# LINKS
# https://www.ncbi.nlm.nih.gov/genome/?term=Arabidopsis+thaliana
# https://www.ncbi.nlm.nih.gov/data-hub/taxonomy/3702/


import re
import json
import sys
import uuid


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
    gene_sequence, not_gene_sequence = "", ""
    genes, not_genes = [], []

    with open(file_path, 'r') as file:
        for line in file:
            split = line.split()

            if len(split) == 1 and split[0] == "//":
                valid_interval = False
                if not_gene_sequence != "":
                    not_genes.append(not_gene_sequence)
                    not_gene_sequence = ""

            if valid_interval:
                index = int(split[0])
                split.pop(0)
                line = "".join([str(s) for s in split])

                if gene_sequence == "":
                    if (len(indexes) == 0) or (len(indexes) > 0 and not indexes[0]["begin"] <= index + 60):
                        not_gene_sequence = "%s%s" % (not_gene_sequence, line)

                if len(indexes) > 0 and indexes[0]["begin"] <= index + 60:
                    cut = indexes[0]["begin"] - index

                    if cut <= 0:

                        if index + 60 >= indexes[0]["end"]:
                            cut = indexes[0]["end"] - index
                            gene_sequence = "%s%s" % (gene_sequence, line[:cut])
                            indexes.pop(0)
                            genes.append(gene_sequence)
                            gene_sequence = ""
                            not_gene_sequence = "%s%s" % (not_gene_sequence, line[cut:])

                        else:
                            gene_sequence = "%s%s" % (gene_sequence, line)

                    else:
                        gene_sequence = "%s%s" % (gene_sequence, line[cut:])
                        not_gene_sequence = "%s%s" % (not_gene_sequence, line[:cut])
                        not_genes.append(not_gene_sequence)
                        not_gene_sequence = ""

            if len(split) == 1 and split[0] == "ORIGIN":
                valid_interval = True

    return genes, not_genes


def write_genes_sequences(sequences):
    if len(sequences[0]) <= 0 and len(sequences[1]) <= 0:
        raise Exception('No sequence or gene found!')

    file_uuid = uuid.uuid4().hex

    if len(sequences[0]) > 0:
        with open("genes-%s.json" % file_uuid, "w") as outfile:
            json.dump(sequences[0], outfile)

    if len(sequences[1]) > 0:
        with open("not-genes-%s.json" % file_uuid, "w") as outfile:
            json.dump(sequences[1], outfile)


def run(file_path):
    try:
        print("\n")
        print("Extracting gene sequences from %s" % file_path)
        genes_indexes = find_valid_genes_indexes(file_path)
        sequences = arrange_sequence(file_path, genes_indexes)
        write_genes_sequences(sequences)
        print("\n")
        print("Gene extraction succeeded! %d sequences found. Check the .json file at the application folder." %
              len(sequences[0]))
        print("\n")

    except Exception as e:
        print("\n")
        print("Error! Could not extract genes!")
        print("%s : %s" % ("Error information", str(e)))
        print("\n")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        run(sys.argv[1])
    else:
        print("File path not found!")
