#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Defining the MAX number of candidates
#define MAX 9

// Candidates names & votes
typedef struct
{
    string name;
    int votes;
} candidate;

// Array of candidates
candidate candidates[MAX];

// Number of candidates
int candidate_count;

// Function Prototypes
bool vote(string name);
void print_winner(void);

int main(int argc, string argv[])
{
    // Checking for invalid usage

    if (argc != 2)
    {
        printf("Usage: plurality [candidate ...]\n");
        return 1;
    }

    // Populate Array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 1;
    }

    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
    }

    // Prompt the user for the number of voters & Who they want to vote for. If name doesn't exist,
    // return error message
    int voter_count = get_int("Number of voters:\n");

    for (int i = 0; i < voter_count; i++)
    {
        string name = get_string("Vote:\n");

        if (!vote(name))
        {
            printf("Invalid Vote.\n");
        }
    }
}

// Check if entered name is found, and if it is, increment their votes by 1
bool vote(string name)
{
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(name, candidates[i].name) == 0)
        {
            candidates[i].votes++;
            return true;
        }
    }
    return false;
}

// Update the total votes & Print the winner
void print_winner(void)
{
    int maxvotes = 0;
    for (int i = 0; i < candidate_count; i++)
    {
        if (candidates[i].votes > maxvotes)
        {
            maxvotes = candidates[i].votes;
        }
    }

    for (int i = 0; i < candidate_count; i++)
    {
        if (candidates[i].votes == maxvotes)
        {
            printf("%s\n", candidates[i].name);
        }
    }
}
