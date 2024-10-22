from chessboard_detector import detect_chessboard
from piece_probability import save_detected_positions
from square_detector import detect_and_save_squares, create_squares_folder
import os

# Main function to call chessboard detection and piece identification
if __name__ == "__main__":
    print("Starting chessboard detection...")
    detect_chessboard()
    print("Chessboard detection completed.")
    
    # Paths
    folder_path = 'screenshots'
    file_name = 'cropped_chessboard.png'
    image_path = os.path.join(folder_path, file_name)
    squares_folder = os.path.join(folder_path, 'squares')

    # Create the 'squares' folder
    create_squares_folder(squares_folder)

    # Detect and save squares
    detect_and_save_squares(image_path, squares_folder)

    print("Detecting pieces on the board...")
    save_detected_positions(method="SSIM", threshold=0.1)   
    print("Piece detection completed. Check 'piece_positions.txt' for results.")
