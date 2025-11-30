#일정관리 프로그램
#일정추가
def append_job(date, job):
    if date not in calender:
        calender[date] = [job]
    else:
        calender[date].append(job)

#일정제거
def remove_job(date):
    if date in calender:
        job = input("제거할 일정을 입력하세요: ")
        if job in calender[date]:
            calender[date].remove(job)
            if calender[date] == []:
                print("해당 날짜의 모든 일정이 제거되어 날짜를 삭제합니다.")
                calender.pop(date)
        else:
            print("해당 일정이 없습니다.")
    else:
        print("해당 날짜에 일정이 없습니다.")

#일정확인
def check_job(date):
    if date in calender:
        print(f"{date}의 일정: {calender[date]}")
    else:
        print("해당 날짜에 일정이 없습니다.")

#전체일정확인
def check_all_jobs():
    for date, job in calender.items():
        print(f"{date}: {job}")

calender = {}
while True:
    num = int(input("1. 일정추가, 2. 일정제거, 3. 일정확인, 4. 전체일정확인, 5. 종료: "))
    if num == 1:
        date = input("날짜를 입력하세요: ")
        job = input("일정을 입력하세요: ")
        append_job(date, job)
    elif num == 2:
        date = input("제거할 일정의 날짜를 입력하세요: ")
        remove_job(date)
    elif num == 3:
        date = input("확인할 일정의 날짜를 입력하세요: ")
        check_job(date)
    elif num == 4:
        check_all_jobs()
    elif num == 5:
        print("일정관리 프로그램을 종료합니다.")
        break
    else:
        print("잘못된 입력입니다. 다시 시도하세요.")