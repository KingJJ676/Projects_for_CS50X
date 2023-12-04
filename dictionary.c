// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <strings.h>

#include "dictionary.h"

int dict_size = 0;

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 675;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    //Hash word for hash value
    int word_index = hash(word);

    //Access the correlated linked list
    node *cursor = table[word_index];

    //Traverse linked list for word
    while(cursor != NULL)
    {
        if(strcasecmp(cursor->word, word) == 0)
        {
            return true;
        }
        else
        {
            cursor = cursor->next;
        }
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
        int first_letter = toupper(word[0]) - 'A' + 1; //a=1, z=26
        int second_letter;
        if (word[1] != '\0')
        {
            second_letter = toupper(word[1]) - 'A' + 1;
        }
        else
        {
            second_letter = 0;
        }

        int hash_index = 26*(first_letter - 1) + second_letter - 1;
        return hash_index;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    FILE *dict = fopen(dictionary, "r");
    if(dict == NULL)
    {
        return false;
    }

    //reading words one at a time
    int read_words = 0;
    do
    {
        //create a node to store read-in word
        node *cur_word = malloc(sizeof(node));
        if (cur_word == NULL)
        {
            return false;
        }

        read_words = fscanf(dict, "%s", cur_word -> word); //fscanf returns how many words is read (should be 1)

        if (read_words == 1)
        {
             //hash the read in word
            int hash_index = hash(cur_word -> word);

            //insert cur_word into hash table
            cur_word -> next = table[hash_index];
            table[hash_index] = cur_word;

            //add to size function
            dict_size ++;
        }
        else
        {
            free(cur_word);
        }

    }
    while(read_words != EOF);

    fclose(dict);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return dict_size;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    node *cursor;
    node *tmp;

    //loop over each bucket
    for(int i = 0; i <= N ; i++)
    {
         cursor = table[i];

        //free each linked list
        while (cursor != NULL)
        {
            tmp = cursor;
            cursor = cursor->next;
            free(tmp);
        }
    }

    return true;
}
