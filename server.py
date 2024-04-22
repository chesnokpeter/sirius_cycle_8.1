from fastapi.responses import StreamingResponse
from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from PIL import Image
import numpy as np
import io

app = FastAPI()

images = {}

@app.post("/row")
async def create_image_row(row_number: int, image: UploadFile, r: Request):
    print(row_number)
    image_content = await image.read() 
    images[row_number] = image_content 
    return 'Строчка пикселей загружена'

@app.get("/clear")
async def clear_images():
    global images
    images.clear()
    return 'Данные успешно очистились'

@app.get("/pic")
async def get_image():
    if not images:
        raise HTTPException(status_code=404, detail="Пиксели отсутствуют")

    max_row = max(images.keys()) 
    sorted_images = [images.get(key, None) for key in range(1, max_row + 1)]

    images_list = []
    width = None
    for img_bytes in sorted_images:
        if img_bytes is None:
            if width is None:
                for img_bytes in sorted_images:
                    if img_bytes is not None:
                        img = Image.open(io.BytesIO(img_bytes))
                        width = img.width
                        break
            img = Image.new('RGB', (width, 1), color='white')
        else:
            img = Image.open(io.BytesIO(img_bytes))
        images_list.append(img)

    merged_image = np.concatenate([np.array(img) for img in images_list], axis=0)
    final_image = Image.fromarray(merged_image)

    img_byte_arr = io.BytesIO()
    final_image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    return StreamingResponse(io.BytesIO(img_byte_arr.read()), media_type="image/png")