 #include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

// Functions that will be defined later on in the code
int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    // Ask user for input in terms of text
    string text = get_string("Enter text:\n ");

    // Variables to count letters, words and sentences in text written by user
    int letters = count_letters(text);
    int words = count_words(text);
    int sentences = count_sentences(text);

    // Computing the Coleman-Liau Index
    float L = (letters / (float) words) * 100;
    float S = (sentences / (float) words) * 100;

    float index_round = 0.0588 * L - 0.296 * S - 15.8;
    int index = round(index_round);

    // Output the Grade Level
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
    return 0;
}

// Counting the amount of letters in text written.
int count_letters(string text)
{
    int letters = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (isalpha(text[i]))
        {
            letters++;
        }
    }
    return letters;
}

// Counting the amount of words in the text, while paying special attention to where spaces are in
// the text so that we can get an accurate print
int count_words(string text)
{
    int words = 0;
    for (int i = 1, n = strlen(text); i < n; i++)
    {
        if (text[i] == ' ') // Check if the current character is a space
        {
            words++;
        }
    }
    return words + 1; // Increment words by 1
}

// Counting the amount of sentences in the text, while paying special attention to '.' '!' and '?'
// because those usually indicate end of sentence.
int count_sentences(string text)
{
    int sentences = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            sentences++;
        }
    }
    return sentences;
}
