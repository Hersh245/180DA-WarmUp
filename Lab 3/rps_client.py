import pygame
import paho.mqtt.client as mqtt
import sys

# Pygame Initialization
pygame.init()

# Screen Setup
size = (400, 300)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Rock Paper Scissors")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Fonts
font = pygame.font.Font(None, 36)

# MQTT Client Setup
broker_address = "test.mosquitto.org"
client_id = "player1"  # Change this for different clients
client = mqtt.Client(client_id)
client.connect(broker_address, 1883, 60)

# Global Variables
your_choice = ""
result = ""
waiting_for_result = False

# Define Buttons
button_rock = pygame.Rect(50, 200, 100, 50)
button_paper = pygame.Rect(150, 200, 100, 50)
button_scissors = pygame.Rect(250, 200, 100, 50)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(f"rps_game_result/{client_id}")


def on_message(client, userdata, msg):
    global result, waiting_for_result
    result = msg.payload.decode()
    waiting_for_result = False


client.on_connect = on_connect
client.on_message = on_message


def draw_buttons():
    pygame.draw.rect(screen, GREEN, button_rock)
    pygame.draw.rect(screen, RED, button_paper)
    pygame.draw.rect(screen, BLUE, button_scissors)

    rock_text = font.render("Rock", True, WHITE)
    paper_text = font.render("Paper", True, WHITE)
    scissors_text = font.render("Scissors", True, WHITE)

    screen.blit(rock_text, (60, 210))
    screen.blit(paper_text, (160, 210))
    screen.blit(scissors_text, (250, 210))


def display_player_info():
    player_text = font.render(f"Player ID: {client_id}", True, (0, 0, 0))
    screen.blit(player_text, (10, 10))
    if your_choice:
        choice_text = font.render(f"Your selection is: {your_choice}", True, (0, 0, 0))
        screen.blit(choice_text, (10, 50))


# Main Loop
running = True
client.loop_start()
while running:
    screen.fill(WHITE)
    draw_buttons()
    display_player_info()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not waiting_for_result:
            mouse_pos = event.pos
            if button_rock.collidepoint(mouse_pos):
                your_choice = "Rock"
                client.publish(f"rps_game/{client_id}", your_choice)
                waiting_for_result = True
            elif button_paper.collidepoint(mouse_pos):
                your_choice = "Paper"
                client.publish(f"rps_game/{client_id}", your_choice)
                waiting_for_result = True
            elif button_scissors.collidepoint(mouse_pos):
                your_choice = "Scissors"
                client.publish(f"rps_game/{client_id}", your_choice)
                waiting_for_result = True

    # Displaying results
    if result:
        result_text = font.render(result, True, (0, 0, 0))
        screen.blit(result_text, (100, 150))

    pygame.display.flip()

client.loop_stop()
pygame.quit()
sys.exit()
