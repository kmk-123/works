import random as r

num1 = r.randint(1, 99)
num2 = r.randint(1, 99)
cal = r.randint(1, 4)

if cal == 1:
    print(f"{num1} + {num2} = ?")
    cal1 = num1 + num2
elif cal == 2:
    print(f"{num1} - {num2} = ?")
    cal1 = num1 - num2
elif cal == 3:
    print(f"{num1} * {num2} = ?")
    cal1 = num1 * num2
else:
    print(f"{num1} / {num2} = ?")
    cal1 = num1 / num2

inp = int(input("입력 : "))

if cal1 == inp:
    print("정답")
else:
    print("오답")

