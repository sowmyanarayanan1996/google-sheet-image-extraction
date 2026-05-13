
import io
import os
import re
import uuid
import requests
import numpy as np

from PIL import Image as PILImage
from openpyxl import load_workbook
from rapidocr_onnxruntime import RapidOCR

# ==========================================
# OCR ENGINE
# ==========================================

engine = RapidOCR()

# ==========================================
# CREATE TEMP FOLDER
# ==========================================

os.makedirs(
    "temp/images",
    exist_ok=True
)

# ==========================================
# URL CHECK
# ==========================================

def is_image_url(text):

    if not text:
        return False

    text = str(text).lower()

    return (
        text.startswith("http://")
        or text.startswith("https://")
    )

# ==========================================
# OCR FUNCTION
# ==========================================

def extract_text_from_image(
    pil_image
):

    img_np = np.array(
        pil_image
    )

    result, _ = engine(img_np)

    if result:

        texts = [
            item[1]
            for item in result
        ]

        return "\n".join(texts)

    return ""

# ==========================================
# PROCESS EXCEL
# ==========================================

def process_excel_images(
    excel_path
):

    wb = load_workbook(
        excel_path
    )

    ws = wb.active

    results = []

    # ======================================
    # EMBEDDED IMAGES
    # ======================================

    embedded_images = getattr(
        ws,
        "_images",
        []
    )

    for index, image in enumerate(
        embedded_images
    ):

        try:

            image_bytes = image._data()

            pil_image = PILImage.open(
                io.BytesIO(image_bytes)
            ).convert("RGB")

            image_name = (
                f"embedded_{index}.png"
            )

            image_path = (
                f"temp/images/{image_name}"
            )

            pil_image.save(
                image_path
            )

            extracted_text = (
                extract_text_from_image(
                    pil_image
                )
            )

            results.append({

                "image_name":
                image_name,

                "image_path":
                image_path,

                "text":
                extracted_text,

                "source_type":
                "embedded_image",

                "image_url":
                ""

            })

        except Exception as e:

            results.append({

                "image_name":
                f"embedded_{index}.png",

                "image_path":
                "",

                "text":
                "",

                "error":
                str(e)

            })

    # ======================================
    # IMAGE URLS IN CELLS
    # ======================================

    for row in ws.iter_rows():

        for cell in row:

            try:

                cell_value = cell.value

                if is_image_url(
                    cell_value
                ):

                    image_url = str(
                        cell_value
                    ).strip()

                    response = requests.get(
                        image_url,
                        timeout=20
                    )

                    if response.status_code != 200:
                        continue

                    image_bytes = (
                        response.content
                    )

                    pil_image = PILImage.open(
                        io.BytesIO(
                            image_bytes
                        )
                    ).convert("RGB")

                    image_name = (
                        f"url_"
                        f"{uuid.uuid4().hex[:8]}"
                        f".png"
                    )

                    image_path = (
                        f"temp/images/"
                        f"{image_name}"
                    )

                    pil_image.save(
                        image_path
                    )

                    extracted_text = (
                        extract_text_from_image(
                            pil_image
                        )
                    )

                    results.append({

                        "image_name":
                        image_name,

                        "image_path":
                        image_path,

                        "text":
                        extracted_text,

                        "source_type":
                        "image_url",

                        "image_url":
                        image_url

                    })

            except Exception as e:

                results.append({

                    "image_name":
                    "url_image",

                    "image_path":
                    "",

                    "text":
                    "",

                    "error":
                    str(e)

                })

    return results