from cs50 import get_float
import math

change = get_float("Change: ")
change = math.ceil(change * 100)

while change < 0:
    change = get_float("Change: ")

coin_counter = 0

while change > 0:
    if change >= 25:
        change = change - 25
        coin_counter += 1

    elif change >= 10:
        change = change - 10
        coin_counter += 1

    elif change >= 5:
        change = change - 5
        coin_counter += 1

    elif change >= 1:
        change = change - 1
        coin_counter += 1

print("Your change is:", coin_counter)
