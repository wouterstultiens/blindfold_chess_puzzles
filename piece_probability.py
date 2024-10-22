import cv2
import numpy as np
import os
from skimage.metrics import structural_similarity as ssim

# Path to the folders containing square images and pieces
squares_folder = 'screenshots/squares'
pieces_folder = 'pieces'

# List of all piece image names in logical order
pieces = ['bK', 'bQ', 'bR', 'bB', 'bN', 'bP', 'wK', 'wQ', 'wR', 'wB', 'wN', 'wP', 'empty']

# White's perspective mapping
board_positions_white = {
    0: "a1", 1: "a2", 2: "a3", 3: "a4", 4: "a5", 5: "a6", 6: "a7", 7: "a8",
    8: "b1", 9: "b2", 10: "b3", 11: "b4", 12: "b5", 13: "b6", 14: "b7", 15: "b8",
    16: "c1", 17: "c2", 18: "c3", 19: "c4", 20: "c5", 21: "c6", 22: "c7", 23: "c8",
    24: "d1", 25: "d2", 26: "d3", 27: "d4", 28: "d5", 29: "d6", 30: "d7", 31: "d8",
    32: "e1", 33: "e2", 34: "e3", 35: "e4", 36: "e5", 37: "e6", 38: "e7", 39: "e8",
    40: "f1", 41: "f2", 42: "f3", 43: "f4", 44: "f5", 45: "f6", 46: "f7", 47: "f8",
    48: "g1", 49: "g2", 50: "g3", 51: "g4", 52: "g5", 53: "g6", 54: "g7", 55: "g8",
    56: "h1", 57: "h2", 58: "h3", 59: "h4", 60: "h5", 61: "h6", 62: "h7", 63: "h8",
}

# Black's perspective mapping (180 degrees turned)
board_positions_black = {
    0: "h8", 1: "h7", 2: "h6", 3: "h5", 4: "h4", 5: "h3", 6: "h2", 7: "h1",
    8: "g8", 9: "g7", 10: "g6", 11: "g5", 12: "g4", 13: "g3", 14: "g2", 15: "g1",
    16: "f8", 17: "f7", 18: "f6", 19: "f5", 20: "f4", 21: "f3", 22: "f2", 23: "f1",
    24: "e8", 25: "e7", 26: "e6", 27: "e5", 28: "e4", 29: "e3", 30: "e2", 31: "e1",
    32: "d8", 33: "d7", 34: "d6", 35: "d5", 36: "d4", 37: "d3", 38: "d2", 39: "d1",
    40: "c8", 41: "c7", 42: "c6", 43: "c5", 44: "c4", 45: "c3", 46: "c2", 47: "c1",
    48: "b8", 49: "b7", 50: "b6", 51: "b5", 52: "b4", 53: "b3", 54: "b2", 55: "b1",
    56: "a8", 57: "a7", 58: "a6", 59: "a5", 60: "a4", 61: "a3", 62: "a2", 63: "a1",
}

# Function to compare two images using SSIM and return a similarity score
def compare_images(imageA, imageB):
    imageB = cv2.resize(imageB, (imageA.shape[1], imageA.shape[0]))
    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
    score, _ = ssim(grayA, grayB, full=True)
    return score

# Function to detect the predominant color (black or white) in an image with a single threshold
def detect_color(image, threshold=1):
    # Convert the image to RGB
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    total_pixels = rgb_image.shape[0] * rgb_image.shape[1]  # Total number of pixels

    # Define thresholds for what is considered "dark" (black) and "light" (white)
    black_threshold = 50  # Very low values across all channels for black
    white_threshold = 200  # Very high values across all channels for white

    # Count black pixels: where all RGB values are below black_threshold
    black_pixels = np.sum(np.all(rgb_image < black_threshold, axis=2))
    
    # Count white pixels: where all RGB values are above white_threshold
    white_pixels = np.sum(np.all(rgb_image > white_threshold, axis=2))
    
    # Calculate black and white values as numbers from 1 to 100
    black_value = int((black_pixels / total_pixels) * 100)
    white_value = int((white_pixels / total_pixels) * 100)
    
    # Divide white by black to determine threshold
    threshold_value = white_value / black_value if black_value != 0 else float('inf')
    
    # Determine if it's predominantly white or black based on the threshold
    if threshold_value > threshold:
        return 'white', black_value, white_value, threshold_value
    else:
        return 'black', black_value, white_value, threshold_value

