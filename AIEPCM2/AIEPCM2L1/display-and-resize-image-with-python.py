import cv2

image = cv2.imread('exa.jpg')

if image is None:
    raise FileNotFoundError("Could not load image.")

cv2.namedWindow('Loaded Image', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Loaded Image', 800, 500)

cv2.imshow('Loaded Image', image)

while True:
    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()
print("Image shape:", image.shape)
