

import pandas as pd
import cv2
import numpy as np
from openfoodfacts import utils
from pyzbar.pyzbar import decode


def get_product(barcode, locale='Denmark'):
    url = utils.build_url(geography=locale, service='api', resource_type='product', parameters=barcode)
    return utils.fetch(url)


def product_df(product_info):
    productDf = pd.DataFrame(product_info)
    productDf = productDf.loc['ingredients']['product']
    productDf = pd.DataFrame(productDf)
    productDfFinal = productDf[['id', 'vegan', 'vegetarian']].copy()
    return productDfFinal


def is_vegan(table):
    vegan = 'product is vegan'
    nvegan = 'product is not vegan'
    for row in table['vegan']:
        if row == 'no':
            return nvegan
            break
    return vegan


def is_vegetarian(table):
    vegetarian = 'product is vegetarian'
    nvegetarian = 'product is not vegetarian'
    for row in table['vegetarian']:
        if row == 'no':
            return nvegetarian
            break
    return vegetarian


def product_ingredients(table):
    listIngredients = []
    dictIngredients = {}
    for row in table['id']:
        listIngredients.append(row)
    return listIngredients


def non_vegan_ingredients(table):
    listID = []
    listVegan = []
    dictIngredients = {}
    dictVegan = {}
    for row in table['id']:
        listID.append(row)
    for row in table['vegan']:
        listVegan.append(row)
    for key in listID:
        for value in listVegan:
            dictIngredients[key] = value
            listVegan.remove(value)
            break

    for k, v in dictIngredients.items():
        if v == 'no':
            dictVegan[k] = v

    return dictVegan


def non_vegetarian_ingredients(table):
    listID = []
    listVegetarian = []
    dictIngredients = {}
    dictVegetarian = {}
    for row in table['id']:
        listID.append(row)
    for row in table['vegetarian']:
        listVegetarian.append(row)
    for key in listID:
        for value in listVegetarian:
            dictIngredients[key] = value
            listVegetarian.remove(value)
            break

    for k, v in dictIngredients.items():
        if v == 'no':
            dictVegetarian[k] = v

    return dictVegetarian


def display_product_info(x):
    #TODO: you need to handle for errors and/or other results.
    product_list = get_product(x)
    product_info = product_df(product_list)
    vegan = is_vegan(product_info)
    vegetarian = is_vegetarian(product_info)
    ingredients = product_ingredients(product_info)
    ingredient_vegan = non_vegan_ingredients(product_info)
    ingredients_vegetarian = non_vegetarian_ingredients(product_info)
    print(vegan)
    print(vegetarian)
    print(ingredients)
    print(ingredient_vegan)
    print(ingredients_vegetarian)


output = ''


def decoder(image):
    gray_img = cv2.cvtColor(image, 0)
    barcode = decode(gray_img)
    global output
    for obj in barcode:
        points = obj.polygon
        (x, y, w, h) = obj.rect
        pts = np.array(points, np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(image, [pts], True, (0, 255, 0), 3)
        barcodeData = obj.data.decode("utf-8")
        barcodeType = obj.type
        string = "Data " + str(barcodeData) + " | Type " + str(barcodeType)
        cv2.putText(frame, string, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
        # global output
        output = str(barcodeData)
        # global barcode2
        # barcode2 = str(barcodeData)
        # print(barcodeData)
        print(output)
        # return output
        break
        # return(barcodeData)
    return output


cap = cv2.VideoCapture(0)
x = ''
while x == '':
    ret, frame = cap.read()
    x = decoder(frame)
    cv2.imshow('Image', frame)
    code = cv2.waitKey(100)
    if code == ord('q'):
        break


print("Let's capture the bar code...")
print(f"Barcode is: {x}")

print("Let's check the ingredients...")
try:
    display_product_info(x)
# if there is any error, show error on Terminal
except Exception as e_ing:
    print(f"ERROR: {e_ing}")


