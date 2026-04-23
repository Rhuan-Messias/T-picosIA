import os
import cv2

labels_dir = "labels_dir"
images_dir = "images_dir"
output_dir = "labels_yolo"

os.makedirs(output_dir, exist_ok=True)

for file in os.listdir(labels_dir):
    if not file.endswith(".cat"):
        continue

    cat_path = os.path.join(labels_dir, file)

    # nome da imagem
    img_name = file.replace(".cat", "")
    img_path = os.path.join(images_dir, img_name)

    if not os.path.exists(img_path):
        print(f"Imagem não encontrada: {img_name}")
        continue

    # ler imagem para pegar dimensões
    img = cv2.imread(img_path)
    h, w, _ = img.shape

    # ler .cat
    with open(cat_path, "r") as f:
        data = list(map(int, f.read().strip().split()))

    n_points = data[0]
    coords = data[1:]

    xs = coords[0::2]
    ys = coords[1::2]

    # bounding box
    x_min = min(xs)
    y_min = min(ys)
    x_max = max(xs)
    y_max = max(ys)

    # converter para YOLO
    x_center = ((x_min + x_max) / 2) / w
    y_center = ((y_min + y_max) / 2) / h
    bw = (x_max - x_min) / w
    bh = (y_max - y_min) / h

    # salvar label
    yolo_path = os.path.join(output_dir, img_name.replace(".jpg", ".txt"))

    with open(yolo_path, "w") as f:
        f.write(f"0 {x_center} {y_center} {bw} {bh}\n")

print("✅ Conversão concluída!")