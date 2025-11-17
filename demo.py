import cv2
import numpy as np
import random


# Encryption function
def encrypt():
    # img1 and img2 are the
    # two input images
    img1 = cv2.imread('9_horses.png')
    img2 = cv2.imread('11.png')

    for i in range(img2.shape[0]):
        for j in range(img2.shape[1]):
            for l in range(3):
                # v1 and v2 are 8-bit pixel values
                # of img1 and img2 respectively
                v1 = format(img1[i][j][l], '08b')
                v2 = format(img2[i][j][l], '08b')

                # Taking 4 MSBs of each image
                v3 = v1[:4] + v2[:4]

                img1[i][j][l] = int(v3, 2)

    cv2.imwrite('encrypt.png', img1)


# Decryption function
def decrypt():
    # Encrypted image
    img = cv2.imread('encrypt.png')
    width = img.shape[0]
    height = img.shape[1]

    # img1 and img2 are two blank images
    img1 = np.zeros((width, height, 3), np.uint8)
    img2 = np.zeros((width, height, 3), np.uint8)

    for i in range(width):
        for j in range(height):
            for l in range(3):
                v1 = format(img[i][j][l], '08b')
                v2 = v1[:4] + chr(random.randint(0, 1) + 48) * 4
                v3 = v1[4:] + chr(random.randint(0, 1) + 48) * 4

                # Appending data to img1 and img2
                img1[i][j][l] = int(v2, 2)
                img2[i][j][l] = int(v3, 2)

    # These are two images produced from
    # the encrypted image
    cv2.imwrite('image1.png', img1)
    cv2.imwrite('image2.png', img2)


# Driver's code
encrypt()
decrypt()

#
#
# # import pyrebase
# #
# # import PIL
# # from PIL import Image
# # firebaseConfig = {
# #   "apiKey": "AIzaSyBUiToMpgyJYI3EUZ0U4cr3VS-zMzTccfE",
# #   "authDomain": "python-83560.firebaseapp.com",
# #   "databaseURL": "https://python-83560-default-rtdb.firebaseio.com",
# #   "projectId": "python-83560",
# #   "storageBucket": "python-83560.appspot.com",
# #   "messagingSenderId": "439817628919",
# #   "appId": "1:439817628919:web:9fa080fd41b8cf052bf7f2"
# #
# # }
# # firebase=pyrebase.pyrebase.initialize_app(firebaseConfig)
# # storage=firebase.storage()
# # my_img="C:\\Users\\intex\\Pictures\\user\\user2.jpg"
# #
# # # todo upload
# # # storage.child(my_img).put(my_img)
# # #download
# # storage.child(my_img).download(filename="new.jpg",path="")
# # img=PIL.Image.open("new.jpg")
# # myHeight,myWidth=img.size
# # img=img.resize((myHeight,myWidth),PIL.Image.ANTIALIAS)
# # img.save(" compressed.jpg")
# #
# #
# #
