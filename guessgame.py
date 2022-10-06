import random
from random import randint
number = random.randint(0, 10)
guess_limit = 5
guess_count = 0
while guess_count < guess_limit:
    guess = int(input('Guess a random number between 0 and 10: '))
    guess_count += 1
    if guess > number:
        print('You guessed high')
    elif guess < number:
        print('You guess low')
    elif guess == number:
        print(f'you guessed right after {guess_count} attempts')

        break
    if guess_count == guess_limit:
        print(f'you have made {guess_count} attempts and failed')

print('Done')
