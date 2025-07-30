# Introduction

The Python CRISPR Analyser is a set of libraries and scripts that allows you to index CRISPRs from FASTA genome files and use the resulting index to find CRISPRS from guide RNA (gRNA) sequences and to find off-targets for a given CRISPR.

## About

This tool is a re-write of the original [CRISPR Analyser](https://en.wikipedia.org/wiki/CRISPR) written in C++ with the intention that the Python version will be easier to use and extend.
The following workflow is supported:

- **Gathering** CRISPRs from a FASTA file specifying the PAM sequence and the length of the gRNA,
- **Indexing** the CRISPRs into a binary formatted index for fast search,
- **Searching** for CRISPRs by using a gRNA sequence,
- **Aligning** the gRNA sequence to the CRISPRs to find off-targets.

Furthermore library functions can be used directly in a user's own code to perform the above tasks.

If you use this code in any scientific work please cite:

*Bin Shen, Wensheng Zhang, Jun Zhang, Jiankui Zhou, Jianying Wang, Li Chen, Lu Wang, Alex Hodgkins, Vivek Iyer, Xingxu Huang & William C Skarnes (2014) Efficient genome modification by CRISPR-Cas9 nickase with minimal off-target effects. doi:10.1038/nmeth.2857*
