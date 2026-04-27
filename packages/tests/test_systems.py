import pygame
import numpy as np

pygame.init()

W, H = 1000, 1000
screen = pygame.display.set_mode((W, H))

# ma trận random
matrix = np.random.randint(0, 4, (H, W), dtype=np.uint8)

# bảng màu (lookup table)
table = np.array([
    [0, 0, 0],        # 0: đen
    [255, 0, 0],      # 1: đỏ
    [0, 255, 0],      # 2: xanh lá
    [0, 0, 255]       # 3: xanh dương
], dtype=np.uint8)

# 🔥 vectorized mapping (KHÔNG loop Python)
rgb_array = table[matrix]   # shape: (H, W, 3)

# tạo surface từ buffer
surface = pygame.surfarray.make_surface(rgb_array.swapaxes(0, 1))

# loop render
running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    screen.blit(surface, (0, 0))
    pygame.display.flip()

pygame.quit()