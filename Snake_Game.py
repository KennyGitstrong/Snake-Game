import tkinter as tk
import random


class SnakeGame:
    def __init__(self, master, size=20):
        self.master = master
        self.size = size
        self.canvas = tk.Canvas(master, width=size * 20, height=size * 20, bg="black")
        self.canvas.pack()

        self.snake = [(size // 2, size // 2)]
        self.food = self.spawn_food()

        self.direction = (0, 0)
        self.score = 0  # Initialize score

        # Create Quit button
        self.quit_button = tk.Button(master, text="Quit", command=self.master.destroy)
        self.quit_button.pack(side="right", padx=10)

        # Create Start New Game button
        self.new_game_button = tk.Button(master, text="Start New Game", command=self.start_new_game)
        self.new_game_button.pack(side="left", padx=10)

        # Create a label to display the score
        self.score_label = tk.Label(master, text="Score: {}".format(self.score), fg="white", font=("Helvetica", 16))
        self.score_label.pack()

        self.master.bind("<KeyPress>", self.on_key_press)
        self.update()

    def on_key_press(self, event):
        key = event.keysym
        if key == "Up" and self.direction != (0, 1):
            self.direction = (0, -1)
        elif key == "Down" and self.direction != (0, -1):
            self.direction = (0, 1)
        elif key == "Left" and self.direction != (1, 0):
            self.direction = (-1, 0)
        elif key == "Right" and self.direction != (-1, 0):
            self.direction = (1, 0)

    def spawn_food(self):
        x = random.randint(0, self.size - 1)
        y = random.randint(0, self.size - 1)
        return x, y

    def update(self):
        head = (self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1])
        self.snake.insert(0, head)

        if head == self.food:
            self.food = self.spawn_food()
            self.score += 1  # Increment score when the snake eats the food

        else:
            self.snake.pop()

        self.draw_snake()
        self.draw_food()
        self.update_score()  # Update the displayed score

        if self.check_collision():
            self.game_over()

        self.master.after(100, self.update)

    def draw_snake(self):
        self.canvas.delete("snake")
        for x, y in self.snake:
            self.canvas.create_rectangle(x * 20, y * 20, (x + 1) * 20, (y + 1) * 20, fill="green", tags="snake")

    def draw_food(self):
        self.canvas.delete("food")
        x, y = self.food
        self.canvas.create_rectangle(x * 20, y * 20, (x + 1) * 20, (y + 1) * 20, fill="red", tags="food")

    def update_score(self):
        self.score_label.config(text="Score: {}".format(self.score))

    def check_collision(self):
        x, y = self.snake[0]
        return x < 0 or x >= self.size or y < 0 or y >= self.size or self.snake[0] in self.snake[1:]

    def game_over(self):
        self.canvas.create_text(self.size * 10, self.size * 10, text="Game Over", fill="white", font=("Helvetica", 16))
        self.canvas.create_text(self.size * 10, self.size * 12, text="Final Score: {}".format(self.score), fill="white", font=("Helvetica", 16))
        self.quit_button.config(state="normal")
        self.new_game_button.config(state="normal")
        self.master.bind("<KeyPress>", self.on_game_over_key_press)

    def start_new_game(self):
        self.master.destroy()
        new_game_root = tk.Tk()
        new_game_root.title("Snake Game")
        new_game = SnakeGame(new_game_root)
        new_game_root.mainloop()

    def on_game_over_key_press(self, event):
        key = event.keysym
        if key == "q":
            self.master.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Snake Game")

    game = SnakeGame(root)

    root.mainloop()
