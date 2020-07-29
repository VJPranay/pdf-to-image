from pdf2image import convert_from_path, convert_from_bytes
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)

images = convert_from_path('a.pdf')
count = 0
for image in images:
    count = count + 1
    image.save("img" + str(count) + ".webp", "WEBP")
    image.thumbnail((200, 200))
    image.save("thumb" + str(count) + ".webp", "WEBP")
