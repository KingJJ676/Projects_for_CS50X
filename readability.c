#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    //get text from user
    string text = get_string("Text: ");

    //count letter, words, sentences
    int letters = count_letters(text);
    int words = count_words(text);
    int sentences = count_sentences(text);

    //determine Coleman-Liau index
    float L = ((float) letters / words) * 100.0;
    float S = ((float) sentences / words) * 100.0;
    int index = round((0.0588 * L) - (0.296 * S) - 15.8);

    //print result
    if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }

}














//////////////////////////////
int count_letters(string text)
{
    int count = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if (isupper(text[i]) | islower(text[i]))
        {
            count++;
        }
    }
    return count;
}
///
int count_words(string text)
{
    int count = 1;
    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] == ' ')
        {
            count++;
        }
    }
    return count;
}
///
int count_sentences(string text)
{
    int count = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] == '.' | text[i] == '!' | text[i] == '?')
        {
            count++;
        }
    }
    return count;
}
//////////////////////////////