import os
import numpy as np
import cv2
import matplotlib.pyplot as plt


# image_test = "C:/Users/parek/Downloads/4th_Floor_Hallway_Measuring_Test1/4th_Floor_Hallway_Measuring_Test1/Photos_Color_1742071924428.31933593750000.png"
# image_test = "C:/Users/parek/Downloads/4th_Floor_Hallway_Measuring_Test1/4th_Floor_Hallway_Measuring_Test1/Photos_Color_1742071923706.56591796875000.png"
# image_test = "C:/Users/parek/Downloads/4th_Floor_Hallway_Measuring_Test1/4th_Floor_Hallway_Measuring_Test1/Photos_Color_1742071924862.66601562500000.png"

# path = "C:/Users/parek/Downloads/4th_Floor_Hallway_Measuring_Test1/4th_Floor_Hallway_Measuring_Test00"
# path = "C:/Users/parek/Downloads/4th_Floor_Hallway_Measuring_Test1/4th_Floor_Hallway_Measuring_Test2/image_0670_bin_210_44.png"
# path = "C:/Users/parek/Desktop/SeniorDesign/RTABMAP/437desksetupdata/imageOuts/rgb"

isRGB = False

def laplace_variance(image):
    return cv2.Laplacian(image, cv2.CV_64F).var()

def RL_deconvolution(observed, psf, iterations):
    # initial estimate is arbitrary - uniform 50% grey works fine
    latent_est = 0.5*np.ones(observed.shape)
    # create an inverse psf
    psf_hat = psf[::-1,::-1]
    # iterate towards ML estimate for the latent image
    for i in np.arange(iterations):
        est_conv      = cv2.filter2D(latent_est,-1,psf)
        relative_blur = observed/est_conv
        error_est     = cv2.filter2D(relative_blur,-1,psf_hat)
        latent_est    = latent_est * error_est
    return latent_est

# var_store = np.zeros(len(os.listdir(path)))

# for file in os.listdir(path):
    # os.rename(path + "/" + file, path + "/" + file.replace(".", ""))
    # os.rename(path + "/" + file, path + "/" + file.replace("png", ".png"))



# print(laplace_variance(cv2.imread("C:/Users/parek/Desktop/SeniorDesign/RTABMAP/437desksetupdata/imageOuts/rgb/1742162471608267.png")))

# for index, file in enumerate(os.listdir(path)):
#     # print(file)
#     if(os.path.isdir(path + "/" + file)):
#         continue
#     image = cv2.imread(path + "/" + file)
#     try:
#         gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#         isRGB = True
#     except:
#         gray = image
    
#     # print(gray.dtype)
#     # blurmetric = laplace_variance(gray)
    
#     # print(blurmetric)
#     # if blurmetric > 200:
#         # plt.figure()
#         # if isRGB:
#         #     plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
#         # else:
#         #     plt.imshow(gray)
#         # print(file)
#     # var_store[index] = blurmetric

image = cv2.imread(path)
kernel_size = 7
kernMB = np.zeros((kernel_size,kernel_size))
kernMB[int((kernel_size-1)/2), :] = np.ones(kernel_size)
kernMB /= kernel_size
new_img = RL_deconvolution(image, kernMB, 50)
new_img = cv2.normalize(new_img, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
plt.figure()
plt.imshow(cv2.cvtColor(new_img, cv2.COLOR_BGR2RGB))
plt.waitforbuttonpress()
# print(np.median(var_store))
# print(np.average(var_store))

# plt.figure()
# plt.hist(var_store, bins=50, color='red')
# plt.xlabel("Value")
# plt.ylabel("Freq")

# plt.show()

# for image in list_images:
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     blurmetric = laplace_variance(gray)

