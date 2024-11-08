from cs50 import get_string

text = get_string("Enter word: ")

letters = 0
words = 1
sentences = 0

for char in text:
    if char.isalpha():
        letters += 1
    elif char.isspace():
        words += 1
    elif char in ['.', '!', '?']:
        sentences += 1

if words > 0:
    L = letters / float(words) * 100

if sentences > 0:
    S = sentences / float(words) * 100

index = round(0.0588 * L - 0.296 * S - 15.8)

# Output the Grade Level
if index < 1:
    print("Before Grade 1")

elif index >= 16:
    print("Grade 16+")

else:
    print("Grade " + str(index))
