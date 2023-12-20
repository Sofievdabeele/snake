import pygame, sys, random
from pygame.math import Vector2

class Snake:
    def __init__(self):
        self.body = [Vector2(4, 8), Vector2(3,8), Vector2(2,8)]
        self.direction = Vector2(1,0)
        self.new_block = False
        
        self.head_original = pygame.image.load('img/snake_head.png').convert_alpha()
        self.head = pygame.transform.scale(self.head_original, (cell_size, cell_size))
        self.head_down = pygame.transform.rotate(self.head, 0)
        self.head_right = pygame.transform.rotate(self.head, 90)
        self.head_up = pygame.transform.rotate(self.head, 180)
        self.head_left = pygame.transform.rotate(self.head, -90)

        self.point_sound = pygame.mixer.Sound('sound/jump.wav')
        self.game_over_sound = pygame.mixer.Sound('sound/game_over.wav')
    
    def draw_snake(self):
        self.position_head()
        
        for index,block in enumerate(self.body):
            x_pos = block.x * cell_size
            y_pos = block.y * cell_size
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            
            if index == 0:
                screen.blit(self.head,block_rect)
                
            else:
                pygame.draw.rect(screen, snake_color, block_rect)
                
    def position_head(self):
        head_to_body_relation = self.body[1] - self.body[0]
        if head_to_body_relation == Vector2(1,0): self.head = self.head_left
        if head_to_body_relation == Vector2(-1,0): self.head = self.head_right
        if head_to_body_relation == Vector2(0,1): self.head = self.head_up
        if head_to_body_relation == Vector2(0,-1): self.head = self.head_down
    
    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
    
    def add_block(self):
        self.new_block = True
 
    def play_point_sound(self):
        self.point_sound.play()
    
    def play_game_over_sound(self):
        self.game_over_sound.play()
    
    def reset(self):
        self.body = [Vector2(4, 8), Vector2(3,8), Vector2(2,8)]
        
class Fruit:
    def __init__(self):
        self.randomize()
        self.apple_original = pygame.image.load('img/apple.png').convert_alpha()
        self.apple = pygame.transform.scale(self.apple_original, (cell_size, cell_size))
        
    def draw_fruit(self):
        fruit_rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        #pygame.draw.rect(screen, red, fruit_rect, border_radius=30)   #(surface,color,rect)
        screen.blit(self.apple,fruit_rect)
    
    def randomize(self):
        self.x = random.randint(0,cell_nr - 1)
        self.y = random.randint(0,cell_nr - 1)
        self.pos = Vector2(self.x,self.y)

class Main:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()
        self.fruit_count = 0
        self.acceleration_counter = 0
    
    def update(self):
        self.snake.move_snake()
        self.check_on_top()
        self.check_die()
    
    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.text_surface()
        self.draw_score()
    
    def check_on_top(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_point_sound()
            self.fruit_count += 1
            self.acceleration_counter += 1
            
            if self.fruit_count % 5 == 0:
                pygame.time.set_timer(SCREEN_UPDATE, max(50, 300 - self.acceleration_counter * 10))

            key_states = pygame.key.get_pressed()
            if key_states[pygame.K_UP] and self.snake.direction.y != 1:
                self.snake.direction = Vector2(0, -1)
            elif key_states[pygame.K_DOWN] and self.snake.direction.y != -1:
                self.snake.direction = Vector2(0, 1)
            elif key_states[pygame.K_RIGHT] and self.snake.direction.x != -1:
                self.snake.direction = Vector2(1, 0)
            elif key_states[pygame.K_LEFT] and self.snake.direction.x != 1:
                self.snake.direction = Vector2(-1, 0)
                
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()
     
    def paused(self):
        paused = True
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        paused = False

            pauze_text = game_font_l.render("PAUSE", True, black)
            pauze_rect = pauze_text.get_rect(center=(game_cells / 2, game_cells / 2))
            screen.blit(pauze_text, pauze_rect)
            pygame.display.update()
 
            
    def check_die(self):
        if not 0 <= self.snake.body[0].x < cell_nr or not 0 <= self.snake.body[0].y < cell_nr:
            self.game_over()
        
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()
            
    def game_over(self):
        self.snake.play_game_over_sound()
        self.game_over_message()
        pygame.display.update()
        
        waiting_for_key = True
        while waiting_for_key:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.snake.reset()
                    waiting_for_key = False
                    self.acceleration_counter = 0
        
    def game_over_message(self):
        game_over_text = game_font.render("Game Over!", True, (0, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(game_cells / 2, game_cells / 2))
        screen.blit(game_over_text, game_over_rect)
        
    def draw_grass(self):
        grass_color = (142,170,139)
        
        for row in range(cell_nr):
            if row % 2 == 0:
                for col in range(cell_nr):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_nr):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)            

    def text_surface(self):
        text_surface = pygame.Surface((game_cells,100))
        text_surface.fill(black)
        
        play_text = game_font_s.render("Press ARROWS to play", True, white)
        play_text_rect = play_text.get_rect(topleft=(30, 20))
        
        pause_text = game_font_s.render("Press SPACE to Pause", True, white)
        pause_text_rect = pause_text.get_rect(topleft=(30, 40))
        
        unpause_text = game_font_s.render("Press SPACE x 2 to Continue", True, white)
        unpause_text_rect = unpause_text.get_rect(topleft=(30, 60))
    
        text_surface.blit(play_text, play_text_rect)
        text_surface.blit(pause_text, pause_text_rect)
        text_surface.blit(unpause_text, unpause_text_rect)
        
        screen.blit(text_surface,(0,game_cells))
        return text_surface
        
    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, (white))
        score_x = game_cells - score_surface.get_width() - 20
        score_y = game_cells + ((100 - score_surface.get_height() )/ 2)
      
        screen.blit(score_surface, (score_x, score_y))
        
pygame.init()

green = (142,174,139)
snake_color = (100, 156, 73)
red = (226,84,1)
black = (0,0,0)
white = (255,255,255)

cell_size = 20
cell_nr = 20
game_cells = cell_size * cell_nr

screen = pygame.display.set_mode((game_cells,game_cells + 100))
pygame.display.set_caption("SNAKE")

game_icon = pygame.image.load("img/snake.png")
pygame.display.set_icon(game_icon)
clock = pygame.time.Clock()
game_font = pygame.font.Font('KILOTON3.TTF', 50)
game_font_l = pygame.font.Font('KILOTON3.TTF', 80)
game_font_s = pygame.font.Font('KILOTON3.TTF', 10)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 300)

main_game = Main()

running = True
paused = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if not paused:
            if event.type == SCREEN_UPDATE:
                main_game.update()

            if event.type == pygame.KEYDOWN:
                if not main_game.snake.new_block:
                    if event.key == pygame.K_UP:
                        if main_game.snake.direction.y != 1:
                            main_game.snake.direction = Vector2(0,-1)
            
                    if event.key == pygame.K_DOWN:
                        if main_game.snake.direction.y != -1:
                            main_game.snake.direction = Vector2(0,1)
                
                    if event.key == pygame.K_RIGHT:
                        if main_game.snake.direction.x != -1:
                            main_game.snake.direction = Vector2(1,0)
            
                    if event.key == pygame.K_LEFT:
                        if main_game.snake.direction.x != 1:
                            main_game.snake.direction = Vector2(-1,0)    
                    
                    if event.key == pygame.K_SPACE:
                        paused = True
                        main_game.paused()
        else: 
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                paused = False
        
    screen.fill(green)
    
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)
        