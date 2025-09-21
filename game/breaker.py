import pygame

unique_counter = 1000000

def handle_break_place(event, blocks, mouse_pos):
    global unique_counter
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 3:  # Right click - break block
            for block in blocks:
                rect = pygame.Rect(block['x'], block['y'], block['size'], block['size'])
                if rect.collidepoint(mouse_pos):
                    blocks.remove(block)
                    break
        if event.button == 1:  # Left click - place block
            blocks.append({'id': f'block_{unique_counter}', 'x': mouse_pos[0]//20*20, 'y': mouse_pos[1]//20*20, 'size': 20})
            unique_counter += 1
