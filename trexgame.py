import tkinter as tk
import random

class TRexGame:
    def __init__(self):
        # Create the main window
        self.window = tk.Tk()
        self.window.title("T-Rex Game")
        self.window.geometry("800x400")
        self.window.resizable(False, False)
        
        # Create the canvas
        self.canvas = tk.Canvas(self.window, width=800, height=400, bg="white")
        self.canvas.pack()
        
        # Game variables
        self.score = 0
        self.high_score = self.get_high_score()
        self.game_speed = 5
        self.is_jumping = False
        self.jump_velocity = 0
        self.gravity = 1
        self.game_over = False
        self.obstacles = []
        self.passed_obstacles = set()
        
        # Create game elements
        self.create_ground()
        self.create_trex()
        self.create_score_display()
        
        # Bind keys
        self.window.bind("<space>", self.jump)
        self.window.bind("<KeyPress-r>", self.restart_game)
        
        # Start game loop
        self.spawn_obstacle()
        self.game_loop()
        
        # Start the main loop
        self.window.mainloop()
    
    def get_high_score(self):
        """Get the high score from the file"""
        try:
            with open("high_score.txt", "r") as file:
                return int(file.read())
        except FileNotFoundError:
            return 0
    
    def set_high_score(self, score):
        """Set the high score in the file"""
        with open("high_score.txt", "w") as file:
            file.write(str(score))
    
    def create_ground(self):
        """Create the ground line"""
        self.ground_y = 300
        self.canvas.create_line(0, self.ground_y, 800, self.ground_y, width=2, fill="black")
    
    def create_trex(self):
        """Create the T-Rex character"""
        self.trex_x = 50
        self.trex_y = self.ground_y - 50
        self.trex_width = 40
        self.trex_height = 50
        
        self.trex = self.canvas.create_rectangle(
            self.trex_x, 
            self.trex_y,
            self.trex_x + self.trex_width,
            self.trex_y + self.trex_height,
            fill="green", 
            outline="darkgreen",
            width=2
        )
    
    def create_score_display(self):
        """Create score and high score display"""
        self.score_text = self.canvas.create_text(
            700, 30, 
            text=f"Score: {self.score}", 
            font=("Arial", 16, "bold"),
            fill="black"
        )
        self.high_score_text = self.canvas.create_text(
            700, 60, 
            text=f"High Score: {self.high_score}", 
            font=("Arial", 12),
            fill="gray"
        )
    
    def jump(self, event=None):
        """Make the T-Rex jump"""
        if not self.is_jumping and not self.game_over:
            self.is_jumping = True
            self.jump_velocity = -15
    
    def update_jump(self):
        """Update jump physics"""
        if self.is_jumping:
            coords = self.canvas.coords(self.trex)
            current_y = coords[1]
            
            # Apply velocity
            new_y = current_y + self.jump_velocity
            self.canvas.move(self.trex, 0, self.jump_velocity)
            
            # Apply gravity
            self.jump_velocity += self.gravity
            
            # Check if landed
            if new_y >= self.trex_y:
                # Reset to ground
                self.canvas.coords(
                    self.trex,
                    self.trex_x,
                    self.trex_y,
                    self.trex_x + self.trex_width,
                    self.trex_y + self.trex_height
                )
                self.is_jumping = False
                self.jump_velocity = 0
    
    def spawn_obstacle(self):
        """Spawn a new obstacle"""
        if not self.game_over:
            # Random obstacle height
            heights = [30, 40, 50, 60]
            height = random.choice(heights)
            width = 20
            
            x = 800
            y = self.ground_y - height
            
            obstacle = self.canvas.create_rectangle(
                x, y, x + width, self.ground_y,
                fill="brown",
                outline="saddlebrown",
                width=2
            )
            
            self.obstacles.append(obstacle)
            
            # Schedule next obstacle with random delay
            delay = random.randint(1500, 3000)
            self.window.after(delay, self.spawn_obstacle)
    
    def move_obstacles(self):
        """Move all obstacles to the left"""
        obstacles_to_remove = []
        
        for obstacle in self.obstacles:
            # Move obstacle
            self.canvas.move(obstacle, -self.game_speed, 0)
            
            # Check if obstacle is off screen
            coords = self.canvas.coords(obstacle)
            if coords[2] < 0:
                obstacles_to_remove.append(obstacle)
            
            # Check if obstacle was passed (for scoring)
            if coords[2] < self.trex_x and obstacle not in self.passed_obstacles:
                self.passed_obstacles.add(obstacle)
                self.score += 1
                self.update_score_display()
                
                # Increase difficulty
                if self.score % 10 == 0:
                    self.game_speed += 0.5
        
        # Remove off-screen obstacles
        for obstacle in obstacles_to_remove:
            self.canvas.delete(obstacle)
            self.obstacles.remove(obstacle)
            if obstacle in self.passed_obstacles:
                self.passed_obstacles.remove(obstacle)
    
    def check_collision(self):
        """Check for collision between T-Rex and obstacles"""
        trex_coords = self.canvas.coords(self.trex)
        
        for obstacle in self.obstacles:
            obstacle_coords = self.canvas.coords(obstacle)
            
            # Check rectangle overlap
            if (trex_coords[0] < obstacle_coords[2] and
                trex_coords[2] > obstacle_coords[0] and
                trex_coords[1] < obstacle_coords[3] and
                trex_coords[3] > obstacle_coords[1]):
                
                self.end_game()
                return True
        
        return False
    
    def update_score_display(self):
        """Update the score display"""
        self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")
    
    def end_game(self):
        """End the game"""
        self.game_over = True
        
        # Update high score if needed
        if self.score > self.high_score:
            self.high_score = self.score
            self.set_high_score(self.high_score)
            self.canvas.itemconfig(self.high_score_text, text=f"High Score: {self.high_score}")
        
        # Display game over message
        self.canvas.create_text(
            400, 150,
            text="GAME OVER",
            font=("Arial", 48, "bold"),
            fill="red",
            tags="gameover"
        )
        self.canvas.create_text(
            400, 200,
            text=f"Final Score: {self.score}",
            font=("Arial", 24),
            fill="black",
            tags="gameover"
        )
        self.canvas.create_text(
            400, 240,
            text="Press 'R' to Restart",
            font=("Arial", 18),
            fill="blue",
            tags="gameover"
        )
    
    def restart_game(self, event=None):
        """Restart the game"""
        if self.game_over:
            # Remove game over message
            self.canvas.delete("gameover")
            
            # Clear obstacles
            for obstacle in self.obstacles:
                self.canvas.delete(obstacle)
            self.obstacles.clear()
            self.passed_obstacles.clear()
            
            # Reset game variables
            self.score = 0
            self.game_speed = 5
            self.is_jumping = False
            self.jump_velocity = 0
            self.game_over = False
            
            # Reset T-Rex position
            self.canvas.coords(
                self.trex,
                self.trex_x,
                self.trex_y,
                self.trex_x + self.trex_width,
                self.trex_y + self.trex_height
            )
            
            # Update score display
            self.update_score_display()
            
            # Restart game loop
            self.spawn_obstacle()
    
    def game_loop(self):
        """Main game loop"""
        if not self.game_over:
            self.update_jump()
            self.move_obstacles()
            self.check_collision()
            
            # Continue game loop
            self.window.after(20, self.game_loop)

# Start the game
if __name__ == "__main__":
    game = TRexGame()