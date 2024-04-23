x = float(input())
y = float(input())
list = [x+y,x-y,x/y,x*y,x//y]
print(list)
sort_num = sorted(list, reverse=True)
print(f"Воторое по величине число: {sort_num[1]}")