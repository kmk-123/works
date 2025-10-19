# 사각형 그리기
import turtle as t

colors = ["red", "purple", "blue", "green", "yellow", "orange"]
angle = 89
length = 10

t.shape("turtle")
t.speed(0)
t.width(3)

while length < 500:
    t.pencolor(colors[length%6])
    t.forward(length)
    t.right(angle)
    length += 5
# 배열 안의 색의 종류가 6개 -> length % 6
# 길이의 증가가 5여서 수가 1씩 줄어듬 

t.done()
