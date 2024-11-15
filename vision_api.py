from google.cloud import vision
from mandatory_func import open_image_binary

client = vision.ImageAnnotatorClient()

def label_detection(image_path):
    image = open_image_binary(image_path)
    response = client.label_detection(image=image)
    labels = response.label_annotations
    desc, score = labels.description, labels.score
    return desc, score


def web_detection(image_path):
    image = open_image_binary(image_path)
    response = client.web_detection(image=image)
    web_detections = response.web_detections

    if web_detections.full_matching_images:
        print("완전 일치 이미지:")
        for img in web_detection.full_matching_images:
            print(f" - URL: {img.url}")

    if web_detections.partial_matching_images:
        print("부분 일치 이미지:")
        for img in web_detection.partial_matching_images:
            print(f" - URL: {img.url}")

    if web_detections.pages_with_matching_images:
        print("페이지 일치:")
        for page in web_detection.pages_with_matching_images:
            print(f" - URL: {page.url}")


# def safe_search_detection(image_path):
#     image = open_image_binary(image_path)
#     response = client.safe_search_detection(image=image)
#     safe_search = response.safe_search_annotation
#     return safe_search
# safe_search.adult
#               spoof, medical, violence, racy