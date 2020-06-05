import os
import numpy as np
import json
import cv2
from django.conf import settings
from PIL import Image

import keras.backend as K
import tensorflow as tf

import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/ML/libs')

# from .ML.libs.pconv_model import PConvUnet
from .ML.libs.ganinp_model import InpaintNet
import segmentation_models as sm


# from .ML.libs.segmentation import u_net, testImg_preprocessing
# from .ML.libs import efficientnet
# from .ML.libs import classification_models
# from .ML.libs import segmentation_models as sm

json_path = '/Users/singwanghyeon/Source/git/goologin-272011-f2b7a9f953f2.json'

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = json_path

# 두개의 모델을 각각 다른 그래프, 다른 세션에 초기화 해야함.

graph1 = tf.Graph()
with graph1.as_default():
    session1 = tf.Session()
    with session1.as_default():
        BACKBONE = 'efficientnetb3'
        preprocess_input = sm.get_preprocessing(BACKBONE)
        n_classes = 1
        s_model = sm.FPN(BACKBONE, classes=n_classes, activation='sigmoid')
        s_model.load_weights('./main/ML/model/seg/FPN_best_model_aug2.h5')

# graph2 = tf.Graph()
# with graph2.as_default():
#     session2 = tf.Session()
#     with session2.as_default():
#         i_model = PConvUnet()
#         i_model.load('./main/ML/model/inp/V3_0.73.h5')


graph3 = tf.Graph()
with graph3.as_default():
    session3 = tf.Session()
    with session3.as_default():
        Net = InpaintNet(batch=1)
        Net.generator.load_weights('./main/ML/model/inp/gan_gen.h5')
        Net.gan.load_weights('./main/ML/model/inp/gan.h5')
        Net.discriminator.load_weights('./main/ML/model/inp/gan_dis.h5')



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


# 현재 사용 x
# def predict_pconv_inp(oriURL, maskURL, inpURL):
#     # 이미지 load
#     # 1536, img_cols = 768
#
#     K.clear_session()
#
#
#     mask_img = Image.open(maskURL)
#     # mask_img = mask_img.resize((256, 512))
#     mask_img = np.array(mask_img)
#
#     mask = mask_img.copy()
#     mask[mask < 126] = 0
#     mask[mask > 127] = 1
#
#     # mask scale : 0 ~ 255 > 1 ~ 0
#     mask_img = mask_img - 255
#     mask_img[mask_img != 1] = 0
#     mask_img = mask_img.reshape(1, mask_img.shape[0], mask_img.shape[1], mask_img.shape[2])
#
#     ori_img = Image.open(oriURL)
#     # ori_img = ori_img.resize((256, 512))
#     ori_img = np.array(ori_img)
#
#     img_in = ori_img.copy()
#     img_in = img_in * (1. - mask)
#     img_in = img_in.astype(np.uint8)
#
#
#     ori_img = ori_img.reshape(1, ori_img.shape[0], ori_img.shape[1], ori_img.shape[2])
#     ori_img = ori_img * 1. / 255
#
#     # 원본 이미지에 마스크 입히기
#     ori_img[mask_img == 0] = 1
#
#     print('original img!! : ', ori_img.shape)
#
#     # 모델 load
#
#     with graph2.as_default():
#         with session2.as_default():
#             out_img = i_model.predict([ori_img, mask_img])
#
#
#     pred = out_img[0, :, :, :]
#     pred = pred * 255
#     pred = pred.astype(np.uint8)
#     img_complete = pred * mask + img_in * (1 - mask)
#
#     cv2.imwrite(settings.MEDIA_ROOT + '/' + inpURL, cv2.cvtColor(img_complete, cv2.COLOR_BGR2RGB))
#
#     return print('inpaint')


def predict_seg(oriURL, maskURL):
    # ori_img 코드 추가
    K.clear_session()

    ori_img = cv2.imread(oriURL)
    ori_img = cv2.cvtColor(ori_img, cv2.COLOR_BGR2RGB)
    ori_img = cv2.resize(ori_img, dsize=(256, 512), interpolation=cv2.INTER_AREA)

    ori_img = ori_img.reshape(1,512,256,3)


    ori_img = preprocess_input(ori_img)

    # round는 0 ~ 1 사이의 0.6 0.7 0.1 등의 값들을 반올림 해줘서 0 or 1로 하기위함
    with graph1.as_default():
        with session1.as_default():
            predict_img = s_model.predict(ori_img).round()


    predict_img = predict_img[..., 0].squeeze()

    # 1채널 -> 3 채널
    new_img = np.stack((predict_img,) * 3, -1)

    # to inpaint resize
    new_img = cv2.resize(new_img, dsize=(768, 1536), interpolation=cv2.INTER_AREA)

    cv2.imwrite(settings.MEDIA_ROOT + '/' + maskURL, new_img * 255)


    return print('segment')

def predict_inp_gan(oriURL, maskURL, inpURL):
    # 이미지 load
    # 512, img_cols = 256
    K.clear_session()

    img = cv2.imread(oriURL)
    mask_ = cv2.imread(maskURL,cv2.IMREAD_GRAYSCALE)

    cv2.imwrite(settings.MEDIA_ROOT + '/' + inpURL[:-4] + 'mask_src.jpg', mask_)

    # 침식+팽창 > 팽창
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.morphologyEx(mask_, cv2.MORPH_OPEN, kernel)
    kernel = np.ones((8, 8), np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=1)
    # 구멍 메우기
    kernel_ = np.ones((3, 3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel_)

    cv2.imwrite(settings.MEDIA_ROOT + '/' + inpURL[:-4] + 'mask_dst.jpg', mask)

    img_copy = img.copy()

    img = cv2.resize(img, (256, 512)).reshape(1, 512, 256, 3)
    mask = cv2.resize(mask, (256, 512)).reshape(1, 512, 256, 1)

    # 전처리
    img = img / 127.5 - 1.
    mask[mask < 126] = 0
    mask[mask > 127] = 1

    # 모델 load
    with graph3.as_default():
        with session3.as_default():
            pred = Net.generator.predict([img, mask])
            #out_img = i_model.predict([ori_img, mask_img])

    batch_pred = np.squeeze(((pred[0] + 1.) * 127.5).astype(np.uint8))
    batch_pred = cv2.resize(batch_pred, dsize=(768, 1536), interpolation=cv2.INTER_AREA)

    mask = cv2.resize(np.squeeze(mask),(768, 1536)).reshape(1536,768,1)
    batch_incomplete = img_copy * (1. - mask)
    batch_complete = batch_pred * mask + batch_incomplete * (1 - mask)
    print(batch_complete.shape)

    cv2.imwrite(settings.MEDIA_ROOT + '/' + inpURL, batch_complete)

    return print('inpaint gan')