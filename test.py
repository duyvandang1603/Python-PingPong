import pygame, sys, random
# -*- coding: utf-8 -*-


screen_width = 1300
screen_height = 800
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 48, 48)

restart_flag = False

# Kích thước các vật thể
ball = pygame.Rect(0,0,30,30)
ball.center = (screen_width/2, screen_height/2)

cpu = pygame.Rect(0,0,20,100)
cpu.midleft = (0, screen_height/2)

player1 = pygame.Rect(0,0,20,100)
player1.midright = (screen_width, screen_height/2)

player2 = pygame.Rect(0,0,20,100)
player2.midleft = (0, screen_height/2)

# Tốc độ di chuyển các vật thể
ball_speed_x = 7
ball_speed_y = 7
player1_speed_x = 0
player1_speed_y = 0
player2_speed_x = 0
player2_speed_y = 0
cpu_speed_x = 6
cpu_speed_y = 6
cpu_points, player1_points, player2_points = 0, 0, 0

screen_menu = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("My Pong Game!")

# Hàm reset ball
def reset_ball():
    global ball_speed_x, ball_speed_y
    ball.x = screen_width/2 - 10
    ball.y = random.randint(10,100)
    ball_speed_x *= random.choice([-1,1])
    ball_speed_y *= random.choice([-1,1])

# Hàm tính điểm
def point_won(winner):
    global cpu_points, player1_points, player2_points

    if winner == "cpu":
        cpu_points += 1
    if winner == "player1":
        player1_points += 1
    if winner == "player2":
        player2_points += 1

    reset_ball()

# Hàm di chuyển của banh
def animate_ball():
    global ball_speed_x, ball_speed_y, collision_occurred
    ball.x += ball_speed_x
    ball.y += ball_speed_y
    
    if ball.bottom >= screen_height or ball.top <= 0:
        ball_speed_y *= -1

    if ball.right >= screen_width:
        point_won("cpu")
        point_won('player2')

    if ball.left <= 0:
        point_won("player1")
        
    if ball.colliderect(player1) or ball.colliderect(cpu) or ball.colliderect(player2):
    # Chỉ xử lý va chạm nếu collision_occurred là False
        if not collision_occurred:
            ball_speed_x *= -1

        # Đặt collision_occurred thành True để chỉ xử lý một lần va chạm
            collision_occurred = True
    else:
    # Nếu không có va chạm xảy ra, đặt lại collision_occurred thành False để cho phép xử lý va chạm tiếp theo
        collision_occurred = False

# Hàm di chuyển của player
def animate_player():
    player1.y += player1_speed_y
    player1.x += player1_speed_x

    if player1.top <= 0:
        player1.top = 0

    if player1.bottom >= screen_height:
        player1.bottom = screen_height
        
    if player1.left <= screen_width/2:
        player1.left = screen_width/2
    
    if player1.right >= screen_width:
        player1.right = screen_width   
        
    player2.y += player2_speed_y
    player2.x += player2_speed_x

    if player2.top <= 0:
        player2.top = 0

    if player2.bottom >= screen_height:
        player2.bottom = screen_height  
        
    if player2.left <= 0:
        player2.left = 0
    if player2.right >= screen_width/2:
        player2.right = screen_width/2
           
# Hàm di chuyển của CPU
def animate_cpu():
    global cpu_speed_x, cpu_speed_y
    cpu.y += cpu_speed_y
    cpu.x += cpu_speed_x
    
    if ball.centery <= cpu.centery:
        cpu_speed_y = -6
    if ball.centery >= cpu.centery:
        cpu_speed_y = 6
    if ball.centerx < cpu.centerx:
        cpu_speed_x = -6  # Di chuyển sang trái nếu ball ở bên trái cpu
    elif ball.centerx > cpu.centerx:
        cpu_speed_x = 6  # Di chuyển sang phải nếu ball ở bên phải cpu

        # Kiểm tra va chạm giữa CPU và bóng, nếu có thì di chuyển CPU ra khỏi bóng
    if cpu.colliderect(ball):
        if cpu.right >= ball.left and cpu.left < ball.left:
            cpu.right = ball.left
        elif cpu.left <= ball.right and cpu.right > ball.right:
            cpu.left = ball.right

    if cpu.top <= 0:
        cpu.top = 0
    if cpu.bottom >= screen_height:
        cpu.bottom = screen_height
    if cpu.left <= 0:
        cpu.left = 0
    if cpu.right >= screen_width/2:
        cpu.right = screen_width/2 
        
