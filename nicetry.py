import sys
import pandas as pd
import cv2
import numpy as np
from pyzbar.pyzbar import decode
import openfoodfacts
import requests
from openfoodfacts import utils
def decoder(image):
    gray_img = cv2.cvtColor(image,0)
    barcode = decode(gray_img)
    for obj in barcode:
        points = obj.polygon
        (x,y,w,h) = obj.rect
        pts = np.array(points, np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(image, [pts], True, (0, 255, 0), 3)
        barcodeData = obj.data.decode("utf-8")
        barcodeType = obj.type
        string = "Data " + str(barcodeData) + " | Type " + str(barcodeType)
        cv2.putText(frame, string, (x,y), cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,0,0), 2)
        productScan = openfoodfacts.products.get_product(barcodeData)
        productScan = pd.DataFrame(productScan)
        infoOnProduct = pd.DataFrame(productScan.loc['ingredients']['product'])
        if any(infoOnProduct.loc[:,'vegan']) == 'yes':
         print("Product is vegan")
#elif any(infoOnProduct.loc[:,'vegan']) =='yes' and any(infoOnProduct.loc[:,'vegan']) != 'yes':
    #print("Product might be vegan")
        else:
            print("Product is not vegan")
            return ("Barcode: "+barcodeData +" | Type: "+barcodeType)
cap = cv2.VideoCapture(1)
while True:
    ret, frame = cap.read()
    barcode = decoder(frame)
    decoder(frame)
    cv2.imshow('Image', frame)
    code = cv2.waitKey(10)
    if code == ord('q'):
        break
