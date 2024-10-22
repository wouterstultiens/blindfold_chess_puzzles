from chessboard_detector import detect_chessboard
from piece_probability import save_detected_positions

# Main function to call chessboard detection and piece identification
if __name__ == "__main__":
    print("Starting chessboard detection...")
    detect_chessboard()
    print("Chessboard detection completed.")
    
    print("Detecting pieces on the board...")
    save_detected_positions()
    print("Piece detection completed. Check 'piece_positions.txt' for results.")
