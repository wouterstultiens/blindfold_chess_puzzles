import os
from PIL import Image

def detect_and_save_squares(image_path, squares_folder):
    """
    Splits the chessboard image into 64 squares and saves them individually.
    """
    chessboard_image = Image.open(image_path)
    width, height = chessboard_image.size
    square_size = (width // 8, height // 8)
    columns = 'abcdefgh'
    rows = '87654321'  # Adjusted for proper orientation

    for row_index, row in enumerate(rows):
        for col_index, col in enumerate(columns):
            left = col_index * square_size[0]
            top = row_index * square_size[1]
            right = left + square_size[0]
            bottom = top + square_size[1]
            square_image = chessboard_image.crop((left, top, right, bottom))
            square_name = f"{col}{row}.png"
            square_image.save(os.path.join(squares_folder, square_name))

def create_squares_folder(folder_path):
    """
    Creates the 'squares' folder if it doesn't exist.
    """
    os.makedirs(folder_path, exist_ok=True)
