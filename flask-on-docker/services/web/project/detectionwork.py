import easyocr
import cv2
from algorithm import Algorithm                 # 개인정보 탐지 알고리즘 관련


# easyOCR 관련
class GtnOcr():
    ALLOWED_EXTENSIONS = { 'png', 'jpg', 'jpeg'}
    reader = easyocr.Reader(['ko', 'en'], gpu=False)
    
    # 파일 확장자 검증 함수
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in EasyOcr.ALLOWED_EXTENSIONS
  
    # 인식 텍스트 좌표값 추출 함수 / ocr결과, 값저장 사전, 검증 리스트1, 검증 리스트2, 검증 리스트3, 카운팅 변수1, 카운팅 변수2
    def get_coordinate(result, dict1, list1, list2, list3, cnt1, cnt2):
        # bounding box 좌표, 텍스트, 검증(1에 가까울수록 정확도 높음)
        # KITTY, VOC 형식
        for (bbox, text, prob) in result:
            # top left, top right, bottom right, bottom left
            (tl, tr, br, bl) = bbox
            tl = (int(tl[0]), int(tl[1]))
            tr = (int(tr[0]), int(tr[1]))
            br = (int(br[0]), int(br[1]))
            bl = (int(bl[0]), int(bl[1]))

            if Algorithm.is_idcard(text, list1):
                dict1.update({"tag": "idcard"})

            if Algorithm.is_license(text, list2):
                dict1.update({"tag": "license"})

            if Algorithm.is_registration(text, list3):
                dict1.update({"tag": "registration"})

            if Algorithm.jumin_check(text):
                cnt1 += 1
                dict1.update({"jumin {}".format(cnt1): [{'x': tl[0], 'y':tl[1]}, {'x': br[0], 'y':br[1]}]})

            if Algorithm.licensenum_check(text):
                cnt2 += 1
                dict1.update({"license {}".format(cnt2): [{'x': tl[0], 'y':tl[1]}, {'x': br[0], 'y':br[1]}]})

        return dict1


# OpenCV 관련
class PreProcessing():
    block_size = 13                 # 블럭 사이즈(이미지의 등분)
    C = 7                           # 차감 상수

    # 적응형 thresholding - 이진화 및 음영 제거
    def adapted_th(image):
        origin = cv2.imread(image, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(origin, cv2.COLOR_BGR2RGB)
        th_ad = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, PreProcessing.block_size, PreProcessing.C)
        result = cv2.cvtColor(th_ad, cv2.COLOR_BGR2RGB)

        return result