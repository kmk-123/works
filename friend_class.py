# 리스트를 사용하여 친구 이름, 번호, 주소를 관리하는 프로그램
# 같은 이름이 여러 개인 경우 사용자가 그 중에서 골라서 삭제
class Friend:
    def __init__(self):
        self.friend_list = []
    
    #1. 새친구등록(동명이인 가능)
    def insert_friend(self):
        name = input("이름을 입력하세요: ")
        phone = input("전화번호를 입력하세요: ")
        address = input("주소를 입력하세요: ")
        self.friend_list.append([name, phone, address])

    #2. 이름으로 검색하기
    def search_friend_name(self):
        name = input("검색할 이름을 입력하세요")
        found = False
        for key in self.friend_list:
            if key[0] == name:
                print(f"이름: {key[0]}, 전화번호: {key[1]}, 주소: {key[2]}")
                found = True
        if found == False:
            print("해당 이름의 친구가 없습니다.")

    #3. 주소로 검색하기
    def search_friend_address(self):
        address = input("검색할 주소를 입력하세요: ")
        found = False
        for key in self.friend_list:
            if key[2] == address:
                print(f"이름: {key[0]}, 전화번호: {key[1]}, 주소: {key[2]}")
                found = True
        if found == False:
            print("해당 주소의 친구가 없습니다.")

    #4. 이름으로 친구 찾고 내용 수정하기
    def update_friend(self):
        friend_re = [] # 찾은 친구 출력용 리스트
        index_re = [] # 찾은 친구의 인덱스 저장용 리스트
        search_name = input("수정할 친구의 이름을 입력하세요: ")
        found = False
        idx = 0
        for key in self.friend_list:
            if key[0] == search_name:
                friend_re.append(key)
                index_re.append(idx)
                found = True
            idx += 1
        if found == False:
            print("해당 이름의 친구가 없습니다.")
            return
        
        print("----- 검색 결과 -----")
        i = 1
        for name in friend_re:
            print(f"{i}. 이름: {name[0]}, 전화번호: {name[1]}, 주소: {name[2]}")
            i += 1
        
        if len(friend_re) > 1: # 동명이인이 있는 경우
            num = int(input("수정할 친구의 순서를 입력하세요: "))
        else:
            num = 1
        
        choice = int(input("수정할 항목을 선택하세요 (1. 이름, 2. 전화번호, 3. 주소): "))
        
        list_idx = index_re[num - 1]
        if choice == 1:
            new_name = input("새 이름을 입력하세요: ")
            self.friend_list[list_idx][0] = new_name
        elif choice == 2:
            new_phone = input("새 전화번호를 입력하세요: ")
            self.friend_list[list_idx][1] = new_phone
        elif choice == 3:
            new_address = input("새 주소를 입력하세요: ")
            self.friend_list[list_idx][2] = new_address

    #5. 이름으로 친구 찾고 삭제하기
    def delete_friend(self):
        friend_re = []
        index_re = []
        search_name = input("삭제할 친구의 이름을 입력하세요: ")
        found = False
        idx = 0
        for key in self.friend_list:
            if key[0] == search_name:
                friend_re.append(key)
                index_re.append(idx)
                found = True
            idx += 1
        if found == False:
            print("해당 이름의 친구가 없습니다.")
            return
        
        print("----- 검색 결과 -----")
        i = 1
        for key in friend_re:
            print(f"{i}. 이름: {key[0]}, 전화번호: {key[1]}, 주소: {key[2]}")
            i += 1
        
        if len(friend_re) > 1:
            num = int(input("삭제할 친구의 순서를 입력하세요: "))
        else:
            num = 1
        
        del_idx = index_re[num - 1]
        self.friend_list.pop(del_idx)
        print("친구가 삭제되었습니다.")

myFriend = Friend()
while True:
    num = int(input("1. 새친구등록, 2. 이름검색, 3. 주소검색, 4. 친구수정, 5. 친구삭제, 6. 종료: "))
    if num == 1:
        myFriend.insert_friend()
    elif num == 2:
        myFriend.search_friend_name()
    elif num == 3:
        myFriend.search_friend_address()
    elif num == 4:
        myFriend.update_friend()
    elif num == 5:
        myFriend.delete_friend()
    elif num == 6:
        print("친구관리 프로그램을 종료합니다.")
        break
    else:
        print("잘못된 입력입니다. 다시 시도하세요.")