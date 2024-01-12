import cv2
import numpy as np
from sklearn.cluster import KMeans


def find_dominant_color(image, k=1):
    """Find the dominant color in the image."""
    pixels = np.float32(image.reshape(-1, 3))
    kmeans = KMeans(n_clusters=k, random_state=0).fit(pixels)
    return kmeans


def find_histogram(clt):
    """
    create a histogram with k clusters
    :param: clt
    :return:hist
    """
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)

    hist = hist.astype("float")
    hist /= hist.sum()

    return hist


def plot_colors2(hist, centroids):
    bar = np.zeros((50, 300, 3), dtype="uint8")
    startX = 0

    for percent, color in zip(hist, centroids):
        # plot the relative percentage of each cluster
        endX = startX + (percent * 300)
        cv2.rectangle(
            bar, (int(startX), 0), (int(endX), 50), color.astype("uint8").tolist(), -1
        )
        startX = endX

    # return the bar chart
    return bar


# Start capturing video from the webcam
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape
    cx, cy = w // 2, h // 2
    size = 300  # Size of the central rectangle

    # Define the central rectangle coordinates
    x1, y1 = (cx - size // 2, cy - size // 2)
    x2, y2 = (cx + size // 2, cy + size // 2)

    # Extract the central rectangle
    central_rectangle = frame[y1:y2, x1:x2]

    # Find the dominant color
    k_means = find_dominant_color(central_rectangle, k=3)
    hist = find_histogram(k_means)
    bar = plot_colors2(hist, k_means.cluster_centers_)
    # dominant_color = np.uint8(dominant_color).tolist()

    # Draw the central rectangle on the frame
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Display the frame
    cv2.imshow("Frame", frame)

    # Display the dominant color in a separate window
    cv2.imshow("Dominant Colors", bar)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
