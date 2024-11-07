// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 140999;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    int hash_word = hash(word);
    node *trav = table[hash_word];

    while (trav != NULL)
    {
        if (strcasecmp(word, trav->word) == 0)
        {
            return true;
        }
        trav = trav->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    unsigned int hash_value = 0;
    int length = strlen(word);

    for (int i = 0; i < length; i++)
    {
        hash_value = (hash_value * 37 + toupper(word[i])) % N;
    }
    return hash_value;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    printf("Load function called\n");
    // Open the dictionary file
    FILE *dictionary_file = fopen(dictionary, "r");

    if (dictionary_file == NULL)
    {
        printf("Dictionary could not be opened.\n");
        return false;
    }

    // Read each word in the file
    char word[100];
    while (fscanf(dictionary_file, "%s", word) != EOF)
    {
        printf("Loading word: %s\n", word);
        // Add each word to the hash table
        node *word_read = malloc(sizeof(node));

        if (word_read == NULL)
        {
            printf("Error allocating memory for word_read.");
            return false;
        }

        else if (word_read != NULL)
        {
            strcpy(word_read->word, word);
            int index = hash(word);

            word_read->next = table[index];
            table[index] = word_read;
        }
    }

    // Close the dictionary file
    fclose(dictionary_file);
    // TODO
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    unsigned int counter = 0;

    for (int i = 0; i < N; i++)
    {
        node *trav = table[i];
        while (trav != NULL)
        {
            counter++;
            trav = trav->next;
        }
    }
    return counter;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *tmp = table[i];
        while (tmp != NULL)
        {
            node *next = tmp->next;
            free(tmp);
            tmp = next;
        }
    }

    // TODO
    return true;
}
