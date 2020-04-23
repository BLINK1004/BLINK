import os
import numpy as np
import json
import cv2
json_path = '/Users/singwanghyeon/Source/git/goologin-272011-f2b7a9f953f2.json'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = json_path

# 업로드 단계
def detect_text(path):
    """Detects text in the file."""
    from google.cloud import vision

    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    # print(response)
    texts = response.text_annotations
    print('Texts:')

    ocr_list = []
    ocr_list.append([])
    for i,text in enumerate(texts):
        # x
        ocr_list[i].append(text.bounding_poly.vertices[0].x)
        # y
        ocr_list[i].append(text.bounding_poly.vertices[0].y)
        # width
        ocr_list[i].append(text.bounding_poly.vertices[1].x - text.bounding_poly.vertices[0].x)
        # height
        ocr_list[i].append(text.bounding_poly.vertices[2].y - text.bounding_poly.vertices[1].y)
        # txt
        ocr_list[i].append(text.description)
        ocr_list.append([])

    print(ocr_list)

    ocr_json = json.dumps(ocr_list)

    print(ocr_json)

    # ocr_decode = json.loads(ocr_json)

    # print(type(ocr_decode))

    return ocr_json

# user box confirm 단계
def pixel_change(src,inp,box):
    src_ = cv2.imread(src)
    inp_ = cv2.imread(inp)
    for b in box:
        # 주의 : slice 첫 파라미터는 세로축
        aa = inp_[b[1]:b[1]+b[3] , b[0]:b[0]+b[2]]
        src_[b[1]:b[1]+b[3] , b[0]:b[0]+b[2]] = aa
    return src_


# user box confirm 단계
def init_center(mask_path, box):
    img = cv2.imread(mask_path)
    img_shape = img.shape

    print('mask shape :',img_shape)
    input_img = img[box[1]:box[1] + box[3], box[0]:box[0] + box[2]]

    # 컨투어 검출 절차 : BGR > GRAY > Binary > findContour > drawContour
    temp = 255 - input_img
    test_img = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(test_img, 230, 255, 0)
    thresh = cv2.bitwise_not(thresh)

    contours, hierachy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # 컨투어 숫자, 넓이, 길이, 중심점 출력
    cnt = 0
    cx_arr = np.array([])
    cy_arr = np.array([])

    for i in contours:
        cnt += 1
        # 컨투어 특징 추출
        mmt = cv2.moments(i)

        # m10/m00, m01/m00  중심점 계산
        cx = int(mmt['m10'] / mmt['m00'])
        cx_arr = np.append(cx_arr, cx)
        cy = int(mmt['m01'] / mmt['m00'])
        cy_arr = np.append(cy_arr, cy)

        sp = mmt['m00']  # 넓이 추후 넓이관련 알고리즘 추가 예정

    center_x = int(np.mean(cx_arr))
    center_y = int(np.mean(cy_arr))

    dst = [box[0] + center_x, box[1] + center_y]
    print(dst)

    return dst

def find_txt(box, json_ocr):
    ocr_decode = json.loads(json_ocr)
    txt = ''
    for ocr in ocr_decode:
        try:
            if (box[0] < ocr[0]) and (ocr[0]<(box[0]+box[2])):
                if (box[1] < ocr[1]) and (ocr[1]<(box[1]+box[3])):
                    if (ocr[2]*ocr[3]) < 10000: # ocr box의 넓이가 10,000이하인것만 체크
                        txt += ocr[4]
        except:
            print('예외 처리')
    return txt

def im_read(path):
    img = cv2.imread(path)
    print('opencv 함수 정상 실행 확인',type(img))




