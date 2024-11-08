#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int main(int argc, string argv[])
{

    // Making sure there's only 2 inputs at the command line
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    // Making sure only alphabetic characters are entered
    bool seen[26] = {false};
    for (int i = 0; i < 26; i++)
    {
        char c = tolower(argv[1][i]);
        if (!isalpha(c))
        {
            printf("Alphabetic characters only.\n");
            return 1;
        }

        // Making sure the key entered is only 26, nothing less, nothing more.
        int len = strlen(argv[1]);
        if (len != 26)
        {
            printf("Key must contain 26 characters\n");
            return 1;
        }

        if (seen[c - 'a']++)
        {
            printf("Key must contain unique characters only\n");
            return 1;
        }
    }
    // Prompt the user for plaintext
    string plaintext = get_string("plaintext:\n");
    string cipher = plaintext;

}




