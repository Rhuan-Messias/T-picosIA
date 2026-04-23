import os
import cv2

images_dir = r"..\dataset_split\test\images"
labels_dir = r"..\dataset_split\test\labels"

for img_name in os.listdir(images_dir):
    if not img_name.endswith((".jpg", ".png", ".jpeg")):
        continue

    img_path = os.path.join(images_dir, img_name)
    label_path = os.path.join(labels_dir, img_name.replace(".jpg", ".txt"))

    if not os.path.exists(label_path):
        continue

    img = cv2.imread(img_path)
    h, w, _ = img.shape

    with open(label_path, "r") as f:
        lines = f.readlines()

    for line in lines:
        cls, x_center, y_center, bw, bh = map(float, line.strip().split())

        # converter YOLO → pixels
        x_center *= w
        y_center *= h
        bw *= w
        bh *= h

        x_min = int(x_center - bw / 2)
        y_min = int(y_center - bh / 2)
        x_max = int(x_center + bw / 2)
        y_max = int(y_center + bh / 2)

        # desenhar caixa
        cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

    # mostrar imagem
    cv2.imshow("Bounding Box", img)
    key = cv2.waitKey(0)

    # pressione 'q' para sair
    if key == ord('q'):
        break

cv2.destroyAllWindows()