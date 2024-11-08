from cs50 import get_int


def luhn(number):
    total = 0
    num_digits = len(number)
    odd_even = num_digits % 2

    for i in range(num_digits):
        digit = int(number[i])
        if i % 2 == odd_even:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit

    return total % 10 == 0


number = get_int("Enter card number: ")
entire_number = str(number)
first_digit = entire_number[0]

# Length Check to see if it's valid
if len(entire_number) not in [13, 15, 16]:
    print("INVALID")
    exit(1)

# Luhn's Algorithm Check
if not luhn(entire_number):
    print("INVALID")
    exit(1)

# Check the card type
if first_digit == '4':
    print("VISA")
elif entire_number[:2] in ['51', '52', '53', '54', '55']:
    print("MASTERCARD")
elif entire_number[:2] in ['34', '37']:
    print("AMEX")
else:
    print("INVALID")
