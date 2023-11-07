"""
import cv2
import numpy as np

# Load your satellite image where roads are black
satellite_image = cv2.imread('map2.png', cv2.IMREAD_GRAYSCALE)

# Invert the image (making roads white and other regions black)
inverted_image = cv2.bitwise_not(satellite_image)

# Define a structuring element for erosion (a smaller kernel will shrink the roads more)
d = 8
kernel = np.ones((d,d),np.uint8)  # Adjust the kernel size as needed

# Apply erosion to shrink the roads
shrunken_roads = cv2.erode(inverted_image, kernel, iterations=1)

# Invert the image back to its original state
shrunken_roads = cv2.bitwise_not(shrunken_roads)


cv2.imwrite('shrunken_roads.png', shrunken_roads)
# Display the result
cv2.imshow('Shrunken Roads', shrunken_roads)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""
"""
import cv2
import numpy as np

# Load your satellite image where roads are black
satellite_image = cv2.imread('map2.png', cv2.IMREAD_GRAYSCALE)

# Invert the image (making roads white and other regions black)
inverted_image = cv2.bitwise_not(satellite_image)

# Define a structuring element for erosion (for large roads)
large_kernel_size = 20  # Adjust the kernel size as needed
large_kernel = np.ones((large_kernel_size, large_kernel_size), np.uint8)

# Define a structuring element for erosion (for narrow roads)
narrow_kernel_size = 6  # Adjust the kernel size as needed
narrow_kernel = np.ones((narrow_kernel_size, narrow_kernel_size), np.uint8)

# Apply contour analysis to distinguish between narrow and large roads
contours, _ = cv2.findContours(inverted_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for contour in contours:
    area = cv2.contourArea(contour)
    if area > 1000:  # You can adjust this threshold to suit your needs
        # Apply erosion with the large kernel
        shrunken_roads = cv2.erode(inverted_image, large_kernel, iterations=1)
    else:
        # Apply erosion with the narrow kernel
        shrunken_roads = cv2.erode(inverted_image, narrow_kernel, iterations=1)

# Invert the image back to its original state
shrunken_roads = cv2.bitwise_not(shrunken_roads)

# Display the result
cv2.imshow('Shrunken Roads', shrunken_roads)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""
"""
import cv2
import numpy as np

# Load your satellite image where roads are black
satellite_image = cv2.imread('map2.png', cv2.IMREAD_GRAYSCALE)

# Apply Canny edge detection
edges = cv2.Canny(satellite_image, 50, 150)

# Apply distance transform
dist_transform = cv2.distanceTransform(edges, cv2.DIST_L2, 3)

# Threshold the distance transform to identify wide roads
threshold_value = 0.8  # You may need to adjust this based on your specific image
_, wide_roads = cv2.threshold(dist_transform, threshold_value * dist_transform.max(), 255, 0)

# Convert to uint8
wide_roads = np.uint8(wide_roads)

# Apply erosion to the wide roads
kernel = np.ones((5, 5), np.uint8)  # Adjust the kernel size as needed
shrunken_wide_roads = cv2.erode(wide_roads, kernel, iterations=1)

# Display the result
cv2.imshow('Shrunken Wide Roads', shrunken_wide_roads)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""
"""
import cv2
import numpy as np

# Load the satellite image
image = cv2.imread('map2.png', cv2.IMREAD_GRAYSCALE)

# Assuming you have the original image loaded as 'image'
# Invert the image (making roads white and other regions black)
inverted_image = cv2.bitwise_not(image)

# Define a structuring element for erosion (a smaller kernel will shrink the roads more)
d = 7
kernel = np.ones((d,d),np.uint8)  # Adjust the kernel size as needed

# Apply erosion to shrink the roads
shrunken_roads = cv2.erode(inverted_image, kernel, iterations=1)

# Invert the image back to its original state
eroded_image = cv2.bitwise_not(shrunken_roads)







# Create a mask of the wide roads
wide_roads_mask = cv2.bitwise_not(eroded_image)




# Assuming you have the original image loaded as 'image'
narrow_roads_image = cv2.bitwise_not(image, image, mask=wide_roads_mask)




cv2.imshow('Merged Image', narrow_roads_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Assuming you have the shrunken wide roads image as 'eroded_image'
merged_image = cv2.add(eroded_image, narrow_roads_image)

cv2.imshow('Merged Image', merged_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
# OR save the image with cv2.imwrite()
"""
import cv2
import numpy as np

# Load the shrunken wide roads image
original_image = cv2.imread('map2.png', cv2.IMREAD_GRAYSCALE)


# Assuming you have the original image loaded as 'image'
# Invert the image (making roads white and other regions black)
inverted_image = cv2.bitwise_not(original_image)

# Define a structuring element for erosion (a smaller kernel will shrink the roads more)
d = 8
kernel = np.ones((d,d),np.uint8)  # Adjust the kernel size as needed

# Apply erosion to shrink the roads
shrunken_roads = cv2.erode(inverted_image, kernel, iterations=1)

# Invert the image back to its original state
shrunken_roadss = cv2.bitwise_not(shrunken_roads)
cv2.imshow('Narrow Roads Image', shrunken_roadss)
cv2.waitKey(0)
cv2.destroyAllWindows()


# Define a kernel for morphological operations (structuring element)
s = 11
kernel = np.ones((s,s), np.uint8)

# Apply dilation to widen the roads back to their original size
inverted_image = cv2.bitwise_not(shrunken_roadss)

dilated_wide_roads = cv2.dilate(inverted_image, kernel, iterations=1)

dilated_wide_roads = cv2.bitwise_not(dilated_wide_roads)

_, binary_image = cv2.threshold(dilated_wide_roads, 240, 255, cv2.THRESH_BINARY)

cv2.imshow('Narrow Roads Image', binary_image)
cv2.waitKey(0)
cv2.destroyAllWindows()



# Assuming you have the original image loaded as 'image'
narrow_roads_image = cv2.bitwise_not(original_image, original_image, mask=binary_image)

narrow_roads_image = cv2.bitwise_not(original_image, original_image)


# Display or save the result
cv2.imshow('Narrow Roads Image', narrow_roads_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
# OR save the image with cv2.imwrite()



inverted_image = cv2.bitwise_not(narrow_roads_image)

# Define a structuring element for erosion (a smaller kernel will shrink the roads more)
d = 4
kernel = np.ones((d,d),np.uint8)  # Adjust the kernel size as needed

# Apply erosion to shrink the roads
shrunken_roads = cv2.erode(inverted_image, kernel, iterations=1)

# Invert the image back to its original state
shrunken_roads = cv2.bitwise_not(shrunken_roads)
cv2.imshow('Narrow Roads Image', shrunken_roads)
cv2.waitKey(0)
cv2.destroyAllWindows()

aaa = cv2.bitwise_and(shrunken_roads,shrunken_roadss)

# Convert the image to grayscale

_, thresh = cv2.threshold(aaa, 240, 255, cv2.THRESH_BINARY)
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(aaa, contours, -1, (255, 255, 255), 10)  # -1 draws all contours, (0, 255, 0) is color, 2 is thickness

cv2.imshow('Narrow Roads Image', aaa)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imwrite("hey.png",aaa)




















