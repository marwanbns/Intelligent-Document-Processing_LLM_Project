# utils/annotate.py
import cv2

def draw_bbox(image_path, bbox):
    img = cv2.imread(image_path)
    x, y, w, h = bbox
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 4)
    output_path = image_path.replace(".png", "_highlighted.png")
    cv2.imwrite(output_path, img)
    return output_path