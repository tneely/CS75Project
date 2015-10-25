# Genome Assembly via Eulerian Paths
Stephanie Her, Lauren Mitchell, Taylor Neely, Erin Connolly

## Background: Current DNA sequencing techniques are limited in the length of nucleotides in a sequence they can read in a given cycle. As a result, sequencing a large amount of DNA, such as that found in genomes, results in many small read fragments of lengths around 500-1000 nucleotides (CHECK). Genome assembly algorithms have been developed to take these produced fragments and align them to one another utilizing read overlaps. However, these algorithms have encountered several challenging obstacles; for instance, genomes contain large numbers of identical sequences. In our project, we will perform genome assembly using Eulerian paths as shown in Michael S. Waterman’s 2001 paper titled, “An Eulerian path approach to DNA fragment assembly.”
Problem: Given a set of short DNA reads from a sequenced genome with overlaps, assemble the reads in such a way as to fully recreate the genome.
## Code
Potential reader for FASTQ files: https://github.com/lh3/readfq/blob/master/readfq.py
Or just use BioPython in faster ways: http://news.open-bio.org/news/2009/09/biopython-fast-fastq/
To check our assembly accuracy: REAPR http://www.genomebiology.com/2013/14/5/R47/
The rest will be implemented from scratch in python
Eulerian path algorithm
Error correction
Graph data structure
Other code
Test cases
Short assembly on clean reads
Short assembly with errors (substitutions and gaps)
Short assembly with repeats
Short assembly with reversed reads
Gage dataset
## Analysis: We will compare our algorithm implementation to other genome assembly programs like CELERA and Python packages with implemented genome assembly functionality.
Work breakdown:
    Graph and Structure implementation: Erin, Stephanie
    Poster: Lauren, Erin, Stephanie, Taylor
    Testing: Stephanie, Lauren
    Designing Test Cases: Stephanie, Taylor
    Error Correction after working algorithm on “ideal” cases: Taylor, Lauren
    Eulerian Path Algorithm: Stephanie, Lauren, Taylor, Erin
    Comparative Analysis: Erin, Lauren
## References
Pevzner, Pavel A., Haixu Tang, and Michael S. Waterman. “An Eulerian Path Approach to DNA Fragment Assembly.” Proceedings of the National Academy of Sciences of the United States of America 98.17 (2001): 9748–9753. PMC. Web. 25 Oct. 2015.    
Possible datasets for testing: http://gage.cbcb.umd.edu/data/index.html

