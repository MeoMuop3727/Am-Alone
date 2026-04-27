import pygame, sys

def exit_game() -> None:
    pygame.quit()
    sys.exit()

class Scene:
    def __init__(self):
        self.manager = None

    # --- Public API ---
    def handle_events(self, events):
        pass

    def update(self, dt):
        pass

    def render(self, screen):
        pass

    def on_enter(self):
        pass

    def on_exit(self):
        pass
        
class ScenceManager:
    def __init__(self, surface: pygame.Surface):
        self._screen = surface

        self._scences: list[Scene] = []
        self._running = True
        self._clock = pygame.time.Clock()
    
    # --- Public API ---
    def push_scence(self, scence: Scene) -> None:
        scence.manager = self
        self._scences.append(scence)
        scence.on_enter()
    
    def pop_scence(self) -> None:
        if self._scences:
            scence = self._scences.pop()
            scence.on_exit()
    
    def replace_scence(self, scence: Scene) -> None:
        self.pop_scence()
        self.push_scence(scence)
    
    def get_current_scence(self) -> Scene:
        return self._scences[-1] if self._scences else None
    
    def run(self, fps: int = 60) -> None:
        while self._running:
            dt = self._clock.tick(fps) / 1e3

            events = pygame.event.get()

            current_scence = self.get_current_scence()

            for event in events:
                if event.type == pygame.QUIT:
                    exit_game()
            
            if not current_scence: continue

            current_scence.handle_events(events)
            current_scence.update(dt)
            current_scence.render(self._screen)

            pygame.display.flip()
            