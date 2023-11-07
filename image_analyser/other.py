import cv2
import numpy as np

# Read the image
image = cv2.imread("map.png")

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


# Apply Canny edge detection
edges = cv2.Canny(gray, 30, 90)


# Find contours in the edges
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
print()
# Draw the contours on a blank image
contour_image = np.zeros_like(image)
cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 2)

# Display the original image and the image with contours
cv2.imshow("Original Image", image)
cv2.imshow("Image with Contours", contour_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
