import os
import json
json_path = '/Users/singwanghyeon/Source/git/goologin-272011-f2b7a9f953f2.json'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = json_path

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

    ocr_decode = json.loads(ocr_json)

    print(ocr_decode)


detect_text('/Users/singwanghyeon/Source/git/2_100_006.jpg')

