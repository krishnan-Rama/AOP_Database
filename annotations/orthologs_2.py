#!/usr/bin/env python

from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML

# Your query sequence
query_sequence = "MFSSIILFFVVSSSSAVYSAPKSQLTLQLYYEGFCPFCHSFVELQLYPGYQKLGDSFLVELVPYGKAVYSKAEDGTVSFNCQHGPSECLLNRIHACAINQKPAQADILKFVYCDLSQSTISNTSKELLGIAQTCAQDSNISFDKITTCINSSLSDELLLKYAHQQEKLQPSLRFVPTIRFNGVYNKTLEDDVRANLVQTVCNLLNDEPSVCNNVLSHKVLPQESTIPKNMFLNN"

# Perform a BLAST search against the NCBI nr database
result_handle = NCBIWWW.qblast("blastp", "nr", query_sequence)

# Parse the BLAST results
blast_record = NCBIXML.read(result_handle)

# Print out information for the top hits
print(f"Top hits for your query sequence:\n")
for alignment in blast_record.alignments[:10]:  # Limit to top 10 results
    for hsp in alignment.hsps:
        print(f"Sequence: {alignment.title}")
        print(f"Length: {alignment.length}")
        print(f"E-value: {hsp.expect}")
        print(f"Align length: {hsp.align_length}")
        print(f"Identities: {hsp.identities}")
        print(f"Gaps: {hsp.gaps}")
        print(f"Query start: {hsp.query_start} Subject start: {hsp.sbjct_start}")
        print(f"Query end: {hsp.query_end} Subject end: {hsp.sbjct_end}")
        print(f"Query: {hsp.query[0:75]}...")
        print(f"Match: {hsp.match[0:75]}...")
        print(f"Subject: {hsp.sbjct[0:75]}...\n")

# Close the result handle
result_handle.close()

