import cv2
import numpy as np
import os
from skimage.metrics import structural_similarity as ssim

# Path to the folders containing square images and pieces
squares_folder = 'screenshots/squares'
pieces_folder = 'pieces'

# List of all piece image names in logical order
pieces = ['bK', 'bQ', 'bR', 'bB', 'bN', 'bP', 'wK', 'wQ', 'wR', 'wB', 'wN', 'wP', 'empty']

# Mapping from file numbers to board coordinates after a 270-degree clockwise (or 90-degree counterclockwise) rotation
board_positions = {
    0: "a1", 1: "a2", 2: "a3", 3: "a4", 4: "a5", 5: "a6", 6: "a7", 7: "a8",
    8: "b1", 9: "b2", 10: "b3", 11: "b4", 12: "b5", 13: "b6", 14: "b7", 15: "b8",
    16: "c1", 17: "c2", 18: "c3", 19: "c4", 20: "c5", 21: "c6", 22: "c7", 23: "c8",
    24: "d1", 25: "d2", 26: "d3", 27: "d4", 28: "d5", 29: "d6", 30: "d7", 31: "d8",
    32: "e1", 33: "e2", 34: "e3", 35: "e4", 36: "e5", 37: "e6", 38: "e7", 39: "e8",
    40: "f1", 41: "f2", 42: "f3", 43: "f4", 44: "f5", 45: "f6", 46: "f7", 47: "f8",
    48: "g1", 49: "g2", 50: "g3", 51: "g4", 52: "g5", 53: "g6", 54: "g7", 55: "g8",
    56: "h1", 57: "h2", 58: "h3", 59: "h4", 60: "h5", 61: "h6", 62: "h7", 63: "h8",
}

# Function to compare two images using SSIM and return a similarity score
def compare_images(imageA, imageB):
    imageB = cv2.resize(imageB, (imageA.shape[1], imageA.shape[0]))
    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
    score, _ = ssim(grayA, grayB, full=True)
    return score

# Function to detect pieces and output probabilities
def detect_pieces():
    white_pieces = []
    black_pieces = []
    
    for i, square_file in enumerate(sorted(os.listdir(squares_folder))):
        if square_file.endswith('.png'):
            square_path = os.path.join(squares_folder, square_file)
            square_img = cv2.imread(square_path)
            probabilities = []

            # Compare the square image with each piece image
            for piece in pieces:
                piece_path = os.path.join(pieces_folder, piece + '.png')
                piece_img = cv2.imread(piece_path)
                similarity = compare_images(square_img, piece_img)
                probabilities.append(similarity)

            # Normalize probabilities
            probabilities = np.array(probabilities)
            probabilities = probabilities / probabilities.sum()

            # Get the most likely piece
            top_piece_index = np.argmax(probabilities)
            top_piece = pieces[top_piece_index]

            # Store the results for later use
            if top_piece != 'empty':
                pos = board_positions[i]
                if top_piece[0] == 'w':
                    white_pieces.append(f"{top_piece[1]}{pos}")
                else:
                    black_pieces.append(f"{top_piece[1]}{pos}")

    return white_pieces, black_pieces

# Save the detected pieces in human-readable format
def save_detected_positions():
    white_pieces, black_pieces = detect_pieces()
    
    with open('piece_positions.txt', 'w') as f:
        f.write(f"White: {', '.join(white_pieces)}\n")
        f.write(f"Black: {', '.join(black_pieces)}\n")
    print(f"Positions saved in piece_positions.txt")

