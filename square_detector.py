import os
from PIL import Image

def detect_and_save_squares(image_path, squares_folder):
    # Open the chessboard image
    chessboard_image = Image.open(image_path)

    # Optionally, crop the image if there are extra edges (adjust the crop values if needed)
    cropped_image = chessboard_image  # If no cropping is needed

    # Get the dimensions of the cropped image
    width, height = cropped_image.size

    # Calculate the size of each square (assuming it's a perfect 8x8 grid)
    square_width = width // 8
    square_height = height // 8

    # Chess notation for the squares (rows 1-8, columns a-h)
    columns = 'abcdefgh'
    rows = '12345678'

    # Loop through the grid and save each square as an individual image
    for row in range(8):
        for col in range(8):
            # Calculate the coordinates for each square
            left = col * square_width
            top = row * square_height
            right = left + square_width
            bottom = top + square_height

            # Crop the square from the image
            square_image = cropped_image.crop((left, top, right, bottom))

            # Define the file name based on chess notation (e.g., 'a1.png')
            square_name = f"{columns[col]}{rows[7 - row]}.png"  # In chess, row 1 starts at the bottom

            # Save the square image to the 'squares' folder
            square_image.save(os.path.join(squares_folder, square_name))

    print("Chessboard squares have been saved in the 'squares' folder.")

def create_squares_folder(folder_path):
    # Create the 'squares' folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
