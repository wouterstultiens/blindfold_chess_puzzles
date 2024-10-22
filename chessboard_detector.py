import os
import pygetwindow as gw
import pyautogui
import numpy as np
import cv2
import time

def detect_chessboard():
    """
    Detects the chessboard from the 'Chess tactics' window and saves the cropped image.
    """
    # Find the window with title containing 'Chess tactics'
    windows = gw.getWindowsWithTitle('Chess tactics')
    if not windows:
        raise Exception("No window found with 'Chess tactics' in the title.")
    window = windows[0]

    # Activate the window and take a screenshot
    window.activate()
    time.sleep(0.005)  # Slight delay to ensure the window is active
    screenshot = pyautogui.screenshot(region=(window.left, window.top, window.width, window.height))
    window.minimize()

    # Create the 'screenshots' directory if it doesn't exist
    os.makedirs('screenshots', exist_ok=True)

    # Convert screenshot to OpenCV format
    image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # Convert to grayscale and apply Gaussian blur
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply binary thresholding
    _, thresh = cv2.threshold(blurred, 150, 255, cv2.THRESH_BINARY)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the largest square contour assuming it's the chessboard
    chessboard_contour = None
    max_area = 0
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        area = w * h
        aspect_ratio = w / float(h)
        if 0.8 <= aspect_ratio <= 1.2 and area > max_area:
            max_area = area
            chessboard_contour = contour

    if chessboard_contour is not None:
        x, y, w, h = cv2.boundingRect(chessboard_contour)
        chessboard_img = image[y:y+h, x:x+w]
        chessboard_img_path = os.path.join('screenshots', 'cropped_chessboard.png')
        cv2.imwrite(chessboard_img_path, chessboard_img)
    else:
        raise Exception("No chessboard found.")
