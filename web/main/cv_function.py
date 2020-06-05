import os
import numpy as np
import json
import cv2
from django.conf import settings
from PIL import Image

import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/ML/libs')

import efficientnet
import classification_models
from .ML.libs.pconv_model import PConvUnet
import segmentation_models as sm

# from .ML.libs.segmentation import u_net, testImg_preprocessing
# from .ML.libs import efficientnet
# from .ML.libs import classification_models
# from .ML.libs import segmentation_models as sm

json_path = r'C:\Users\user\Desktop\goologin-272011-f2b7a9f953f2.json'

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

def init_resize(path):
    ori_img = cv2.imread(path)
    # ori_img = cv2.cvtColor(ori_img, cv2.COLOR_BGR2RGB)
    ori_img = cv2.resize(ori_img, dsize=(768, 1536), interpolation=cv2.INTER_AREA)

    cv2.imwrite(path, ori_img)
    print(path)



def predict_inp(oriURL, maskURL, inpURL):
    # 이미지 load
    # 1536, img_cols = 768

    mask_img = Image.open(maskURL)
    # mask_img = mask_img.resize((256, 512))
    mask_img = np.array(mask_img)

    # mask scale : 0 ~ 255 > 1 ~ 0
    mask_img = mask_img - 255
    mask_img[mask_img != 1] = 0
    mask_img = mask_img.reshape(1, mask_img.shape[0], mask_img.shape[1], mask_img.shape[2])

    ori_img = Image.open(oriURL)
    # ori_img = ori_img.resize((256, 512))
    ori_img = np.array(ori_img)
    ori_img = ori_img.reshape(1, ori_img.shape[0], ori_img.shape[1], ori_img.shape[2])

    ori_img = ori_img * 1. / 255

    # 원본 이미지에 마스크 입히기
    ori_img[mask_img == 0] = 1

    # 모델 load
    model = PConvUnet()
    model.load('./main/ML/model/inp/V3_0.73.h5')
    out_img = model.predict([ori_img, mask_img])

    pred = out_img[0, :, :, :]

    pred = pred * 255

    cv2.imwrite(settings.MEDIA_ROOT + '/' + inpURL, cv2.cvtColor(pred, cv2.COLOR_BGR2RGB))

    return print('inpaint')


# def predict_seg(oriURL, maskURL):
#     # ori_img 코드 추가
#     model = u_net()
#     ori_img = cv2.imread(oriURL)
#
#
#     X_test = testImg_preprocessing(ori_img)
#
#     model.load_weights('./main/ML/model/seg/548--0.9618.h5')
#     predict_img = model.predict(X_test, verbose = 1)
#
#     predict_img_t=np.squeeze(predict_img) # 차원축소
#     img = predict_img_t
#
#     # 1채널 -> 3 채널
#     new_img = np.stack((img,)*3, -1)
#     cv2.imwrite(settings.MEDIA_ROOT + '/' + maskURL ,new_img*255)
#
#     return print('segment')

import keras.backend as K


def predict_seg(oriURL, maskURL):
    # ori_img 코드 추가
    K.clear_session()
    ori_img = cv2.imread(oriURL)
    ori_img = cv2.cvtColor(ori_img, cv2.COLOR_BGR2RGB)
    ori_img = cv2.resize(ori_img, dsize=(256, 512), interpolation=cv2.INTER_AREA)

    ori_img = ori_img.reshape(1,512,256,3)

    BACKBONE = 'efficientnetb3'
    preprocess_input = sm.get_preprocessing(BACKBONE)
    ori_img = preprocess_input(ori_img)
    n_classes = 1
    model = sm.FPN(BACKBONE, classes=n_classes, activation='sigmoid')
    model.load_weights('./main/ML/model/seg/FPN_best_model_aug2.h5')
    # model.load_weights('gdrive/My Drive/Colab Notebooks/seg_exp/v2_pspnet/model/FPN_best_model.h5')

    # round는 0 ~ 1 사이의 0.6 0.7 0.1 등의 값들을 반올림 해줘서 0 or 1로 하기위함
    predict_img = model.predict(ori_img).round()

    predict_img = predict_img[..., 0].squeeze()

    # 1채널 -> 3 채널
    new_img = np.stack((predict_img,) * 3, -1)

    # to inpaint resize
    new_img = cv2.resize(new_img, dsize=(768, 1536), interpolation=cv2.INTER_AREA)

    cv2.imwrite(settings.MEDIA_ROOT + '/' + maskURL, new_img * 255)

    return print('segment')