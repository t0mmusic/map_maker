import pygame

pygame.init()
window = pygame.display.set_mode((250, 250))
clock = pygame.time.Clock()

sword = pygame.Surface((60, 100), pygame.SRCALPHA)
points = [(30, 0), (40, 10), (40, 70), (60, 75), (40, 80), (35, 80), (35, 100), 
          (25, 100), (25, 80), (20, 80), (0, 75), (20, 70), (20, 10)]
pygame.draw.polygon(sword, (255, 255, 0), points)
angle = 0

background = pygame.Surface(window.get_size())
ts, w, h, c1, c2 = 50, *background.get_size(), (128, 128, 128), (64, 64, 64)
tiles = [((x*ts, y*ts, ts, ts), c1 if (x+y) % 2 == 0 else c2) for x in range((w+ts-1)//ts) for y in range((h+ts-1)//ts)]
[pygame.draw.rect(background, color, rect) for rect, color in tiles] 

def blitRotate(surf, image, origin, pivot, angle):
    image_rect = image.get_rect(topleft = (origin[0] - pivot[0], origin[1]-pivot[1]))
    offset_center_to_pivot = pygame.math.Vector2(origin) - image_rect.center
    rotated_offset = offset_center_to_pivot.rotate(-angle)
    rotated_image_center = (origin[0] - rotated_offset.x, origin[1] - rotated_offset.y)
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)
    surf.blit(rotated_image, rotated_image_rect)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False 
        if event.type == pygame.MOUSEBUTTONDOWN:
            target = event.pos
        
    window.blit(background, (0, 0))
    blitRotate(window, sword, window.get_rect().center, (30, 75), angle)
    pygame.display.flip()
    clock.tick(100)
    angle += 1

pygame.quit()
exit()