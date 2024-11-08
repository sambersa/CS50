#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char rotate(char c, int key);

int main(int argc, string argv[])
{
    // Making sure the program was run with just one command-line argument.
    if (argc != 2)
    {
        printf("Usage: ./caesar [key]\n");
        return 1;
    }

    // Making sure every character in argv[1] is a digit
    for (int j = 0; j < strlen(argv[1]); j++)
        if (!isdigit(argv[1][j]))
        {
            printf("You can only use digits.\n");
            return 1;
        }

    // Converting argv[1] from a string to an int
    int key = atoi(argv[1]);

    // Prompting the user for plaintext
    string prompt = get_string("plaintext:\n");

    // Encrypting the plaintext provided by the user
    printf("Ciphertext:\n");
    for (int i = 0, n = strlen(prompt); i < n; i++)
    {
        printf("%c", rotate(prompt[i], key));
    }
    printf("\n");
}

// Defining the function I declared above main
char rotate(char c, int key)
{
    if (isalpha(c))
    {
        char offset = islower(c) ? 'a' : 'A';
        return (c - offset + key) % 26 + offset;
    }
    else
    {
        return c;
    }
}
