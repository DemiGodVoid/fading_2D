import pygame

class Player:
    def __init__(self, stand_img, walk_img, x, ground):
        self.images = [pygame.transform.scale(stand_img,(50,50)),
                       pygame.transform.scale(walk_img,(50,50))]
        self.rect = self.images[0].get_rect(midbottom=(x, ground.rect.top))
        self.speed = 5
        self.anim_idx = 0
        self.anim_timer = 0
        self.ground = ground

    def move(self, keys):
        moving = False
        if keys[pygame.K_a] and self.rect.left > self.ground.rect.left:
            self.rect.x -= self.speed; moving=True
        if keys[pygame.K_d] and self.rect.right < self.ground.rect.right:
            self.rect.x += self.speed; moving=True
        if moving:
            self.anim_timer += 1
            if self.anim_timer % 10 == 0:
                self.anim_idx = (self.anim_idx + 1) % len(self.images)
        else:
            self.anim_idx = 0
        self.rect.bottom = self.ground.rect.top

    def draw(self, win):
        win.blit(self.images[self.anim_idx], self.rect)
