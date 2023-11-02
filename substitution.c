#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int check_key_valid(int argc, string argv[]);
char encrypt(string pt, string argv[]);

int main(int argc, string argv[])
{
    // check key valid
    check_key_valid(argc, argv);

    // get plaintext(case)
    string pt = get_string("Plaintext: ");

    // encrypt text(preserve case)
    printf("ciphertext:");
    encrypt(pt, argv);
    printf("\n");
    return 0;
}

//////////////
char encrypt(string pt, string argv[])
{
    char ct[strlen(pt) + 1];
    int n = 0;
    int L = strlen(pt);

    for (int i = 0; i < L; i++)
    {
        // uppercase
        if (pt[i] > 64 && pt[i] < 91)
        {
            n = pt[i] - 65; //第幾個
            ct[i] = toupper(argv[1][n]);
        }

        // lowercase
        else if (pt[i] > 96 && pt[i] < 123)
        {
            n = pt[i] - 97; //第幾個
            ct[i] = tolower(argv[1][n]);
        }

        // non-alphabetical
        else
        {
            ct[i] = pt[i];
        }

        printf("%c", ct[i]);
    }

    return 0;
}

///////////////
int check_key_valid(int argc, string argv[])
{
    // check for 1 argument
    if (argc != 2)
    {
        printf("Usage: ./subtitution key\n");
        exit(1);
    }

    // check for 26 characters
    if (strlen(argv[1]) != 26)
    {
        printf("Key must contain 26 characters\n");
        exit(1);
    }

    // check for only alphabets
    for (int i = 0; i < strlen(argv[1]); i++)
    {
        if (isdigit(argv[1][i]) || ispunct(argv[1][i]) || isspace(argv[1][i]))
        {
            printf("Key must only contain alphabetic characters\n");
            exit(1);
        }
    }

    // check if every letter appears exactly once
    int alpha[26] = {0};
    for (int i = 0; i < 26; i++)
    {
        if (alpha[(tolower(argv[1][i]) - 97)] == 1)
        {
            printf("Every letter has to appear exactly once\n");
            exit(1);
        }
        else
        {
            alpha[(tolower(argv[1][i]) - 97)] = 1;
        }
    }

    for (int i = 0; i < 26; i++)
    {
        if (alpha[i] != 1)
        {
            printf("Every letter has to appear exactly once\n");
            exit(1);
        }
    }

    // all pass
    return 0;
}