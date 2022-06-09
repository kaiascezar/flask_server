import re


# 텍스트 기반 - 쪼개진 단어를 조합하여 개인정보 유형 파악
class Algorithm():    
    
    # 주민등록증
    def is_idcard(text, verif):
        word = list(text)
        for i in word:
            if verif == [1,1,1,1,1]:
                break;
            if i == "주":
                verif[0] = 1
            if i == "민":
                verif[1] = 1
            if i == "등":
                verif[2] = 1
            if i == "록":
                verif[3] = 1
            if i == "증":
                verif[4] = 1

        if verif == [1,1,1,1,1]:
            return True
        else:
            return False

    # 운전면허증
    def is_license(text, verif):
        word = list(text)
        for i in word:
            if verif == [1,1,1,1,1]:
                break;
            if i == "운":
                verif[0] = 1
            if i == "전":
                verif[1] = 1
            if i == "면":
                verif[2] = 1
            if i == "허":
                verif[3] = 1
            if i == "증":
                verif[4] = 1

        if verif == [1,1,1,1,1]:
            return True
        else:
            return False

    # 주민등록등본
    def is_registration(text, verif):
        word = list(text)
        for i in word:
            if verif == [1,1,1,1,1,1,1,1,1]:
                break;
            if i == "주":
                verif[0] = 1
            if i == "민":
                verif[1] = 1
            if i == "등":
                verif[2] = 1
            if i == "록":
                verif[3] = 1
            if i == "표":
                verif[4] = 1
            if i == "본":
                verif[5] = 1
            if i == "세":
                verif[6] = 1
            if i == "대":
                verif[7] = 1
            if i == "주":
                verif[8] = 1

        if verif == [1,1,1,1,1,1,1,1,1]:
            return True
        else:
            return False

    # 주민번호 정규식 판단
    def jumin_check(input):
        ssn = re.compile("^(?:[0-9]{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[1,2][0-9]|3[0,1]))-[1-4][0-9]{6}$")

        if ssn.match(input):
            return True
        else:
            return False

    # 운전면허번호 정규식 판단
    def licensenum_check(input):
        drv = re.compile("^(?:[0-9]{1,2})-[0-9]{2}-[0-9]{6}-[0-9]{2}$")
        # drv = re.compile("?<=[^0-9a-zA-Z])(\d{2}[\s-:\.])(\d{6}[\s-:\.])(\d{2})(?=[^0-9a-zA-Z]")
        if drv.match(input):
            return True
        else:
            return False
