#!/usr/bin/python
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import subprocess
import re

print("Simple Protein Analyser")
protein = input("Enter protein family: ").strip()
taxon   = input("Enter taxonomic group: ").strip()
term = f"{protein}(protein) AND {taxon}(organism)"
print("\nSearching NCBI for:", term)

retmax = input("Set the max IDs you want to search for: ")
term_url = term.replace(" ", "+")

# save IDs to a file 
os.system(f"wget -q -O ids.txt 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=protein&term={term_url}&retmax={retmax}&retmode=text'")

# Extract IDs from file
ids =[]
with open("ids.txt") as id:
 for line in id:
  line=line.strip()
  if line.startswith("<Id>") and line.endswith("</Id>"):
   ids.append(line[4:-5])

print(ids)

id_list = ",".join(ids)

os.system(f"wget -O sequences.fasta 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=protein&id={id_list}&rettype=fasta&retmode=text'")

print(f"FASTA sequences saved to sequences.fasta ({len(ids)} sequences)")

# Input and output files
fasta_input = "sequences.fasta"
aligned_output = "sequences_aligned.fasta"
plot_output = "plot.ps"

#un Clustal Omega to align sequences
subprocess.run([
    "clustalo",
    "-i", fasta_input,
    "-o", aligned_output,
    "--outfmt=fasta",
    "--force"
], check=True)
print(f"Aligned sequences saved to {aligned_output}")

#Run plotcon on the aligned sequences
subprocess.run([
    "plotcon",
    "-sequence", aligned_output,
    "-winsize", "10",
    "-graph", "ps",      # Use 'x11' to display interactively
    "-auto"], check=True
)
print(f"Conservation plot saved to {plot_output}")
