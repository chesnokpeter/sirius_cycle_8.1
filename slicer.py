from PIL import Image

# Открываем изображение
image_path = "img.jpg"
image = Image.open(image_path)
width, height = image.size

# Преобразуем изображение в список пикселей
pixels = list(image.getdata())

# Разделяем пиксели на строки
pixel_rows = [pixels[i * width:(i + 1) * width] for i in range(height)]

# Сохраняем каждую строку пикселей в отдельное изображение
for i, row_pixels in enumerate(pixel_rows):
    new_image = Image.new("RGB", (width, 1))
    new_image.putdata(row_pixels)
    new_image.save(f"rows/row_{i+1}.png")

print("Строки пикселей были сохранены в папку в виде изображений.")