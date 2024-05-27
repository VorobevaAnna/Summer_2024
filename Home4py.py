# %%
def simple_calculator(expression):
    operand1, operator, operand2 = expression.split()
    
    operand1 = int(operand1)
    operand2 = int(operand2)
    
    if operator == '+':
        result = operand1 + operand2
    elif operator == '-':
        result = operand1 - operand2
    elif operator == '*':
        result = operand1 * operand2
    elif operator == '/':
        if operand2 == 0:
            return "Деление на ноль"
        result = operand1 / operand2
    else:
        return "Неизвестная операция"
    return result
strr = input()
print(simple_calculator(strr))




# %%
def print_spiral(n):
    d = {}  
    x, y = 0, 0  
    dx, dy = 1, 0  
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]  
    direction_index = 0  

    for i in range(1, n * n + 1):
        d[(x, y)] = i  
        nx, ny = x + dx, y + dy
        if (nx, ny) in d or nx < 0 or nx >= n or ny < 0 or ny >= n:
            direction_index = (direction_index + 1) % 4
            dx, dy = directions[direction_index]
            nx, ny = x + dx, y + dy
        x, y = nx, ny
    for i in range(n):
        for j in range(n):
            print(f"{d[(j, i)]:4}", end=' ')
        print()
n = int(input())
print_spiral(n)


# %%
import string

def clean_string(s):
    return ''.join(filter(str.isalpha, s)).lower()

def anagrams(s1, s2):
    cleaned_s1 = sorted(clean_string(s1))
    cleaned_s2 = sorted(clean_string(s2))
    return cleaned_s1 == cleaned_s2

p1 = input()
p2 = input()
print(anagrams(p1, p2))  


