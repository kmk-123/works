# 알파벳 소문자와 숫자중 3글자를 랜덤으로 선택하여 패스워드를 생성하는 프로그램
import random
a_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 1, 2, 3, 4, 5, 6, 7, 8, 9]
password = random.choices(a_list, k = 3)
print(password)