# Function to detect the shape similarity using SSIM
def detect_shape(square_img):
    best_score = -1
    best_piece = 'empty'
    for piece in pieces:
        piece_img = cv2.imread(os.path.join(pieces_folder, piece + '.png'))
        score = compare_images(square_img, piece_img)
        if score > best_score:
            best_score = score
            best_piece = piece
    return best_piece

# Function to detect the board perspective
def detect_perspective():
    a1_template = cv2.imread('pieces/notation_a1_square.png')
    h8_template = cv2.imread('pieces/notation_h8_square.png')
    a1_square = cv2.imread(os.path.join(squares_folder, 'a1.png'))
    similarity_a1 = compare_images(a1_square, a1_template)
    similarity_h8 = compare_images(a1_square, h8_template)
    if similarity_a1 > similarity_h8:
        print("Board is in white's perspective.")
        return 'white'
    else:
        print("Board is in black's perspective.")
        return 'black'

# Function to detect pieces and apply correct board mapping
def detect_pieces(method="SSIM", threshold=0.5):
    perspective = detect_perspective()
    board_positions = board_positions_white if perspective == 'white' else board_positions_black
    white_pieces = []
    black_pieces = []

    for i, square_file in enumerate(sorted(os.listdir(squares_folder))):
        if square_file.endswith('.png'):
            square_path = os.path.join(squares_folder, square_file)
            square_img = cv2.imread(square_path)

            # Get the top piece based on SSIM
            probabilities = []
            for piece in pieces:
                piece_path = os.path.join(pieces_folder, piece + '.png')
                piece_img = cv2.imread(piece_path)
                similarity = compare_images(square_img, piece_img)
                probabilities.append(similarity)

            probabilities = np.array(probabilities)
            top_piece_index = np.argmax(probabilities)  # Get the best SSIM match
            top_piece = pieces[top_piece_index]  # Best matching piece

            # If the detected piece is empty, skip assigning any color
            if top_piece == 'empty':
                print(f"Square {board_positions[i]}: Final Piece: empty")
                continue  # Skip to the next square

            # Detect the color using color method with a threshold
            suggested_color, black_value, white_value, threshold_value = detect_color(square_img, threshold=threshold)

            # Assign the final piece based on the color detected
            if suggested_color == 'black':
                final_piece = 'b' + top_piece[1:]  # Force black color
            elif suggested_color == 'white':
                final_piece = 'w' + top_piece[1:]  # Force white color
            else:
                final_piece = 'empty'  # If neither color is detected

            # Print the final shape and detected color
            print(f"Square {board_positions[i]}: Final Piece: {final_piece}, Detected color: {suggested_color}")

            # Add the piece to the respective color's list
            if final_piece[0] == 'w':
                print(f'white piece: {final_piece[1]}{board_positions[i]}')
                white_pieces.append(f"{final_piece[1]}{board_positions[i]}")
            else:
                print(f'black piece: {final_piece[1]}{board_positions[i]}')
                black_pieces.append(f"{final_piece[1]}{board_positions[i]}")

    return white_pieces, black_pieces

# Save the detected pieces in human-readable format with proper ordering
def save_detected_positions(method="SSIM", threshold=0.5):
    white_pieces, black_pieces = detect_pieces(method=method, threshold=threshold)
    
    # Reorder pieces according to the specified format (pawns first, then king, queen, rook, bishop, knights)
    def reorder_pieces(pieces):
        order = ['P', 'K', 'Q', 'R', 'B', 'N']
        ordered_pieces = []
        for p in order:
            ordered_pieces.extend([piece for piece in pieces if piece[0] == p])
        return ordered_pieces
    
    white_pieces = reorder_pieces(white_pieces)
    black_pieces = reorder_pieces(black_pieces)
    
    # Detect perspective again for the move indication
    perspective = detect_perspective()
    move_text = "White to move" if perspective == 'white' else "Black to move"
    
    with open('piece_positions.txt', 'w') as f:
        f.write(f"White: {', '.join(white_pieces)}\n")
        f.write(f"Black: {', '.join(black_pieces)}\n")
        f.write(f"{move_text}\n")
        
    print(f"Positions saved in piece_positions.txt")