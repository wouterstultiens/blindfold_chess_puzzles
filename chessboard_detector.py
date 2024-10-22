import os
import pygetwindow as gw
import pyautogui
import numpy as np
import cv2
import time

# Function to detect and save the chessboard
def detect_chessboard():
    # Step 1: Find the Chrome window with title containing "Chess tactics"
    windows = gw.getWindowsWithTitle('Chess tactics')
    if not windows:
        raise Exception("No window found with 'Chess tactics' in the title.")
    window = windows[0]

    # Step 2: Get the window's coordinates and take a screenshot of the window
    window.activate()  # Bring the window to the front
    time.sleep(1)  # Small delay to allow the window to focus
    screenshot = pyautogui.screenshot(region=(window.left, window.top, window.width, window.height))

    # Create the 'screenshots' directory if it doesn't exist
    if not os.path.exists('screenshots'):
        os.makedirs('screenshots')

    # Save the intermediate screenshot for debugging
    full_screenshot_path = os.path.join('screenshots', 'full_window_screenshot.png')
    screenshot.save(full_screenshot_path)
    print(f"Full screenshot saved to {full_screenshot_path}")

    # Convert screenshot to OpenCV format
    image = np.array(screenshot)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Step 3: Convert to grayscale for contour detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Step 4: Apply edge detection or binary thresholding
    _, thresh = cv2.threshold(blurred, 150, 255, cv2.THRESH_BINARY)

    # Step 5: Find contours in the thresholded image
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Initialize variables to hold the chessboard bounding box
    chessboard_contour = None
    chessboard_area = 0

    # Step 6: Filter contours to find the chessboard
    for contour in contours:
        # Get the bounding rectangle of each contour
        x, y, w, h = cv2.boundingRect(contour)
        area = w * h
        
        # Heuristic: Chessboard is usually a large square (with an aspect ratio close to 1)
        aspect_ratio = w / float(h)
        if 0.8 <= aspect_ratio <= 1.2 and area > chessboard_area:  # Adjust size if necessary
            chessboard_area = area
            chessboard_contour = contour

    if chessboard_contour is not None:
        # Step 7: Get the bounding box of the chessboard
        x, y, w, h = cv2.boundingRect(chessboard_contour)

        # Crop the image to the chessboard region
        chessboard_img = image[y:y+h, x:x+w]

        # Save the cropped chessboard image
        chessboard_img_path = os.path.join('screenshots', 'cropped_chessboard.png')
        cv2.imwrite(chessboard_img_path, chessboard_img)
        print(f"Cropped chessboard saved to {chessboard_img_path}")

        # Remove the cv2.imshow and cv2.waitKey lines to avoid GUI issues
        # cv2.imshow('Cropped Chessboard', chessboard_img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
    else:
        print("No chessboard found.")
