from pyzbar import pyzbar
from PIL import Image
info = pyzbar.decode(Image.open('qr-code-definition-image_0.png'))
print(info)

import cv2
camera = cv2.VideoCapture(1)
ret, frame = camera.read()

while ret:
  ret, frame = camera.read()
  cv2.imshow('Barcode reader', frame)
  if cv2.waitKey(1) & 0xFF == 27:
    break
    
camera.release()
cv2.destroyAllWindows()
#above code is working - opens camera and reads QR-Codes and can identify barcodes but needs input
