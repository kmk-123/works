#이름과 점수를 받아 총점과 평균 출력하
st1 = []
st2 = []
st3 = []
st = [st1, st2, st3]

for i in range(3):
    st[i].append(input("이름을 입력해주세요: "))
    st[i].append(int(input("국어 점수를 입력해주세요: ")))
    st[i].append(int(input("영어 점수를 입력해주세요: ")))
    st[i].append(int(input("수학 점수를 입력해주세요: ")))

print("성명\t국어\t영어\t수학\t총점\t평균")
for i in range(3):
    st[i].append(st[i][1] + st[i][2] + st[i][3])
    st[i].append(st[i][4] / 3)
    for g in range(6):
      print(f"{st[i][g]}\t", end="")
    print("")
print("=========================================")
print(f"총점/평균\t{st1[4]}/{st1[5]}\t{st2[4]}/{st2[5]}\t{st3[4]}/{st3[5]}")
    
