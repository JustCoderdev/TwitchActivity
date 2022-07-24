from base64 import b64encode

with open("blank.png", "rb") as img_file:
    imgB64 = b64encode(img_file.read())

print(imgB64)