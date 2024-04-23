#Задача 1_2
x = float(input())
y = float(input())
print(f"Сумма:{x+y},Разность:{x-y},Деление:{x/y},Умножение:{x*y},Целочисленное деление:{x//y}")
print(f"Наибольшее: {max(x+y,x-y,x/y,x*y,x//y)}")