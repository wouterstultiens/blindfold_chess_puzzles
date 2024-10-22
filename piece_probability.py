import cv2
import numpy as np
import os
from skimage.metrics import structural_similarity as ssim

# Paths to the folders containing square images and pieces
squares_folder = 'screenshots/squares'
pieces_folder = 'pieces'

# List of all piece image names
pieces = ['bK', 'bQ', 'bR', 'bB', 'bN', 'bP', 'wK', 'wQ', 'wR', 'wB', 'wN', 'wP', 'empty']

# Board positions from white's perspective
board_positions_white = [f"{col}{row}" for row in range(1, 9) for col in 'abcdefgh']

# Board positions from black's perspective
board_positions_black = board_positions_white[::-1]

def compare_images(imageA, imageB):
    """
    Compares two images using SSIM and returns a similarity score.
    """
    imageB_resized = cv2.resize(imageB, (imageA.shape[1], imageA.shape[0]))
    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB_resized, cv2.COLOR_BGR2GRAY)
    score, _ = ssim(grayA, grayB, full=True)
    return score

def detect_color(image, threshold=1):
    """
    Detects the predominant color (black or white) in an image based on pixel intensity.
    """
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    total_pixels = rgb_image.shape[0] * rgb_image.shape[1]
    black_pixels = np.sum(np.all(rgb_image < 50, axis=2))
    white_pixels = np.sum(np.all(rgb_image > 200, axis=2))
    black_value = (black_pixels / total_pixels) * 100
    white_value = (white_pixels / total_pixels) * 100
    threshold_value = white_value / black_value if black_value != 0 else float('inf')
    if threshold_value > threshold:
        return 'white'
    else:
        return 'black'

def detect_perspective():
    """
    Detects the board perspective by comparing the 'a1' square with reference images.
    """
    a1_template = cv2.imread('pieces/notation_a1_square.png')
    h8_template = cv2.imread('pieces/notation_h8_square.png')
    a1_square = cv2.imread(os.path.join(squares_folder, 'a1.png'))
    similarity_a1 = compare_images(a1_square, a1_template)
    similarity_h8 = compare_images(a1_square, h8_template)
    return 'white' if similarity_a1 > similarity_h8 else 'black'

def detect_pieces(method="SSIM", threshold=0.5):
    """
    Detects pieces on the board and returns lists of white and black pieces.
    """
    perspective = detect_perspective()
    board_positions = board_positions_white if perspective == 'white' else board_positions_black
    white_pieces = []
    black_pieces = []

    for i, square_file in enumerate(sorted(os.listdir(squares_folder))):
        if square_file.endswith('.png'):
            square_path = os.path.join(squares_folder, square_file)
            square_img = cv2.imread(square_path)

            # Compare with all piece images to find the best match
            best_score = -1
            best_piece = 'empty'
            for piece in pieces:
                piece_img = cv2.imread(os.path.join(pieces_folder, piece + '.png'))
                score = compare_images(square_img, piece_img)
                if score > best_score:
                    best_score = score
                    best_piece = piece

            if best_piece == 'empty':
                continue

            # Detect the color of the piece
            detected_color = detect_color(square_img, threshold=threshold)
            final_piece = detected_color[0] + best_piece[1]

            # Add to the respective list
            position = board_positions[i]
            if final_piece.startswith('w'):
                white_pieces.append(f"{final_piece[1]}{position}")
            else:
                black_pieces.append(f"{final_piece[1]}{position}")

    return white_pieces, black_pieces

def save_detected_positions(method="SSIM", threshold=0.5):
    """
    Saves the detected piece positions to 'piece_positions.txt'.
    """
    white_pieces, black_pieces = detect_pieces(method=method, threshold=threshold)

    # Reorder pieces: pawns first, then K, Q, R, B, N
    def reorder_pieces(pieces_list):
        order = ['P', 'K', 'Q', 'R', 'B', 'N']
        return [piece for piece_type in order for piece in pieces_list if piece.startswith(piece_type)]

    white_pieces_ordered = reorder_pieces(white_pieces)
    black_pieces_ordered = reorder_pieces(black_pieces)

    perspective = detect_perspective()
    move_text = "White to move" if perspective == 'white' else "Black to move"

    with open('piece_positions.txt', 'w') as f:
        f.write(f"White: {', '.join(white_pieces_ordered)}\n")
        f.write(f"Black: {', '.join(black_pieces_ordered)}\n")
        f.write(f"{move_text}\n")
