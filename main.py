import os
import sys

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame

from state_manager import should_show_welcome, mark_welcome_as_seen

# Initialize Pygame Video and Audio
pygame.init()
try:
    pygame.mixer.init()
except pygame.error as e:
    print("Audio initialization failed! ", e)
    sys.exit(1)

# --- CONFIGURATION & COLORS ---
WIDTH, HEIGHT = 600, 450
DIRT_COLOR = (134, 96, 67)
GRASS_COLOR = (89, 152, 47)
STONE_BASE = (125, 125, 125)
STONE_LIGHT = (170, 170, 170)
STONE_DARK = (88, 88, 88)
TEXT_COLOR = (255, 255, 255)
TEXT_SHADOW = (63, 63, 63)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Craft Listen")
clock = pygame.time.Clock()

# Use default Pygame font to avoid macOS font-loading crashes
font = pygame.font.Font(None, 24)
large_font = pygame.font.Font(None, 32)

def draw_text(surface, text, x, y, use_large=False):
    # False for anti-aliasing gives that crisp "pixelated" look
    fnt = large_font if use_large else font
    # Shadow
    shadow_surf = fnt.render(text, False, TEXT_SHADOW)
    surface.blit(shadow_surf, (x + 2, y + 2))
    # Text
    text_surf = fnt.render(text, False, TEXT_COLOR)
    surface.blit(text_surf, (x, y))

def draw_button(surface, rect, text, is_pressed=False):
    # Minecraft-style 3D button
    pygame.draw.rect(surface, STONE_BASE, rect)

    # Borders to make it look pop-out or pressed
    top_color = STONE_DARK if is_pressed else STONE_LIGHT
    bottom_color = STONE_LIGHT if is_pressed else STONE_DARK

    # Top and Left borders
    pygame.draw.line(surface, top_color, rect.topleft, rect.topright, 3)
    pygame.draw.line(surface, top_color, rect.topleft, rect.bottomleft, 3)
    # Bottom and Right borders
    pygame.draw.line(surface, bottom_color, rect.bottomleft, rect.bottomright, 3)
    pygame.draw.line(surface, bottom_color, rect.topright, rect.bottomright, 3)

    # Center text
    fnt = font
    txt_surf = fnt.render(text, False, TEXT_COLOR)
    txt_rect = txt_surf.get_rect(center=rect.center)

    # Offset text if pressed
    if is_pressed:
        txt_rect.x += 2
        txt_rect.y += 2

    # Draw shadow then text inside button
    shadow_surf = fnt.render(text, False, TEXT_SHADOW)
    surface.blit(shadow_surf, (txt_rect.x + 2, txt_rect.y + 2))
    surface.blit(txt_surf, txt_rect)

def draw_welcome_overlay(surface, mouse_pos, mouse_pressed):
    """Draw welcome message overlay with instructions."""
    # Semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))
    surface.blit(overlay, (0, 0))

    # Welcome box
    box_width, box_height = 500, 320
    box_x = (WIDTH - box_width) // 2
    box_y = (HEIGHT - box_height) // 2
    box_rect = pygame.Rect(box_x, box_y, box_width, box_height)

    # Draw box with minecraft-style border
    pygame.draw.rect(surface, DIRT_COLOR, box_rect)
    pygame.draw.rect(surface, STONE_LIGHT, box_rect, 4)

    # Welcome title
    title_y = box_y + 20
    draw_text(surface, "Welcome to Craft Listen!", box_x + 80, title_y, use_large=True)

    # Instructions
    instructions = [
        "A simple audio player with a Minecraft-style UI!",
        "",
        "Getting Started:",
        "1. Place your .mp3 files in the 'music' folder",
        "2. Use Previous/Next to navigate tracks",
        "3. Use Play to start, Pause to pause playback",
        "4. Use Stop to stop and reset the current track",
        "",
        "Perfect for sequential listening and study sessions!"
    ]

    text_y = title_y + 50
    for line in instructions:
        draw_text(surface, line, box_x + 30, text_y)
        text_y += 25

    # OK button
    btn_ok = pygame.Rect(box_x + 180, box_y + box_height - 60, 140, 40)
    draw_button(surface, btn_ok, "Let's Go!", is_pressed=(btn_ok.collidepoint(mouse_pos) and mouse_pressed))

    return btn_ok


