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
                piece.canvas_id = self.canvas.create_image(x, y, image=piece.image, anchor="center")
                self.pieces.append(piece)

        # Red checkers on bottom 3 rows
        for row in range(5, 8):
            for col in range(4):
                x = start_x + ((col * 2) + ((row + 1) % 2)) * square_size
                y = start_y + row * square_size

                piece = Piece("R", self.red_checker_image)
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
