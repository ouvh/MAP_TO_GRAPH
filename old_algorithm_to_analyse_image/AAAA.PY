import cv2
import numpy as np
# Load the image
image = cv2.imread('map2.png', cv2.IMREAD_GRAYSCALE)

edges = cv2.Canny(image, 50, 150)


gradient_x = cv2.Sobel(edges, cv2.CV_64F, 1, 0, ksize=5)
gradient_y = cv2.Sobel(edges, cv2.CV_64F, 0, 1, ksize=5)
gradient_magnitude = cv2.magnitude(gradient_x, gradient_y)
gradient_orientation = cv2.phase(gradient_x, gradient_y, angleInDegrees=True)



threshold = 50
_, thresholded_magnitude = cv2.threshold(gradient_magnitude, threshold, 255, cv2.THRESH_BINARY)


def detect_orientation_changes(gradient_orientation, threshold):
    orientation_changes = cv2.compare(np.roll(gradient_orientation, 1, axis=0), gradient_orientation, cv2.CMP_NE)
    return np.where(orientation_changes > 0, 255, 0)

intersection_mask = detect_orientation_changes(gradient_orientation, threshold)
intersection_mask = intersection_mask.astype(np.uint8)



cv2.imshow('Intersection Mask', intersection_mask)
cv2.waitKey(0)
cv2.destroyAllWindows()







def detect_dominant_orientation(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Canny edge detection
    edges = cv2.Canny(gray, 50, 150)
    
    # Apply Hough Transform to detect lines
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
    
    # Calculate angles of detected lines
    angles = [line[0][1] for line in lines]
    
    # Calculate histogram of angles
    hist, bins = np.histogram(angles, bins=180, range=(0, 180))
    
    # Find the dominant orientation(s)
    dominant_orientations = [i for i, count in enumerate(hist) if count > 0.2 * max(hist)]
    
    return dominant_orientations

# Load your image
image = cv2.imread('map2.png')

# Detect dominant orientations
orientations = detect_dominant_orientation(image)
print("Dominant Orientations (in degrees):", orientations)

# Draw lines corresponding to the dominant orientations (optional)
output_image = np.copy(image)
for angle in orientations:
    theta = np.pi * angle / 180
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * 1000
    y0 = b * 1000
    x1 = int(x0 + 10000 * (-b))
    y1 = int(y0 + 10000 * (a))
    x2 = int(x0 - 10000 * (-b))
    y2 = int(y0 - 10000 * (a))
    cv2.line(output_image, (x1, y1), (x2, y2), (0, 0, 255), 2)

# Display the result
cv2.imshow('Dominant Orientations', output_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
