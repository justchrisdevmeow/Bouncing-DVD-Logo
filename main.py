import pygame
import sys
import os
from tkinter import filedialog, Tk, Button, Label, Entry, Scale, HORIZONTAL
import tkinter as tk

# Initialize Pygame
pygame.init()

# Settings
settings = {
    'logo_path': '',
    'speed': 3,
    'fullscreen': True,
    'logo_scale': 1.0,
    'trail': False,
    'color_change': True
}

def load_logo():
    """Load logo from file, resize it"""
    try:
        if settings['logo_path'] and os.path.exists(settings['logo_path']):
            img = pygame.image.load(settings['logo_path'])
        else:
            # Create a fallback logo (colored rectangle with text)
            surf = pygame.Surface((200, 100), pygame.SRCALPHA)
            surf.fill((255, 100, 100))
            font = pygame.font.Font(None, 30)
            text = font.render("DVD Logo", True, (255,255,255))
            surf.blit(text, (50, 35))
            return surf.convert_alpha()
        
        if settings['logo_scale'] != 1.0:
            size = img.get_size()
            new_size = (int(size[0] * settings['logo_scale']), int(size[1] * settings['logo_scale']))
            img = pygame.transform.scale(img, new_size)
        return img.convert_alpha()
    except Exception as e:
        print(f"Error loading logo: {e}")
        surf = pygame.Surface((200, 100), pygame.SRCALPHA)
        surf.fill((255, 100, 100))
        font = pygame.font.Font(None, 30)
        text = font.render("DVD Logo", True, (255,255,255))
        surf.blit(text, (50, 35))
        return surf.convert_alpha()

def save_settings():
    """Save settings to file"""
    with open('dvd_settings.txt', 'w') as f:
        for key, value in settings.items():
            f.write(f"{key}:{value}\n")

def load_settings_file():
    """Load settings from file"""
    global settings
    try:
        with open('dvd_settings.txt', 'r') as f:
            for line in f:
                if ':' in line:
                    key, value = line.strip().split(':', 1)
                    if key in settings:
                        if key == 'logo_path':
                            settings[key] = value
                        elif key in ['speed', 'logo_scale']:
                            try:
                                settings[key] = float(value)
                            except:
                                pass
                        elif key in ['fullscreen', 'trail', 'color_change']:
                            settings[key] = value.lower() == 'true'
                        else:
                            settings[key] = value
    except:
        pass

def open_settings():
    """Open tkinter settings window"""
    root = tk.Tk()
    root.title("DVD Logo Settings")
    root.geometry("400x500")
    
    # Logo path
    Label(root, text="Logo Path:").pack(pady=(10,0))
    logo_entry = Entry(root, width=40)
    logo_entry.insert(0, settings['logo_path'])
    logo_entry.pack(pady=5)
    
    def browse_logo():
        filename = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")])
        if filename:
            logo_entry.delete(0, tk.END)
            logo_entry.insert(0, filename)
    
    Button(root, text="Browse", command=browse_logo).pack(pady=5)
    
    # Speed
    Label(root, text="Speed:").pack(pady=(10,0))
    speed_scale = Scale(root, from_=1, to=10, orient=HORIZONTAL)
    speed_scale.set(settings['speed'])
    speed_scale.pack()
    
    # Logo scale
    Label(root, text="Logo Scale:").pack(pady=(10,0))
    scale_scale = Scale(root, from_=0.1, to=2.0, resolution=0.05, orient=HORIZONTAL)
    scale_scale.set(settings['logo_scale'])
    scale_scale.pack()
    
    # Fullscreen toggle
    fullscreen_var = tk.BooleanVar(value=settings['fullscreen'])
    tk.Checkbutton(root, text="Fullscreen", variable=fullscreen_var).pack(pady=5)
    
    # Trail effect
    trail_var = tk.BooleanVar(value=settings['trail'])
    tk.Checkbutton(root, text="Trail Effect", variable=trail_var).pack(pady=5)
    
    # Color change on bounce
    color_var = tk.BooleanVar(value=settings['color_change'])
    tk.Checkbutton(root, text="Color Change on Bounce", variable=color_var).pack(pady=5)
    
    def save_and_exit():
        settings['logo_path'] = logo_entry.get()
        settings['speed'] = speed_scale.get()
        settings['logo_scale'] = scale_scale.get()
        settings['fullscreen'] = fullscreen_var.get()
        settings['trail'] = trail_var.get()
        settings['color_change'] = color_var.get()
        save_settings()
        root.quit()
        root.destroy()
        return  # Signal to restart
    
    Button(root, text="Save and Restart", command=save_and_exit, bg='green', fg='white').pack(pady=20)
    root.mainloop()

def main():
    load_settings_file()
    
    # Setup display
    try:
        if settings['fullscreen']:
            screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode((800, 600))
    except Exception as e:
        print(f"Display error: {e}")
        screen = pygame.display.set_mode((800, 600))
    
    screen_width, screen_height = screen.get_size()
    pygame.display.set_caption("DVD Logo Screensaver")
    
    # Load logo
    logo = load_logo()
    logo_width, logo_height = logo.get_size()
    
    # Starting position (center)
    x = (screen_width - logo_width) // 2
    y = (screen_height - logo_height) // 2
    dx = settings['speed']
    dy = settings['speed']
    
    # Color tint (default white)
    tint_color = (255, 255, 255)
    colors = [(255,0,0), (0,255,0), (0,0,255), (255,255,0), (255,0,255), (0,255,255)]
    tint_index = 0
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_s:
                    open_settings()
                    return  # Restart after settings
            elif event.type == pygame.MOUSEBUTTONDOWN:
                open_settings()
                return
        
        # Move logo
        x += dx
        y += dy
        
        # Bounce off walls
        bounced = False
        if x <= 0 or x + logo_width >= screen_width:
            dx = -dx
            bounced = True
            x = max(0, min(x, screen_width - logo_width))
        if y <= 0 or y + logo_height >= screen_height:
            dy = -dy
            bounced = True
            y = max(0, min(y, screen_height - logo_height))
        
        # Rotate tint color on bounce
        if bounced and settings['color_change']:
            tint_index = (tint_index + 1) % len(colors)
            tint_color = colors[tint_index]
        
        # Apply tint to logo
        tinted_logo = logo.copy()
        tint_surf = pygame.Surface(logo.get_size(), pygame.SRCALPHA)
        tint_surf.fill(tint_color)
        tinted_logo.blit(tint_surf, (0,0), special_flags=pygame.BLEND_RGB_MULT)
        
        # Clear screen
        if settings['trail']:
            screen.fill((0,0,0, 30), special_flags=pygame.BLEND_RGBA_MULT)
        else:
            screen.fill((0,0,0))
        
        # Draw logo
        screen.blit(tinted_logo, (int(x), int(y)))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
