def age_calculator(age):
    if age <= 0:
        raise ValueError('Age cannot be zero or less')
    return 10 / age


try:
    age_calculator(-1)
except ValueError as error:
    print(error)
