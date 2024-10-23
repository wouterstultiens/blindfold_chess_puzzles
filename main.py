import os
import tkinter as tk
from chessboard_detector import detect_chessboard
from square_detector import detect_and_save_squares, create_squares_folder
from piece_probability import print_detected_positions

def popup_choice():
    """
    Creates a popup window with "Next" and "Stop" options.
    Returns 'next' if 'Next' is clicked and 'stop' if 'Stop' is clicked.
    """
    window = tk.Tk()
    window.title("Choose Action")

    # Set window size
    window_width = 500
    window_height = 300

    # Calculate x and y coordinates for the top-right corner
    x = 1350
    y = 50  # Top of the screen

    # Set the geometry of the window to top-right
    window.geometry(f'{window_width}x{window_height}+{x}+{y}')

    # Create StringVar after initializing the window
    choice = tk.StringVar()

    def on_next():
        choice.set('next')
        window.destroy()

    def on_stop():
        choice.set('stop')
        window.destroy()

    # Label at the top
    label = tk.Label(window, text="Select your action:", font=("Arial", 14))
    label.pack(pady=20)

    # Create a frame for buttons to organize them side by side
    btn_frame = tk.Frame(window)
    btn_frame.pack(pady=20)

    # Create buttons with larger size and match design to other pop-up
    next_button = tk.Button(btn_frame, text="Next", width=12, height=2, bg="#77dd77", command=on_next)
    next_button.pack(side="left", padx=10)

    stop_button = tk.Button(btn_frame, text="Stop", width=12, height=2, bg="#ff6961", command=on_stop)
    stop_button.pack(side="left", padx=10)

    # Ensure the window is brought to the front and focused
    window.attributes('-topmost', True)
    window.mainloop()

    return choice.get()

if __name__ == "__main__":
    while True:
        user_choice = popup_choice()
        
        if user_choice == 'next':
            # Proceed with the main program logic
            detect_chessboard()

            # Paths
            image_path = os.path.join('screenshots', 'cropped_chessboard.png')
            squares_folder = os.path.join('screenshots', 'squares')

            # Create the 'squares' folder and detect squares
            create_squares_folder(squares_folder)
            detect_and_save_squares(image_path, squares_folder)

            # Detect pieces and save positions
            print_detected_positions(method="SSIM", threshold=0.5)
        else:
            # Exit the loop and stop the program if "Stop" is selected
            print("Program stopped by user.")
            break
