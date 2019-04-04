import cv2
import os

# Binarization
def Binarization(sample_img):
    for i in range(sample_img.shape[0]):
        for j in range(sample_img.shape[1]):
            if sample_img[i][j] > 128: 
                sample_img[i][j] = 0.  # 這邊黑白相反做處理
            else:
                sample_img[i][j] = 1. # 這邊黑白相反做處理 
    return sample_img # Return Binary image

# row cutting
def Row_cutting(binary_img):
    poplist = []
    flag = 0
    for i in range(binary_img.shape[0]):
        row_sum = 0
        for j in range(binary_img.shape[1]):
            row_sum = row_sum + binary_img[i][j]
        if row_sum != 0 and flag == 0:
            poplist.append(i-1)
            flag = 1            
        if row_sum == 0 and flag == 1 and (i - poplist[-1])>10:
            poplist.append(i+1)
            flag = 0
    return poplist

def col_cutting(binary_img):
    col_poplist = []
    flag2 = 0
    for j in range(binary_img.shape[1]):
        col_sum = 0
        for i in range(binary_img.shape[0]):
            col_sum = col_sum + binary_img[i][j]
        if col_sum != 0 and flag2 == 0:
            col_poplist.append(j)
            flag2 = 1            
        if col_sum == 0 and flag2 == 1:
            col_poplist.append(j-1)
            flag2 = 0
    return col_poplist

#---#

# read images
root_path = "D:/color/sample/"
root_img = "sample33.jpg" # 輸入要切的原圖!!!!!!
original_img = cv2.imread(root_path + root_img)
sample_img = cv2.imread(root_path + root_img, cv2.IMREAD_GRAYSCALE)

# root dir
first_rowcut_dir = "D:/color/letter3_row_cut1/"   # 列切第一次結果存的資料夾
first_colcut_dir = "D:/color/letter3_col_cut1/"   # 行切第一次結果存的資料夾
second_rowcut_dir = "D:/color/letter3_row_Final/"  # 列切第二次結果存的資料夾

# pre processing
binary_img = Binarization(sample_img) # binaried image
row_list = Row_cutting(binary_img) # coordinate


# 列切result1
name_number = 0
for i in range(0, len(row_list)-1, 2):
    name_number = name_number + 1
    # cut_img_binary = binary_img[row_list[i]:row_list[i+1], 0:sample_img.shape[1]] # its is (y, x) 取列行
    cut_img_ori = original_img[row_list[i]:row_list[i+1], 0:sample_img.shape[1]]
    cv2.imwrite(first_rowcut_dir+"row_cutting_result_"+str(name_number)+".jpg", cut_img_ori)


# 行切 result1
name_num = 0
for namejpg in os.listdir(first_rowcut_dir):
    ori_rcut_img = cv2.imread(first_rowcut_dir + namejpg)
    gray_rcut_img = cv2.imread(first_rowcut_dir + namejpg, cv2.IMREAD_GRAYSCALE)
    col_poplist = col_cutting(Binarization(gray_rcut_img))
    
    for i in range(0, len(col_poplist)-1, 2):
        name_num = name_num + 1
        test_letter = ori_rcut_img[0:ori_rcut_img.shape[0], col_poplist[i]:col_poplist[i+1]]
        # cv2.imshow("test_letter_"+str(name_num), test_letter)
        cv2.imwrite(first_colcut_dir + "test_letter_"+str(name_num)+".jpg", test_letter)
        

# Final 列切result2
number = 0
for name in range(1, len(os.listdir(first_colcut_dir))+1):
    ori_c_cut_img = cv2.imread(first_colcut_dir+"test_letter_"+str(name)+".jpg")
    gray_c_cut_img = cv2.imread(first_colcut_dir+"test_letter_"+str(name)+".jpg", cv2.IMREAD_GRAYSCALE)
    p_list = Row_cutting(Binarization(gray_c_cut_img))
    # print(p_list)
    number = number + 1
    cut2_img_ori = ori_c_cut_img[min(p_list)+1:max(p_list)-1, 0:ori_c_cut_img.shape[1]]
    cv2.imwrite(second_rowcut_dir +"cut2_"+str(number)+".jpg", cut2_img_ori)
