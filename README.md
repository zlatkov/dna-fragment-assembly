# dna-fragment-assembly

Create a computer program that assembles a DNA structure from given DNA fragments.

Follow the algorithm described in the article "DNA Paired Fragment Assembly Using Graph Theory". The article is listed in the literature for the course.

Create a prefix tree that uses an alphabet set by the nucleotide bases A, C, G, T.
Create a function that writes a DNA fragment to the tree.
For each edge of the tree, assign a weight that corresponds to the number of DNA fragments that use that edge.
Create a function that extracts from the tree all the paths that have an edge weight not less than a predefined parameter (consensus).