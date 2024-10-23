import os
import cv2
import numpy as np
import csv
from datetime import datetime
import tkinter as tk
from skimage.metrics import structural_similarity as ssim

# Paths to the folders containing square images and pieces
squares_folder = 'screenshots/squares'
pieces_folder = 'pieces'

# List of all piece image names
pieces = ['bK', 'bQ', 'bR', 'bB', 'bN', 'bP', 'wK', 'wQ', 'wR', 'wB', 'wN', 'wP', 'empty']

# Board positions from white's perspective
board_positions_white = [
    "a1", "a2", "a3", "a4", "a5", "a6", "a7", "a8",
    "b1", "b2", "b3", "b4", "b5", "b6", "b7", "b8",
    "c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8",
    "d1", "d2", "d3", "d4", "d5", "d6", "d7", "d8",
    "e1", "e2", "e3", "e4", "e5", "e6", "e7", "e8",
    "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8",
    "g1", "g2", "g3", "g4", "g5", "g6", "g7", "g8",
    "h1", "h2", "h3", "h4", "h5", "h6", "h7", "h8"
]

board_positions_black = board_positions_white[::-1]

# Ensure CSV headers
def initialize_csv():
    if not os.path.exists('puzzle_results.csv'):
        with open('puzzle_results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Date', 'Puzzle Text', 'Number of Pieces', 'Rating Range', 'Result'])

# Function to compare two images using SSIM
def compare_images(imageA, imageB):
    imageB_resized = cv2.resize(imageB, (imageA.shape[1], imageA.shape[0]))
    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB_resized, cv2.COLOR_BGR2GRAY)
    score, _ = ssim(grayA, grayB, full=True)
    return score

# Function to detect predominant color (black/white)
def detect_color(image, threshold=1):
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

# Function to detect perspective
def detect_perspective():
    a1_template = cv2.imread('pieces/notation_a1_square.png')
    h8_template = cv2.imread('pieces/notation_h8_square.png')
    a1_square = cv2.imread(os.path.join(squares_folder, 'a1.png'))
    similarity_a1 = compare_images(a1_square, a1_template)
    similarity_h8 = compare_images(a1_square, h8_template)
    return 'white' if similarity_a1 > similarity_h8 else 'black'

# Function to detect pieces and return detected pieces and their positions
def detect_pieces(method="SSIM", threshold=0.5):
    perspective = detect_perspective()
    board_positions = board_positions_white if perspective == 'white' else board_positions_black
    white_pieces = []
    black_pieces = []

    for i, square_file in enumerate(sorted(os.listdir(squares_folder))):
        if square_file.endswith('.png'):
            square_path = os.path.join(squares_folder, square_file)
            square_img = cv2.imread(square_path)

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

            detected_color = detect_color(square_img, threshold=threshold)
            final_piece = detected_color[0] + best_piece[1]

            position = board_positions[i]
            if final_piece.startswith('w'):
                white_pieces.append(f"{final_piece[1]}{position}")
            else:
                black_pieces.append(f"{final_piece[1]}{position}")

    return white_pieces, black_pieces

# Function to log puzzle metadata and results into a CSV file
def log_puzzle_result(puzzle_id, puzzle_text, num_pieces, rating_range, result):
    # Replace any line breaks with " - " in the puzzle_text
    puzzle_text = puzzle_text.replace("\n", " - ")
    
    with open('puzzle_results.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([puzzle_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), puzzle_text, num_pieces, rating_range, result])

# Function to handle GUI interactions and result submission
def submit_result(result, puzzle_text, num_pieces, rating_range, window):
    puzzle_id = datetime.now().strftime("%Y%m%d%H%M%S")
    log_puzzle_result(puzzle_id, puzzle_text, num_pieces, rating_range, result)
    window.destroy()

# GUI for displaying puzzle and recording results
def display_puzzle_gui(puzzle_text, num_pieces, rating_range):
    window = tk.Tk()
    window.title("Chess Puzzle")

    # Set window size and center it on the screen
    window.geometry('500x300')
    window.eval('tk::PlaceWindow . center')

    label = tk.Label(window, text=f"Puzzle:\n{puzzle_text}", font=("Arial", 14), wraplength=450)
    label.pack(pady=20)

    btn_frame = tk.Frame(window)
    btn_frame.pack(pady=20)

    # Create buttons with larger size and pastel colors
    tk.Button(btn_frame, text="Right", width=12, height=2, bg="#77dd77", command=lambda: submit_result("right", puzzle_text, num_pieces, rating_range, window)).pack(side="left", padx=10)
    tk.Button(btn_frame, text="Wrong", width=12, height=2, bg="#ff6961", command=lambda: submit_result("wrong", puzzle_text, num_pieces, rating_range, window)).pack(side="left", padx=10)
    tk.Button(btn_frame, text="N/A", width=12, height=2, bg="#cfcfc4", command=lambda: submit_result("N/A", puzzle_text, num_pieces, rating_range, window)).pack(side="left", padx=10)

    # Ensure the window is brought to the front and focused
    window.attributes('-topmost', True)
    window.mainloop()

# Main function to detect and display the puzzle in a window
def print_detected_positions(method="SSIM", threshold=0.5):
    initialize_csv()
    white_pieces, black_pieces = detect_pieces(method=method, threshold=threshold)

    def reorder_pieces(pieces_list):
        order = ['K', 'P', 'Q', 'R', 'B', 'N']
        return [piece for piece_type in order for piece in pieces_list if piece.startswith(piece_type)]

    white_pieces_ordered = reorder_pieces(white_pieces)
    black_pieces_ordered = reorder_pieces(black_pieces)

    perspective = detect_perspective()
    move_text = "White to move" if perspective == 'white' else "Black to move"

    puzzle_text = f"{move_text}\nWhite: {', '.join(white_pieces_ordered)}\nBlack: {', '.join(black_pieces_ordered)}"
    num_pieces = "3-5"
    rating_range = "0-1000"

    # Display the puzzle and options in a graphical window
    display_puzzle_gui(puzzle_text, num_pieces, rating_range)

# Example of usage
if __name__ == "__main__":
    print_detected_positions(method="SSIM", threshold=0.5)
