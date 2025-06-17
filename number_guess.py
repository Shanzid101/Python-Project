import random

high_range= input("Write the top range:")
if high_range.isdigit():
    top_range = int(high_range)
else:
    print("Please enter a valid number")
    quit()


random_number= random.randint(0,top_range)
guess =  0

while True:
    guess += 1
    user_guess = input("Write your guess number:")
    if user_guess.isdigit():
        user_guess = int(user_guess)
    else:
        print("Please enter a number greater than or equal to 0")
        quit()

    if user_guess == random_number:
        print("You guess the right number!")
        break
    else:
        print("Sorry, you didn't guess the right number, try again!")
        continue
print("You guess", guess, "times")
