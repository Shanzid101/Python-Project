import random

secret_number = random.randint(1, 10)

print("Welcome to the the Number Guessing Game")
print("I am thinking of a numbert between 1 and 10. You have 3 chances to guess it.")

guess1 = int(input("Enter your first guess:"))
if guess1 == secret_number:
    print("Wow, Correct on the first try! You Won")
elif guess1 < secret_number:
    print("Too low. Try a large number.")
else:
    print("Too high! Try a smaller number.")


if guess1 != secret_number:
    guess2 = int(input("Enter your second guess:"))
    if guess2 == secret_number:
        print("Well done! You guesses it correctly on your second try.")
    elif guess2 < secret_number:
        print("Still too low! Try a larger number.")
    else:
        print("Still too high! Try a smaller number.")

    if guess2 != secret_number:
        guess3 = int(input("Enter your final guess:"))
        if guess3 == secret_number:
            print("Hurry! You guessed it correctly at the very last time.")
        else:
            print(f"Oh no! You lost! The correct number was:{secret_number}")

print("Game Over")