# Hàm menu
def show_menu():
        # Thêm dòng "Ping Pong Game" làm tựa đề
    ping_pong_title_font = pygame.font.Font(None, 80)
    ping_pong_title_text = ping_pong_title_font.render("Ping Pong Game", True, (255, 255, 255))
    ping_pong_title_text_rect = ping_pong_title_text.get_rect(center=(screen_width / 2, 100))
    
    
    # Thành viên thực hiện
    contributors_font = pygame.font.Font(None, 20)
    contributor_text_1 = contributors_font.render(u"Thành viên thực hiện:", True, WHITE)
    contributor_text_2 = contributors_font.render(u"Đặng Duy Văn - 3120410603", True, WHITE)
    contributor_text_3 = contributors_font.render(u"Tạ Hà Anh Tú - 3120410579", True, WHITE)

 
    
    menu_font = pygame.font.Font(None, 50)
    menu_options = ["Play with CPU", "Play with Player", "Quit"]
    selected_option = 0

    while True:
        screen.fill('black')
        screen.blit(ping_pong_title_text, ping_pong_title_text_rect)

        screen.blit(contributor_text_1, (30, screen_height - 100))
        screen.blit(contributor_text_2, (30, screen_height - 70))
        screen.blit(contributor_text_3, (30, screen_height - 40))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                if event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        return "cpu"
                    elif selected_option == 1:
                        return "player"
                    elif selected_option == 2:
                        sys.exit()

        for i, option in enumerate(menu_options):
            if i == selected_option:
                text_surface = menu_font.render(option, True,RED)
            else:
                text_surface = menu_font.render(option,True,WHITE)
            text_rect = text_surface.get_rect(center = (screen_width // 2, (screen_height // 2) + i * 50))
            screen.blit(text_surface, text_rect)
        pygame.display.update()
        clock.tick(60)

# Hàm hiển thị điểm
def show_point():
    
    player1_score_surface = score_font.render(str(player1_points), True, "white")
    screen.blit(player1_score_surface,(3*screen_width/4,20))

    if game_mode == 'cpu':
        cpu_score_surface = score_font.render(str(cpu_points), True, "white")
        screen.blit(cpu_score_surface,(screen_width/4,20))

    elif game_mode == 'player':
        player2_score_surface = score_font.render(str(player2_points), True, "white")
        screen.blit(player2_score_surface,(screen_width/4,20))
          
# Hàm gameover
def game_over():
    global game_over_flag
    if player1_points == 3:
        winner_text = score_font.render("Player 1 wins!", True, "white")
        screen.blit(winner_text, (screen_width / 2 - 200, screen_height / 2))
        pygame.display.update()
        pygame.time.wait(2000)  # Chờ 2 giây trước khi thoát
        show_menu()
        start_new_game()
        game_over_flag=True
        
    elif game_mode == 'player':
        if player2_points == 3:
            winner_text = score_font.render("Player 2 wins!", True, "white")
            screen.blit(winner_text, (screen_width / 2 - 200, screen_height / 2))
            pygame.display.update()
            pygame.time.wait(2000)  # Chờ 2 giây trước khi thoát
            show_menu()
            start_new_game()
            game_over_flag=True

    elif game_mode == 'cpu': 
        if cpu_points == 3:
            winner_text = score_font.render("CPU wins!", True, "white")
            screen.blit(winner_text, (screen_width / 2 - 100, screen_height / 2))
            pygame.display.update()
            pygame.time.wait(2000)  # Chờ 2 giây trước khi thoát
            show_menu()
            start_new_game()
            game_over_flag=True
               
# Hàm menu pause 
def pause_menu():
    pause_options = ["Continue", "Restart", "Exit to menu"]
    selected_item = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:  # Di chuyển con trỏ lên
                    selected_item = (selected_item - 1) % len(pause_options)
                elif event.key == pygame.K_DOWN:  # Di chuyển con trỏ xuống
                    selected_item = (selected_item + 1) % len(pause_options)
                elif event.key == pygame.K_RETURN:  # Chọn tùy chọn
                    if selected_item == 0:
                        return "continue"
                    elif selected_item == 1:
                        start_new_game()
                        return "restart"
                    elif selected_item == 2:
                        start_new_game()
                        return "new_game"
        
        screen.fill(BLACK)
        
        # Vẽ các nút trên thanh menu
        font = pygame.font.SysFont(None, 50)
        
        for i, item in enumerate(pause_options):
            if i == selected_item:
                text_surface = font.render(item, True, RED)
            else:
                text_surface = font.render(item, True, WHITE)  
            text_rect = text_surface.get_rect(center=(screen_width // 2, (screen_height // 2) + i * 50))
            screen.blit(text_surface, text_rect)

        pygame.display.flip()
        clock.tick(30)

# Hàm pause game
def pause_game():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False
                    return "continue"
            elif event.type == pygame.QUIT:  # Xử lý sự kiện tắt của hệ thống
                pygame.quit()
                sys.exit()
        
        action = pause_menu()
        if action == "continue":
            paused = False
        elif action == "restart":
            start_new_game()
            return "restart"
        elif action == "new_game":
            start_new_game()
            return "new_game"

# Hàm bắt đầu game mới
def start_new_game():
    global game_over_flag, player1_points, player2_points, cpu_points, game_mode
    game_mode = show_menu()

    game_over_flag = False
    player1_points = 0
    player2_points = 0
    cpu_points = 0

    ball.center = (screen_width/2, screen_height/2)
    cpu.midleft = (0, screen_height/2)

    player1.midright = (screen_width, screen_height/2)
    player2.midleft = (0, screen_height/2)

pygame.init()

clock = pygame.time.Clock()
score_font = pygame.font.Font(None, 100)

game_mode = show_menu()  # Show the menu and get the selected game mode
# Vòng lặp chính của trò chơi
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                action = pause_game()
                if action == "restart":
                    start_new_game()
                if action == "new_game":
                    show_menu()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player1_speed_y = -6
            if event.key == pygame.K_DOWN:
                player1_speed_y = 6 
            if event.key == pygame.K_LEFT:
                player1_speed_x = -6    
            if event.key == pygame.K_RIGHT:
                player1_speed_x = 6 

            
            if event.key == pygame.K_w:
                player2_speed_y = -6
            if event.key == pygame.K_s:
                player2_speed_y = 6
            if event.key == pygame.K_a:
                player2_speed_x = -6    
            if event.key == pygame.K_d:
                player2_speed_x = 6                 

                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player1_speed_y = 0
            if event.key == pygame.K_DOWN:
                player1_speed_y = 0
            if event.key == pygame.K_LEFT:
                player1_speed_x = 0    
            if event.key == pygame.K_RIGHT:
                player1_speed_x = 0 
                
                
            if event.key == pygame.K_w:
                player2_speed_y = 0
            if event.key == pygame.K_s:
                player2_speed_y = 0
            if event.key == pygame.K_a:
                player2_speed_x = 0    
            if event.key == pygame.K_d:
                player2_speed_x = 0                 


                
    screen.fill('#006600')        

    animate_ball()
    animate_player()
    
    if game_mode == "cpu":
        animate_cpu()
                    
    show_point()    
    game_over()
    
    
    paddle_image_right = pygame.image.load('paddle-right.png')
    paddle_image_left = pygame.image.load('paddle-left.png')

# Thay thế pygame.draw.rect() bằng screen.blit() để vẽ hình ảnh lên màn hình
    screen.blit(paddle_image_right, player1) 


    pygame.draw.aaline(screen,'white',(screen_width/2, 0), (screen_width/2, screen_height))
    pygame.draw.ellipse(screen,'white',ball)
    #pygame.draw.rect(screen,'white',player1)
    #screen.blit(player1, (player1, player1))

    if game_mode == 'cpu':
        screen.blit(paddle_image_left, cpu) 
    elif game_mode == 'player':
        screen.blit(paddle_image_left, player2) 

    pygame.display.update()
    clock.tick(60)
