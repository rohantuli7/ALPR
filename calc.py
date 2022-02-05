import alpr
import cv2
numberplates = ["DL4CAF4943","DL8CAF5030","MH47A6493","KL01BT2525","HFJ726"]
n1 = cv2.imread("demo1.jpg")
n2 = cv2.imread("demo2.jpg")
n3 = cv2.imread("demo3.jpg")
n4 = cv2.imread("demo4.jpg")
n5 = cv2.imread("demo5.png")
number = []
number.append(alpr.main(n1,19,7,10))
number.append(alpr.main(n2,19,19,6))
number.append(alpr.main(n3,7,3,9))
number.append(alpr.main(n4,19,3,6))
number.append(alpr.main(n5,19,7,6))

l =[]
for i in numberplates:
    l.append(int(len(i)))
print()

den = 0
for i in l:
    den = den + int(i)
count = []
for i,j in zip(numberplates,number):
    c = 0
    for j,k in zip(i,j):
        if j!=k:
            c = c + 1
    count.append(int(c))

num = 0
for i in range(5):
    temp = int(l[i]) - int(count[i])
    num = num + temp

print("Actual number plates : ",numberplates)
print()
print("Number plates retrieved from the system : ",number)
print()
print("Variation in the values of the number plates : ",count)
print()

acc = (int(num)/den)*100
print("Accuracy of the system for the given data set = ",acc)