def main():
    folder = "music"
    if not os.path.isdir(folder):
        os.makedirs(folder)

    mp3_files = sorted([f for f in os.listdir(folder) if f.endswith(".mp3")])
    current_index = 0
    is_playing = False

    if mp3_files:
        pygame.mixer.music.load(os.path.join(folder, mp3_files[current_index]))

    # Welcome message state
    show_welcome = should_show_welcome()

    # Define Button Rectangles
    btn_prev = pygame.Rect(50, 350, 100, 40)
    btn_play = pygame.Rect(170, 350, 120, 40)
    btn_stop = pygame.Rect(310, 350, 100, 40)
    btn_next = pygame.Rect(430, 350, 100, 40)

    running = True
    mouse_was_pressed = False
    
    while running:
        screen.fill(DIRT_COLOR)
        
        # Draw "Grass" header
        pygame.draw.rect(screen, GRASS_COLOR, (0, 0, WIDTH, 80))
        pygame.draw.rect(screen, (60, 110, 30), (0, 80, WIDTH, 10)) # Shadow line under grass
        
        draw_text(screen, "Craft Listen", 20, 25, use_large=True)

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        click_event = False
        
        # Handle Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click_event = True

        # Draw current track info
        if not mp3_files:
            draw_text(screen, "No .mp3 files found in 'music/' folder!", 30, 150)
        else:
            status = "Playing" if is_playing else "Paused / Stopped"
            draw_text(screen, f"Status: {status}", 30, 130)
            
            # Wrap track name if too long
            track_name = mp3_files[current_index]
            draw_text(screen, "Current Track:", 30, 180)
            draw_text(screen, track_name[:40] + ("..." if len(track_name)>40 else ""), 30, 210, use_large=True)
            
            draw_text(screen, f"Track {current_index + 1} of {len(mp3_files)}", 30, 270)

            # Button Interactions
            if click_event:
                if btn_play.collidepoint(mouse_pos):
                    if is_playing:
                        pygame.mixer.music.pause()
                        is_playing = False
                    else:
                        if not pygame.mixer.music.get_busy():
                            pygame.mixer.music.play()
                        else:
                            pygame.mixer.music.unpause()
                        is_playing = True

                elif btn_stop.collidepoint(mouse_pos):
                    pygame.mixer.music.stop()
                    is_playing = False

                elif btn_next.collidepoint(mouse_pos):
                    current_index = (current_index + 1) % len(mp3_files)
                    pygame.mixer.music.load(os.path.join(folder, mp3_files[current_index]))
                    pygame.mixer.music.play()
                    is_playing = True

                elif btn_prev.collidepoint(mouse_pos):
                    current_index = (current_index - 1) % len(mp3_files)
                    pygame.mixer.music.load(os.path.join(folder, mp3_files[current_index]))
                    pygame.mixer.music.play()
                    is_playing = True

        # Draw Buttons
        draw_button(screen, btn_prev, "<< Prev", is_pressed=(btn_prev.collidepoint(mouse_pos) and mouse_pressed))
        play_text = "Pause" if is_playing else "Play"
        draw_button(screen, btn_play, play_text, is_pressed=(btn_play.collidepoint(mouse_pos) and mouse_pressed))
        draw_button(screen, btn_stop, "Stop", is_pressed=(btn_stop.collidepoint(mouse_pos) and mouse_pressed))
        draw_button(screen, btn_next, "Next >>", is_pressed=(btn_next.collidepoint(mouse_pos) and mouse_pressed))

        # Draw welcome overlay if it should be shown
        if show_welcome:
            btn_ok = draw_welcome_overlay(screen, mouse_pos, mouse_pressed)
            if click_event and btn_ok.collidepoint(mouse_pos):
                show_welcome = False
                mark_welcome_as_seen()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()