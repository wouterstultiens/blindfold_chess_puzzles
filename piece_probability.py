import cv2
import numpy as np
import os
from skimage.metrics import structural_similarity as ssim

# Path to the folders containing square images and pieces
squares_folder = 'screenshots/squares'
pieces_folder = 'pieces'

# List of all piece image names in logical order
pieces = ['bK', 'bQ', 'bR', 'bB', 'bN', 'bP', 'wK', 'wQ', 'wR', 'wB', 'wN', 'wP', 'empty']

# Mapping from file numbers to board coordinates
board_positions = {
    0: "a8", 1: "b8", 2: "c8", 3: "d8", 4: "e8", 5: "f8", 6: "g8", 7: "h8",
    8: "a7", 9: "b7", 10: "c7", 11: "d7", 12: "e7", 13: "f7", 14: "g7", 15: "h7",
    16: "a6", 17: "b6", 18: "c6", 19: "d6", 20: "e6", 21: "f6", 22: "g6", 23: "h6",
    24: "a5", 25: "b5", 26: "c5", 27: "d5", 28: "e5", 29: "f5", 30: "g5", 31: "h5",
    32: "a4", 33: "b4", 34: "c4", 35: "d4", 36: "e4", 37: "f4", 38: "g4", 39: "h4",
    40: "a3", 41: "b3", 42: "c3", 43: "d3", 44: "e3", 45: "f3", 46: "g3", 47: "h3",
    48: "a2", 49: "b2", 50: "c2", 51: "d2", 52: "e2", 53: "f2", 54: "g2", 55: "h2",
    56: "a1", 57: "b1", 58: "c1", 59: "d1", 60: "e1", 61: "f1", 62: "g1", 63: "h1",
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

