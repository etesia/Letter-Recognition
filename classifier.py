import cv2
import os
import math

# Binarization
def Binarization(sample_img):
    for i in range(sample_img.shape[0]):
        for j in range(sample_img.shape[1]):
            if sample_img[i][j] < 128: 
                sample_img[i][j] = 1.  # 這邊黑白相反做處理
            else:
                sample_img[i][j] = 0. # 這邊黑白相反做處理 
    return sample_img # Return Binary image


letter_dictionary = {1:'a', 2:'b', 3:'c', 4:'d', 5:'e', 6:'f', 7:'g', 8:'h',9:'i', 10:'j', 11:'k', 12:'l',
13:'m', 14:'n', 15:'o', 16:'p',17:'q', 18:'r', 19:'s', 20:'t', 21:'u', 22:'v', 23:'w', 24:'x', 25:'y', 26:'z'}


Feature_dict = {}
root_path = "D:/color/"
sample_dir = "sample3_row_Final/" # 要辨識的路徑名稱

for i in range(1, 27):
    letter_1 = cv2.resize(Binarization(cv2.imread(root_path + "letter1_row_Final/cut2_"+str(i)+".jpg", cv2.IMREAD_GRAYSCALE)),(80, 60))
    letter_2 = cv2.resize(Binarization(cv2.imread(root_path + "letter2_row_Final/cut2_"+str(i)+".jpg", cv2.IMREAD_GRAYSCALE)),(80, 60))
    letter_3 = cv2.resize(Binarization(cv2.imread(root_path + "letter3_row_Final/cut2_"+str(i)+".jpg", cv2.IMREAD_GRAYSCALE)),(80, 60))
    Feature = (((letter_1 + letter_3)/2) + letter_2)/2
    Feature_dict[i] = Feature


for m in range(1, len(os.listdir(root_path + sample_dir))+1):
    test_sample = cv2.resize(Binarization(cv2.imread(root_path + sample_dir + "cut2_"+str(m)+".jpg", cv2.IMREAD_GRAYSCALE)),(80, 60))
    res_dict = {}
    
    for n in range(1, 27): #26 個 letter
        letter = Feature_dict[n]
        cos = 0
        inner_product = 0
        len_letter = 0
        len_sample = 0
        for i in range(letter.shape[0]):
            for j in range(letter.shape[1]):
                inner_product = inner_product + letter[i][j] * test_sample[i][j]

        for i in range(letter.shape[0]):
            for j in range(letter.shape[1]):
                len_letter = len_letter + letter[i][j]*letter[i][j]
        len_letter = math.sqrt(len_letter)

        for i in range(test_sample.shape[0]):
            for j in range(test_sample.shape[1]):
                len_sample = len_sample + test_sample[i][j]*test_sample[i][j]
        len_sample = math.sqrt(len_sample)

        cos = inner_product / (len_letter*len_sample)
        res_dict[n] = cos


    key = max(res_dict, key=res_dict.get)
    print(letter_dictionary[key], end='', flush=True)
print("\n")
