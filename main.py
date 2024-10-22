import os
from chessboard_detector import detect_chessboard
from square_detector import detect_and_save_squares, create_squares_folder
from piece_probability import save_detected_positions

if __name__ == "__main__":
    detect_chessboard()

    # Paths
    image_path = os.path.join('screenshots', 'cropped_chessboard.png')
    squares_folder = os.path.join('screenshots', 'squares')

    # Create the 'squares' folder and detect squares
    create_squares_folder(squares_folder)
    detect_and_save_squares(image_path, squares_folder)

    # Detect pieces and save positions
    save_detected_positions(method="SSIM", threshold=0.5)
