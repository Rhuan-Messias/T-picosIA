import os
import random
import shutil

# caminhos
images_dir = r"images_dir"   # pasta com imagens originais
labels_dir = r"labels_dir"   # pasta com labels YOLO (.txt)

output_dir = "dataset_split"

# proporções
train_ratio = 0.7
val_ratio = 0.15
test_ratio = 0.15

# cria estrutura
for split in ["train", "val", "test"]:
    os.makedirs(os.path.join(output_dir, split, "images"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, split, "labels"), exist_ok=True)

# lista imagens
images = [f for f in os.listdir(images_dir) if f.endswith((".jpg", ".png", ".jpeg"))]

# embaralhar
random.seed(42)
random.shuffle(images)

# calcular índices
n = len(images)
train_end = int(n * train_ratio)
val_end = int(n * (train_ratio + val_ratio))

train_files = images[:train_end]
val_files = images[train_end:val_end]
test_files = images[val_end:]

def move_files(file_list, split):
    for img in file_list:
        label = os.path.splitext(img)[0] + ".txt"

        src_img = os.path.join(images_dir, img)
        src_label = os.path.join(labels_dir, label)

        dst_img = os.path.join(output_dir, split, "images", img)
        dst_label = os.path.join(output_dir, split, "labels", label)

        # move imagem
        shutil.copy(src_img, dst_img)

        # move label (se existir)
        if os.path.exists(src_label):
            shutil.copy(src_label, dst_label)
        else:
            print(f"⚠️ Label não encontrada para {img}")

# executar
move_files(train_files, "train")
move_files(val_files, "val")
move_files(test_files, "test")

print("✅ Dataset dividido com sucesso!")