import sys

def sum(a, b):
    return a + b

print('Enter 1st number: ', end='', flush=True)
a = int(input())
print(a+2, flush=True)

print('Enter 2nd number: ', end='', flush=True)
b = int(input())
print(f'Sum of {a} and {b} is {sum(a, b)}', flush=True)