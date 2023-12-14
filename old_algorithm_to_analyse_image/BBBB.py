import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the image
image = cv2.imread('map2.png')
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

# Compute gradients
gradient_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=5)
gradient_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=5)


# Calculate gradient magnitude and angle
gradient_magnitude, gradient_angle = cv2.cartToPolar(gradient_x, gradient_y)

# Convert angle to degrees for easier visualization
gradient_angle_degrees = np.rad2deg(gradient_angle)

# Create an image for visualization
visualization_image = np.zeros_like(image)
S = 0.001
# Draw vectors on the visualization image
for i in range(0, gradient_magnitude.shape[0], 10):
    for j in range(0, gradient_magnitude.shape[1], 10):
        magnitude = gradient_magnitude[i, j]
        angle = gradient_angle_degrees[i, j]
        if magnitude > 0:  # Threshold to only draw significant gradients
            end_point = (int(j - S * magnitude * np.sin(np.deg2rad(angle))),
                         int(i + S * magnitude * np.cos(np.deg2rad(angle))))
            cv2.arrowedLine(visualization_image, (j, i), end_point, (255, 0, 0), 1, tipLength=0.5)

# Display the visualization
plt.imshow(visualization_image)
plt.title('Gradient Vectors')
plt.axis('off')
plt.show()

import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the image
image = cv2.imread('map2.png')
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

# Compute gradients
gradient_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=5)
gradient_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=5)

# Calculate divergence
divergence = cv2.Sobel(gradient_x, cv2.CV_64F, 1, 0, ksize=5) + cv2.Sobel(gradient_y, cv2.CV_64F, 0, 1, ksize=5)

# Define colormap for visualization (green to red)
colormap = plt.get_cmap('RdYlGn')  # RdYlGn is a colormap that transitions from green to red

# Normalize divergence values for mapping to colormap
divergence_normalized = cv2.normalize(divergence, None, 0, 1, cv2.NORM_MINMAX)

# Apply colormap
divergence_color = (colormap(divergence_normalized) * 255).astype(np.uint8)

# Display the divergence color map
plt.imshow(divergence_color)
plt.title('Divergence Color Map (Green to Red)')
plt.axis('off')
plt.show()

"""
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the image
image = cv2.imread('map2.png')
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

# Compute gradients
gradient_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=5)
gradient_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=5)

# Calculate the curl components
curl_zx = cv2.Sobel(gradient_x, cv2.CV_64F, 0, 1, ksize=5)
curl_zy = cv2.Sobel(gradient_y, cv2.CV_64F, 1, 0, ksize=5)

# Calculate magnitude of the curl
curl_magnitude = np.sqrt(curl_zy**2 + curl_zx**2)

# Define colormap for visualization (green to red)
colormap = plt.get_cmap('RdYlGn')

# Normalize curl magnitude values for mapping to colormap
curl_magnitude_normalized = cv2.normalize(curl_magnitude, None, 0, 1, cv2.NORM_MINMAX)

# Apply colormap
curl_color = (colormap(curl_magnitude_normalized) * 255).astype(np.uint8)

# Display the curl color map
plt.imshow(curl_color)
plt.title('Curl Magnitude Color Map (Green to Red)')
plt.axis('off')
plt.show()"""
