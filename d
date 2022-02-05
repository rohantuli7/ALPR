The following stages of image processing are followed:
 
Fig. 6.1: Stages of Image processing
i. Image acquisition 
Different images were acquired through the internet as well as through our phone cameras. Image in fig 1, 3 & 4 were acquired through our cameras while images in fig. 2 & 5 were taken from the internet. Each of these images were selected for their unique features such as the different types of characters, numbers and length of the number plate characters. 
These images are stored as imgOriginal in PyCharm and then, manipulated.






The different images are:
 
Fig. 6.2: License plate – DL 8C AF 5030

 
Fig. 6.3: License plate – MH 47 A 6493

 
Fig. 6.4: License plate – HF J726

 
Fig. 6.5: License plate – DL 4C AF 4943

 
Fig. 6.6: License plate – KL 01 BT 2525

Each of the above license plates are taken as input and worked upon separately.

ii. Pre-processing
The original input images are first converted into grayscale images. 
A grayscale image is simply one in which the only colours are shades of gray. The reason for differentiating such images from any other sort of colour image is that less information needs to be provided for each pixel.

 
Fig. 6.7:  Grayscale for License plate – DL 8C AF 5030

 
Fig. 6.8: Grayscale for License plate – MH 47 A 6493
 
Fig. 6.9: Grayscale for License plate – HF J726


 
Fig. 6.10: Grayscale for License plate – DL 4C AF 4943

 
Fig. 6.11: Grayscale for License plate – KL 01 BT 2525

Further, the images are converted into binary images using thresholding. Binarization is a process in which, a threshold value is selected and the pixel intensity values lying above that threshold are given a 255 pixel intensity and the values lying below the threshold are given 0 pixel intensity. This method allows us to efficiently display the edges and boundaries present in the image. We have binarized the image to obtain the characters present on the number plate.
 
	Fig. 6.12: Binarized License plate – DL 8C AF 5030	

 
Fig. 6.13: Binarized License plate – MH 47 A 6493

 
Fig. 6.14: Binarized License plate – HF J726


 
Fig. 6.15: Binarized License plate – DL 4C AF 4943

 
Fig. 6.16: Binarized License plate – KL 01 BT 2525
