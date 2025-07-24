import random

print("Welcome to the Number Guessing Game!")

# Choosing level
print("\nChoose Difficulty Level:")
print("1. Easy (1 to 10)")
print("2. Medium (1 to 50)")
print("3. Hard (1 to 100)")

level = input("Enter your choice (1/2/3): ")

# Set range
if level == '1':
    max_num = 10
elif level == '2':
    max_num = 50
elif level == '3':
    max_num = 100
else:
    print("Invalid choice! Defaulting to Easy level.")
    max_num = 10

# Generate random number
secret_number = random.randint(1, max_num)
attempts = 0

print(f"\nI have picked a number between 1 and {max_num}. Try to guess it!")

while True:
    guess = input("Enter your guess: ")

    # Check if input is a number
    if not guess.isdigit():
        print("Please enter a valid number.")
        continue

    guess = int(guess)
    attempts += 1

    if guess < secret_number:
        print("Too low! Try again.")
    elif guess > secret_number:
        print("Too high! Try again.")
    else:
        print(f"Congratulations! You guessed it in {attempts} attempts.")
        break
