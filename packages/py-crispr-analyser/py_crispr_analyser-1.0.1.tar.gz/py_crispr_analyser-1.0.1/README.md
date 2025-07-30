# Python CRISPR Analyser

## Introduction

The Python CRISPR Analyser is a set of libraries and scripts that allows you to index [CRISPR](https://en.wikipedia.org/wiki/CRISPR)s from FASTA genome files and use the resulting index to find CRISPRS by using guide RNA (gRNA) sequences and to find off-targets for a given gRNA sequence. This code is a re-write of the original [CRISPR Analyser](https://github.com/htgt/CRISPR-Analyser) written in C/C++ with the intention that the Python version will be easier to use and extend.

For the efficient search for CRISPR off-targets, Python CRISPR Analyser supports CUDA on Linux platforms.

py-crispr-analyser uses Python 3.12 or later and is tested on Linux and MacOS. It has not been tested on Windows.

## Documentation

All documentation is online at [https://py-crispr-analyser.readthedocs.io/](https://py-crispr-analyser.readthedocs.io/).

## Copyright

Copyright (C) 2025 Genome Research Ltd.


## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

[Cellular Informatics Team](https://www.sanger.ac.uk/group/cellular-informatics/) at the [Wellcome Sanger Institute](https://www.sanger.ac.uk/), Hinxton, UK - [wge@sanger.ac.uk](mailto:wge@sanger.ac.uk)
