In this project, the user inputs a block of text, and the program computes the Coleman-Liau index to determine the text’s readability. The Coleman-Liau index formula relies on the average number of letters per 100 words and the average number of sentences per 100 words. The formula is as follows:

𝐿
L is the average number of letters per 100 words.
𝑆
S is the average number of sentences per 100 words.
After calculating the index, the program outputs an estimated grade level (e.g., “Grade 4” for 4th-grade level text), or it will indicate that the text is too simple or too complex (e.g., below grade 1 or above grade 16).

The program also ensures the text's validity and handles edge cases (e.g., very short text or punctuation). The user is prompted to input text, and the program gives the readability grade based on the input.

Languages and Technologies Used:

Python: The main language used to implement the logic for counting letters, words, and sentences in the text and applying the Coleman-Liau index formula. The program uses basic string manipulation, loops, and conditional logic to analyze and process the input text.
