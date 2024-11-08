from cs50 import get_int


def pyramids(height):
    for i in range(height):
        print(" " * (height-1-i) + "#" * (i+1) + "  " + "#" * (i+1))


# User input
height = get_int("Enter a number from 1 to 8: ")

# Making sure user input of "height" is no more than 8 and no less than 1
while height > 8 or height < 1:
    print("Enter a number from 1 to 8")
    height = get_int("Enter a number from 1 to 8: ")

# Printing the pyramids
pyramids(height)
