import csv
import sys


def main():

    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        exit(1)

    # TODO: Read database file into a variable
    try:
        d = open(sys.argv[1], "r")
        db = csv.DictReader(d)
        STRs = db.fieldnames.copy()
        del STRs[0]

    except IOError:
        print("cannot read csv file")
        exit(1)

    # TODO: Read DNA sequence file into a variable
    try:
        s = open(sys.argv[2], "r")
        seq = s.read()

    except IOError:
        print("cannot read txt file")
        exit(1)

    # TODO: Find longest match of each STR in DNA sequence
    s_checklist = []
    for STR in STRs:
        times = longest_match(seq, STR)
        s_checklist.append(times)

    # TODO: Check database for matching profiles
    match = False
    for row in db:

        d_checklist = []

        name = row['name']
        del row['name']

        for n in row:
            row[n] = int(row[n])
            d_checklist.append(row[n])

        #compare checklist s and d
        if d_checklist == s_checklist:
            print(name)
            match = True
    if match == False:
        print('No match')

    #close files
    d.close()
    s.close()

    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
