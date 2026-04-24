import tkinter as tk
import os

class Piece:
    def __init__(self, team, image):
        self.team = team
        self.image = image

class CheckerBoardGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LED Checkerboard GUI")

        # Create canvas with fixed size
        self.canvas_width = 880
        self.canvas_height = 640
        self.canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()

        # Load background image
        self.bg_image = tk.PhotoImage(file="Project_folder/background/background.png")
        # Place background image on the page
        self.canvas.create_image(0, 0, image=self.bg_image, anchor='nw')

        # Load checker images
        self.blue_checker_image = tk.PhotoImage(file=r"C:\Users\domin\AppData\Local\Programs\Python\Python313\Project_folder\blue_checkers\Blue checker.png")
        self.red_checker_image = tk.PhotoImage(file=r"C:\Users\domin\AppData\Local\Programs\Python\Python313\Project_folder\red_checkers\Red checker.png")

        # Create checker pieces
        self.pieces = []

        # Board positioning values
        start_x = 42
        start_y = 40
        square_size = 80

        # Blue checkers on top 3 rows
        for row in range(3):
            for col in range(4):
                x = start_x + ((col * 2) + ((row + 1) % 2)) * square_size
                y = start_y + row * square_size

                piece = Piece("B", self.blue_checker_image)
                piece.x = x
                piece.y = y
                piece.canvas_id = self.canvas.create_image(x, y, image=piece.image, anchor="center")
                self.pieces.append(piece)

        # Red checkers on bottom 3 rows
        for row in range(5, 8):
            for col in range(4):
                x = start_x + ((col * 2) + ((row + 1) % 2)) * square_size
                y = start_y + row * square_size

                piece = Piece("R", self.red_checker_image)
                piece.x = x
                piece.y = y
                piece.canvas_id = self.canvas.create_image(x, y, image=piece.image, anchor="center")
                self.pieces.append(piece)

        # Load counter icon images
        self.number_images = {}
        numbers_folder = "Project_folder/numbers"
        for num in range(13):
            image_path = os.path.join(numbers_folder, f"{num}.png")
            self.number_images[num] = tk.PhotoImage(file=image_path)

        self.counter1_value = 12
        self.counter1_x = 750
        self.counter1_y = 600
        self.counter1_image_id = self.canvas.create_image(self.counter1_x, self.counter1_y, image=self.number_images[self.counter1_value], anchor='center')

        self.counter2_value = 12
        self.counter2_x = 750
        self.counter2_y = 285
        self.counter2_image_id = self.canvas.create_image(self.counter2_x, self.counter2_y, image=self.number_images[self.counter2_value], anchor='center')

        # this section is what creates the decreasing function and can be easily swapped to work with other methods
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=13)
        
        dec_btn1 = tk.Button(btn_frame, text="Decrease", command=self.decrease_counter1)
        dec_btn1.pack(side='left', padx=10)

        dec_btn2 = tk.Button(btn_frame, text="Decrease", command=self.decrease_counter2)
        dec_btn2.pack(side='left', padx=10)

        # Used to keep track of which checker is selected
        self.selected_piece = None

        # Red starts first
        self.current_turn = "R"

        # Allow mouse clicks on the canvas
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        
    def on_canvas_click(self, event):
        clicked_x = event.x
        clicked_y = event.y

        # Check if a piece was clicked
        for piece in self.pieces:
            piece_x, piece_y = self.canvas.coords(piece.canvas_id)

            if abs(clicked_x - piece_x) < 35 and abs(clicked_y - piece_y) < 35:
                
                if piece.team != self.current_turn:
                    print("It is not your turn.")
                    return
                
                self.selected_piece = piece
                print("Selected piece:", piece.team)
                return

        # If no piece was clicked, move selected piece
        if self.selected_piece is not None:
            # Snap movement to the checkerboard squares
            start_x = 42
            start_y = 40
            square_size = 80

            col = round((clicked_x - start_x) / square_size)
            row = round((clicked_y - start_y) / square_size)

            new_x = start_x + col * square_size
            new_y = start_y + row * square_size

            old_x = self.selected_piece.x
            old_y = self.selected_piece.y

            x_change = abs(new_x - old_x)
            y_change = abs(new_y - old_y)

            # Allow diagonal movement by one square OR jumping by two squares
            if not (
                (x_change == square_size and y_change == square_size) or
                (x_change == 2 * square_size and y_change == 2 * square_size)
            ):
                print("Invalid Move: Checkers must move diagonally.")
                self.selected_piece = None
                returnelected_piece = None
                return

            # Enforce forward movement
            if self.selected_piece.team == "B":
                if new_y <= old_y:
                    print("Invalid Move: Blue pieces must move forward.")
                    self.selected_piece = None
                    return

            if self.selected_piece.team == "R":
                if new_y >= old_y:
                    print("Invalid Move: Red pieces must move forward.")
                    self.selected_piece = None
                    return
            
            # Do not allow moving onto another checker
            for piece in self.pieces:
                if piece != self.selected_piece:
                    if piece.x == new_x and piece.y == new_y:
                        print("Invalid Move: That square already has a checker.")
                        self.selected_piece = None
                        return

            # If jumping, remove the checker being jumped over
            if x_change == 2 * square_size and y_change == 2 * square_size:
                middle_x = (old_x + new_x) / 2
                middle_y = (old_y + new_y) / 2

                for piece in self.pieces:
                    if piece.x == middle_x and piece.y == middle_y:
                        if piece.team == self.selected_piece.team:
                            print("Invalid Move: You cannot jump over your own checker.")
                            self.selected_piece = None
                            return

                        self.canvas.delete(piece.canvas_id)
                        self.pieces.remove(piece)
                        print("Captured piece:", piece.team)
                        break
            
            self.canvas.coords(self.selected_piece.canvas_id, new_x, new_y)

            self.selected_piece.x = new_x
            self.selected_piece.y = new_y

            print("Moved piece to:", new_x, new_y)

            # Switch turns after a successful move
            if self.current_turn == "B":
                self.current_turn = "R"
            else:
                self.current_turn = "B"

            print("Current turn:", self.current_turn)

            self.selected_piece = None
    
    def update_counter1_image(self):
        # Update the canvas image to the current counter 1 value
        self.canvas.itemconfig(self.counter1_image_id, image=self.number_images[self.counter1_value])

    def decrease_counter1(self):
        if self.counter1_value > 0:
            self.counter1_value -= 1
            self.update_counter1_image()

    def update_counter2_image(self):
        # Update the canvas image to the current counter 2 value
        self.canvas.itemconfig(self.counter2_image_id, image=self.number_images[self.counter2_value])

    def decrease_counter2(self):
        if self.counter2_value > 0:
            self.counter2_value -= 1
            self.update_counter2_image()
            
if __name__ == "__main__":
    app = CheckerBoardGUI()
    app.mainloop()
