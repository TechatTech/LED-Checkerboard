import tkinter as tk
from tkinter import messagebox
import os

class Piece:
    def __init__(self, team, image):
        self.team = team
        self.image = image
        self.king = False

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
        self.blue_king_image = tk.PhotoImage(file=r"C:\Users\domin\AppData\Local\Programs\Python\Python313\Project_folder\blue_checkers\Blue king.png")
        self.red_king_image = tk.PhotoImage(file=r"C:\Users\domin\AppData\Local\Programs\Python\Python313\Project_folder\red_checkers\Red king.png")

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

        # Used to highlight the valid moves of the selected checker
        self.highlighted_squares = []

        #Used to prevent users from clicking non-highlighted squares
        self.valid_move_positions = []

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

                self.highlight_valid_moves(piece)
                
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

            # Prevent moves outside the board
            board_min_x = start_x
            board_max_x = start_x + 7 * square_size
            board_min_y = start_y
            board_max_y = start_y + 7 * square_size

            if new_x < board_min_x or new_x > board_max_x or new_y < board_min_y or new_y > board_max_y:
                print("Invalid Move: You cannot move off the board.")
                self.selected_piece = None
                self.clear_highlights()
                return

            if (new_x, new_y) not in self.valid_move_positions:
                print("Invalid Move: You must click a highlighted square.")
                self.selected_piece = None
                self.clear_highlights()
                return
            
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
                return

            # Enforce forward movement unless the piece is a king
            if self.selected_piece.king == False:
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

                captured_piece_found = False

                for piece in self.pieces:
                    if piece.x == middle_x and piece.y == middle_y:
                        if piece.team == self.selected_piece.team:
                            print("Invalid Move: You cannot jump over your own checker.")
                            self.selected_piece = None
                            return

                        self.canvas.delete(piece.canvas_id)
                        self.pieces.remove(piece)
                        print("Captured Piece:", piece.team)

                        self.update_checker_counts()

                        self.check_winner()
                        
                        captured_piece_found = True
                        break

                if captured_piece_found == False:
                    print("Invalid Move: No checker to jump over.")
            
            self.canvas.coords(self.selected_piece.canvas_id, new_x, new_y)

            self.selected_piece.x = new_x
            self.selected_piece.y = new_y

            # Make piece a king if it reaches the opposite side
            if self.selected_piece.team == "R" and new_y == start_y:
                self.selected_piece.king = True
                self.selected_piece.image = self.red_king_image
                self.canvas.itemconfig(self.selected_piece.canvas_id, image=self.red_king_image)
                print("Red piece became a king!")

            if self.selected_piece.team == "B" and new_y == start_y + 7 * square_size:
                self.selected_piece.king = True
                self.selected_piece.image = self.blue_king_image
                self.canvas.itemconfig(self.selected_piece.canvas_id, image=self.blue_king_image)
                print("Blue piece became a king!")

            print("Moved piece to:", new_x, new_y)

            self.clear_highlights()

            # If a jump was made and another jump is possible, keep the same turn
            if x_change == 2 * square_size and y_change == 2 * square_size:
                if self.double_jump(self.selected_piece):
                    print("Double jump available. Same player goes again.")
                    self.highlight_valid_moves(self.selected_piece)
                    return

            # Switch turns after a successful move
            if self.current_turn == "B":
                self.current_turn = "R"
            else:
                self.current_turn = "B"

            print("Current turn:", self.current_turn)
    
    def check_winner(self):
        red_count = 0
        blue_count = 0

        for piece in self.pieces:
            if piece.team == "R":
                red_count += 1
            elif piece.team == "B":
                blue_count += 1

        if red_count == 0:
            messagebox.showinfo("Game Over", "Blue wins!")
            self.canvas.unbind("<Button-1>")

        elif blue_count == 0:
            messagebox.showinfo("Game Over", "Red wins!")
            self.canvas.unbind("<Button-1>")
    
    def clear_highlights(self):
        for highlight in self.highlighted_squares:
            self.canvas.delete(highlight)

        self.highlighted_squares = []
        self.valid_move_positions = []

    def highlight_valid_moves(self, piece):
        self.clear_highlights()

        square_size = 80
        start_x = 42
        start_y = 40

        board_min_x = start_x
        board_max_x = start_x + 7 * square_size
        board_min_y = start_y
        board_max_y = start_y + 7 * square_size

        # Track if any jump exists
        jump_exists = False
        jump_positions = []

        # Jump directions 
        if piece.king:
            jump_directions = [(-2, -2), (2, -2), (-2, 2), (2, 2)]
        elif piece.team == "R":
            jump_directions = [(-2, -2), (2, -2)]
        else:
            jump_directions = [(-2, 2), (2, 2)]

        # Check for jumps first
        for col_change, row_change in jump_directions:
            new_x = piece.x + col_change * square_size
            new_y = piece.y + row_change * square_size

            # Boundary check
            if new_x < board_min_x or new_x > board_max_x or new_y < board_min_y or new_y > board_max_y:
                continue

            middle_x = piece.x + (col_change // 2) * square_size
            middle_y = piece.y + (row_change // 2) * square_size

            middle_piece = None
            landing_empty = True

            for other_piece in self.pieces:
                if other_piece.x == middle_x and other_piece.y == middle_y:
                    middle_piece = other_piece

                if other_piece.x == new_x and other_piece.y == new_y:
                    landing_empty = False

            if middle_piece is not None and middle_piece.team != piece.team and landing_empty:
                jump_exists = True
                jump_positions.append((new_x, new_y))

        # If jumps exist, only show jumps
        if jump_exists:
            for jump_x, jump_y in jump_positions:
                highlight = self.canvas.create_rectangle(
                    jump_x - 40, jump_y - 40,
                    jump_x + 40, jump_y + 40,
                    outline="red",
                    width=4
                )

                self.highlighted_squares.append(highlight)
                self.valid_move_positions.append((jump_x, jump_y))

            return  

        # Otherwise show normal moves
        if piece.king == True:
            directions = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
        elif piece.team == "R":
            directions = [(-1, -1), (1, -1)]
        else:
            directions = [(-1, 1), (1, 1)]

        for col_change, row_change in directions:
            new_x = piece.x + col_change * square_size
            new_y = piece.y + row_change * square_size

            # Boundary check
            if new_x < board_min_x or new_x > board_max_x or new_y < board_min_y or new_y > board_max_y:
                continue

            square_is_empty = True

            for other_piece in self.pieces:
                if other_piece.x == new_x and other_piece.y == new_y:
                    square_is_empty = False

            if square_is_empty == False:
                continue

            highlight = self.canvas.create_rectangle(
                new_x - 40, new_y - 40,
                new_x + 40, new_y + 40,
                outline="yellow",
                width=4
            )

            self.highlighted_squares.append(highlight)
            self.valid_move_positions.append((new_x, new_y))
    
    def double_jump(self, piece):
        start_x = 42
        start_y = 40
        square_size = 80

        directions = [(-2, -2), (2, -2), (-2, 2), (2, 2)]

        for col_change, row_change in directions:
            new_x = piece.x + col_change * square_size
            new_y = piece.y + row_change * square_size

            middle_x = piece.x + (col_change // 2) * square_size
            middle_y = piece.y + (row_change // 2) * square_size

            middle_piece = None
            landing_empty = True

            for other in self.pieces:
                if other.x == middle_x and other.y == middle_y:
                    middle_piece = other
                if other.x == new_x and other.y == new_y:
                    landing_empty = False

            if middle_piece and middle_piece.team != piece.team and landing_empty:
                return True

        return False
    
    def update_checker_counts(self):
        red_count = 0
        blue_count = 0

        for piece in self.pieces:
            if piece.team == "R":
                red_count += 1
            elif piece.team == "B":
                blue_count += 1

        self.counter1_value = red_count
        self.counter2_value = blue_count

        self.update_counter1_image()
        self.update_counter2_image()
    
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
