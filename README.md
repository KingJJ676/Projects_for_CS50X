# DNA
This program identifies who the provided DNA sequence belongs to by taking a sequence of DNA and a CSV file containing STR counts for a list of individuals. Per below:
```python
  $ python dna.py databases/large.csv sequences/5.txt
  Lavender
```

## How DNA profiling works
DNA is really just a sequence of molecules called nucleotides, arranged into a particular shape (a double helix). Every human cell has billions of nucleotides arranged in sequence. Each nucleotide of DNA contains one of four different bases: adenine (A), cytosine (C), guanine (G), or thymine (T). Some portions of this sequence (i.e., genome) are the same, or at least very similar, across almost all humans, but other portions of the sequence have a higher genetic diversity and thus vary more across the population.

One place where DNA tends to have high genetic diversity is in Short Tandem Repeats (STRs). An STR is a short sequence of DNA bases that tends to repeat consecutively numerous times at specific locations inside of a person’s DNA. The number of times any particular STR repeats varies a lot among individuals. In the DNA samples below, for example, Alice has the STR AGAT repeated four times in her DNA, while Bob has the same STR repeated five times.  

![image](https://github.com/KingJJ676/Projects-for-CS50/assets/130853046/d8c80eba-5f1c-4045-9c22-b7a426d7c94a)

sing multiple STRs, rather than just one, can improve the accuracy of DNA profiling. If the probability that two people have the same number of repeats for a single STR is 5%, and the analyst looks at 10 different STRs, then the probability that two DNA samples match purely by chance is about 1 in 1 quadrillion (assuming all STRs are independent of each other). So if two DNA samples match in the number of repeats for each of the STRs, the analyst can be pretty confident they came from the same person. 

## Introducing the files
- dna.py: where the main code is
- large.csv, small.csv: two databases containing the names and STRs of each person
- 1.txt ~ 18.txt: different DNA sequences for testing purposes
