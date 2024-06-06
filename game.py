import pygame

class CountdownTimer:
    def __init__(self, duration, callback):
        self.counter = duration
        self.callback = callback
        self.font = pygame.font.SysFont(None, 100)
        self.text = self.font.render(str(self.counter), True, (0, 128, 0))
        pygame.time.set_timer(pygame.USEREVENT, 1000)

    def update(self, event):
        if event.type == pygame.USEREVENT:
            self.counter -= 1
            self.text = self.font.render(str(self.counter), True, (0, 128, 0))
            if self.counter <= 0:
                pygame.time.set_timer(pygame.USEREVENT, 0)
                self.callback()

    def draw(self, window):
        window.blit(self.text, self.text.get_rect(center=window.get_rect().center))

def game_over():
    print("Game Over!")
    pygame.quit()
    exit()

if __name__ == "__main__":
    pygame.init()
    window = pygame.display.set_mode((400, 300))
    clock = pygame.time.Clock()
    
    timer = CountdownTimer(30, game_over)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            timer.update(event)

        window.fill((255, 255, 255))
        timer.draw(window)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
