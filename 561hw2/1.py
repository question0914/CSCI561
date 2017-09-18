from decimal import Decimal


def my_round(data, precise):
    sign = True if data < 0 else False
    updated_data = -data if sign else data
    updated_data = updated_data + 1e-8
    decimal = updated_data - int(updated_data)
    num = int(decimal * (10 ** (precise + 1)))
    if num % 10 >= 5:
        num += 10
    num = num / 10
    result = num / (10.0 ** (precise)) + int(updated_data)
    return -result if sign else result
with open("input.txt", "r")as infile:
    data = infile.read()

line = data.splitlines()

nums = line[0].split(",")
count = 0.0
sum = 0.0
for num in nums:
    count += 1
    sum += int(num)

print(int(my_round(sum/count, 0)))






