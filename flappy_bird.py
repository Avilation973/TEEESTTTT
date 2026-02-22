import random
import tkinter as tk


class FlappyBirdGame:
    WIDTH = 480
    HEIGHT = 640
    GRAVITY = 0.5
    FLAP_STRENGTH = -9
    PIPE_SPEED = 4
    PIPE_GAP = 180
    PIPE_WIDTH = 70
    PIPE_INTERVAL_MS = 1600

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Flappy Bird")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(
            root,
            width=self.WIDTH,
            height=self.HEIGHT,
            bg="#70c5ce",
            highlightthickness=0,
        )
        self.canvas.pack()

        self.bird_x = 120
        self.bird_y = self.HEIGHT // 2
        self.bird_radius = 18
        self.bird_vel = 0.0

        self.pipes: list[dict] = []
        self.score = 0
        self.running = True
        self.started = False

        self.score_text = self.canvas.create_text(
            self.WIDTH // 2,
            60,
            text="Skor: 0",
            font=("Arial", 26, "bold"),
            fill="white",
        )
        self.info_text = self.canvas.create_text(
            self.WIDTH // 2,
            self.HEIGHT // 2,
            text="Başlamak için BOŞLUK'a bas",
            font=("Arial", 20, "bold"),
            fill="white",
        )

        self.root.bind("<space>", self.on_flap)
        self.root.bind("<Button-1>", self.on_flap)

        self.spawn_pipe()
        self.loop()

    def on_flap(self, _event=None) -> None:
        if not self.running:
            self.restart()
            return
        self.started = True
        self.canvas.itemconfig(self.info_text, text="")
        self.bird_vel = self.FLAP_STRENGTH

    def restart(self) -> None:
        self.pipes.clear()
        self.canvas.delete("pipe")
        self.bird_y = self.HEIGHT // 2
        self.bird_vel = 0.0
        self.score = 0
        self.running = True
        self.started = False
        self.canvas.itemconfig(self.score_text, text="Skor: 0")
        self.canvas.itemconfig(self.info_text, text="Başlamak için BOŞLUK'a bas")
        self.spawn_pipe()

    def spawn_pipe(self) -> None:
        if not self.running:
            return
        margin = 90
        gap_top = random.randint(margin, self.HEIGHT - margin - self.PIPE_GAP)
        pipe = {
            "x": self.WIDTH + 20,
            "top": gap_top,
            "bottom": gap_top + self.PIPE_GAP,
            "scored": False,
        }
        self.pipes.append(pipe)
        self.root.after(self.PIPE_INTERVAL_MS, self.spawn_pipe)

    def draw(self) -> None:
        self.canvas.delete("bird")
        self.canvas.delete("pipe")

        # Ground
        self.canvas.create_rectangle(
            0,
            self.HEIGHT - 70,
            self.WIDTH,
            self.HEIGHT,
            fill="#ded895",
            outline="#ded895",
            tags="ground",
        )

        # Bird
        self.canvas.create_oval(
            self.bird_x - self.bird_radius,
            self.bird_y - self.bird_radius,
            self.bird_x + self.bird_radius,
            self.bird_y + self.bird_radius,
            fill="#ffeb3b",
            outline="#fbc02d",
            width=2,
            tags="bird",
        )

        # Pipes
        for p in self.pipes:
            self.canvas.create_rectangle(
                p["x"],
                0,
                p["x"] + self.PIPE_WIDTH,
                p["top"],
                fill="#5abf41",
                outline="#3f8f2f",
                width=2,
                tags="pipe",
            )
            self.canvas.create_rectangle(
                p["x"],
                p["bottom"],
                p["x"] + self.PIPE_WIDTH,
                self.HEIGHT - 70,
                fill="#5abf41",
                outline="#3f8f2f",
                width=2,
                tags="pipe",
            )

    def update_game(self) -> None:
        if not self.running or not self.started:
            return

        self.bird_vel += self.GRAVITY
        self.bird_y += self.bird_vel

        for p in self.pipes:
            p["x"] -= self.PIPE_SPEED

            if not p["scored"] and p["x"] + self.PIPE_WIDTH < self.bird_x:
                p["scored"] = True
                self.score += 1
                self.canvas.itemconfig(self.score_text, text=f"Skor: {self.score}")

        self.pipes = [p for p in self.pipes if p["x"] + self.PIPE_WIDTH > -10]

        # Collision: floor/ceiling
        if self.bird_y - self.bird_radius <= 0 or self.bird_y + self.bird_radius >= self.HEIGHT - 70:
            self.game_over()
            return

        # Collision: pipes
        for p in self.pipes:
            bird_left = self.bird_x - self.bird_radius
            bird_right = self.bird_x + self.bird_radius
            bird_top = self.bird_y - self.bird_radius
            bird_bottom = self.bird_y + self.bird_radius

            pipe_left = p["x"]
            pipe_right = p["x"] + self.PIPE_WIDTH

            overlaps_x = bird_right > pipe_left and bird_left < pipe_right
            hits_top_pipe = bird_top < p["top"]
            hits_bottom_pipe = bird_bottom > p["bottom"]

            if overlaps_x and (hits_top_pipe or hits_bottom_pipe):
                self.game_over()
                return

    def game_over(self) -> None:
        self.running = False
        self.canvas.itemconfig(
            self.info_text,
            text=f"Oyun Bitti!\nSkor: {self.score}\nTekrar başlamak için BOŞLUK",
        )

    def loop(self) -> None:
        self.update_game()
        self.draw()
        self.root.after(16, self.loop)


def main() -> None:
    root = tk.Tk()
    FlappyBirdGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
