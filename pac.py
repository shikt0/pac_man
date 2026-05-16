import pygame
import sys
import math
from collections import deque
import random

TILE_SIZE = 40
GRID_WIDTH = 19
GRID_HEIGHT = 21
HUD_HEIGHT = 72
SCREEN_WIDTH = GRID_WIDTH * TILE_SIZE
SCREEN_HEIGHT = HUD_HEIGHT + GRID_HEIGHT * TILE_SIZE
FPS = 60
PACMAN_MOVE_MS = 135
GHOST_MOVE_MS = 175
MIN_PACMAN_MOVE_MS = 80
MIN_GHOST_MOVE_MS = 105
FRIGHTENED_MS = 6500
READY_MS = 1200
SCATTER_MS = 7000
CHASE_MS = 18000
LEVEL_BONUS = 500
CAUGHT_ANIMATION_MS = 1500
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 221, 51)
GOLD = (255, 190, 44)
RED = (239, 68, 68)
PINK = (255, 137, 216)
CYAN = (34, 211, 238)
BLUE = (37, 99, 235)
DEEP_BLUE = (12, 28, 84)
ORANGE = (251, 146, 60)
WALL_EDGE = (96, 165, 250)
WALL_FILL = (24, 64, 165)
WALL_HOT = (125, 211, 252)
WALL_SHADOW = (6, 17, 50)
BG_TOP = (5, 8, 22)
BG_BOTTOM = (2, 4, 12)
HUD_BG = (8, 13, 32)
TEXT = (238, 242, 255)
MUTED = (148, 163, 184)
POWER = (255, 255, 255)
FRIGHTENED_BLUE = (29, 78, 216)
FRIGHTENED_FLASH = (248, 250, 252)
PANEL = (12, 20, 48)
PANEL_EDGE = (51, 65, 120)
SPARK = (252, 211, 77)
PLATINUM = (226, 232, 240)
PREMIUM_GOLD = (251, 191, 36)
NEON_PURPLE = (168, 85, 247)
GLASS = (15, 23, 42)
CRITICAL = (244, 63, 94)







UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
STOP = (0, 0)
DIRECTIONS = [UP, DOWN, LEFT, RIGHT]





MAZE = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
    [0, 2, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 2, 0],
    [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 2, 0, 2, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 3, 3, 3, 3, 3, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 3, 3, 3, 3, 3, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 3, 3, 3, 3, 3, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
    [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
    [0, 2, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 2, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]






PACMAN_START = (9, 16)
GHOST_STARTS = [(9, 9), (9, 10), (10, 9), (8, 9)]








SCATTER_TARGETS = {


    "blinky": (17, 1),
    "pinky": (1, 1),
    "inky": (17, 19),
    "clyde": (1, 19),
}





def clamp(value, low, high):
    return max(low, min(high, value))




def blend_color(a, b, ratio):
    ratio = clamp(ratio, 0, 1)
    return tuple(int(a[index] + (b[index] - a[index]) * ratio) for index in range(3))




def with_alpha(color, alpha):
    return color[0], color[1], color[2], alpha





def ease_out_cubic(t):
    t = clamp(t, 0, 1)
    return 1 - (1 - t) ** 3


def ease_in_out(t):
    t = clamp(t, 0, 1)
    return t * t * (3 - 2 * t)


def tile_to_pixel(x, y):
    return x * TILE_SIZE, HUD_HEIGHT + y * TILE_SIZE


def tile_center(x, y):
    px, py = tile_to_pixel(x, y)
    return px + TILE_SIZE // 2, py + TILE_SIZE // 2


def tile_rect(x, y, inset=0):
    px, py = tile_to_pixel(x, y)
    return pygame.Rect(
        px + inset,
        py + inset,
        TILE_SIZE - inset * 2,
        TILE_SIZE - inset * 2,
    )


def pixel_to_tile(pos):
    return pos[0] // TILE_SIZE, (pos[1] - HUD_HEIGHT) // TILE_SIZE


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def opposite_dir(direction):
    return (-direction[0], -direction[1])


def direction_angle(direction):
    if direction == LEFT:
        return math.pi
    if direction == UP:
        return -math.pi / 2
    if direction == DOWN:
        return math.pi / 2
    return 0


def is_open_tile(tile, walls):
    x, y = tile
    return 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT and tile not in walls


def draw_glow_circle(surface, center, color, radius, layers=5, alpha=95):
    if radius <= 0:
        return

    size = radius * 2 + 8
    glow = pygame.Surface((size, size), pygame.SRCALPHA)
    local_center = size // 2, size // 2
    for layer in range(layers, 0, -1):
        layer_ratio = layer / layers
        layer_radius = max(1, int(radius * layer_ratio))
        layer_alpha = int(alpha * (1 - layer_ratio * 0.72))
        pygame.draw.circle(glow, with_alpha(color, layer_alpha), local_center, layer_radius)
    surface.blit(glow, (center[0] - size // 2, center[1] - size // 2))


def draw_text_shadow(surface, font, text, pos, color, shadow=(0, 0, 0), offset=(2, 2)):
    shadow_img = font.render(text, True, shadow)
    text_img = font.render(text, True, color)
    surface.blit(shadow_img, (pos[0] + offset[0], pos[1] + offset[1]))
    surface.blit(text_img, pos)
    return text_img


def draw_panel(surface, rect, fill=PANEL, edge=PANEL_EDGE):
    shadow_rect = rect.move(3, 4)
    pygame.draw.rect(surface, (0, 0, 0), shadow_rect, border_radius=14)
    pygame.draw.rect(surface, fill, rect, border_radius=10)
    glass = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    for y in range(rect.height):
        ratio = y / max(1, rect.height - 1)
        alpha = int(52 * (1 - ratio))
        pygame.draw.line(glass, (255, 255, 255, alpha), (0, y), (rect.width, y))
    surface.blit(glass, rect.topleft)
    pygame.draw.rect(surface, edge, rect, width=2, border_radius=10)
    highlight = rect.inflate(-8, -8)
    pygame.draw.line(surface, blend_color(fill, WHITE, 0.25), highlight.topleft, highlight.topright, 1)


def nearest_open_tile(target, walls, open_tiles):
    tx = clamp(target[0], 0, GRID_WIDTH - 1)
    ty = clamp(target[1], 0, GRID_HEIGHT - 1)
    target = (tx, ty)
    if is_open_tile(target, walls):
        return target

    return min(open_tiles, key=lambda tile: manhattan(tile, target))


def validate_maze():
    if len(MAZE) != GRID_HEIGHT:
        raise ValueError("MAZE height does not match GRID_HEIGHT")
    for row in MAZE:
        if len(row) != GRID_WIDTH:
            raise ValueError("Every MAZE row must match GRID_WIDTH")






def bfs_path(start, target, walls):
    queue = deque([(start, [])])
    visited = {start}
    while queue:
        pos, path = queue.popleft()
        if pos == target:
            return path + [pos]
        for dx, dy in DIRECTIONS:
            nx, ny = pos[0] + dx, pos[1] + dy
            next_tile = (nx, ny)
            if is_open_tile(next_tile, walls) and next_tile not in visited:
                visited.add(next_tile)
                queue.append((next_tile, path + [pos]))
    return []


# -------------------------------
# Classes
# -------------------------------
class Pacman:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = STOP
        self.next_direction = STOP
        self.radius = TILE_SIZE // 2 - 5

    def update(self, walls):
        old_tile = self.get_tile()

        if self.next_direction != STOP:
            dx, dy = self.next_direction
            if is_open_tile((self.x + dx, self.y + dy), walls):
                self.direction = self.next_direction

        dx, dy = self.direction
        new_tile = (self.x + dx, self.y + dy)
        if is_open_tile(new_tile, walls):
            self.x, self.y = new_tile

        return old_tile, self.get_tile()

    def draw(self, screen, animation_ms):
        cx, cy = tile_center(self.x, self.y)
        direction = self.direction if self.direction != STOP else RIGHT
        angle = direction_angle(direction)
        mouth = 0.22 + 0.42 * abs(math.sin(animation_ms / 110))

        draw_glow_circle(screen, (cx, cy), YELLOW, self.radius + 18, layers=7, alpha=78)
        pygame.draw.circle(screen, (0, 0, 0), (cx + 4, cy + 5), self.radius + 1)
        pygame.draw.circle(screen, GOLD, (cx + 2, cy + 2), self.radius)
        pygame.draw.circle(screen, YELLOW, (cx, cy), self.radius)
        pygame.draw.circle(screen, blend_color(YELLOW, WHITE, 0.35), (cx - 5, cy - 7), self.radius // 3)

        mouth_points = [
            (cx, cy),
            (
                cx + int((self.radius + 5) * math.cos(angle + mouth)),
                cy + int((self.radius + 5) * math.sin(angle + mouth)),
            ),
            (
                cx + int((self.radius + 5) * math.cos(angle - mouth)),
                cy + int((self.radius + 5) * math.sin(angle - mouth)),
            ),
        ]
        pygame.draw.polygon(screen, BLACK, mouth_points)
        pygame.draw.arc(
            screen,
            blend_color(YELLOW, WHITE, 0.5),
            pygame.Rect(cx - self.radius + 2, cy - self.radius + 2, self.radius * 2 - 4, self.radius * 2 - 4),
            angle - 2.35,
            angle - 0.8,
            2,
        )

        eye_offsets = {
            RIGHT: (5, -9),
            LEFT: (-5, -9),
            UP: (8, -5),
            DOWN: (8, 5),
            STOP: (5, -9),
        }
        ex, ey = eye_offsets.get(direction, eye_offsets[RIGHT])
        pygame.draw.circle(screen, BLACK, (cx + ex, cy + ey), 4)
        pygame.draw.circle(screen, WHITE, (cx + ex - 1, cy + ey - 1), 1)

    def get_tile(self):
        return self.x, self.y


class Ghost:
    def __init__(self, x, y, color, name, ai_type):
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y
        self.color = color
        self.name = name
        self.ai_type = ai_type
        self.direction = random.choice(DIRECTIONS)
        self.mode = "scatter"
        self.frightened_ms = 0

    def get_tile(self):
        return self.x, self.y

    def set_base_mode(self, mode):
        if self.mode != "frightened":
            self.mode = mode

    def frighten(self):
        self.mode = "frightened"
        self.frightened_ms = FRIGHTENED_MS
        if self.direction != STOP:
            self.direction = opposite_dir(self.direction)

    def tick_frightened(self, dt, base_mode):
        if self.mode != "frightened":
            return

        self.frightened_ms -= dt
        if self.frightened_ms <= 0:
            self.frightened_ms = 0
            self.mode = base_mode

    def choose_direction(self, pacman, walls, ghosts, open_tiles):
        possible = []
        for dx, dy in DIRECTIONS:
            nx, ny = self.x + dx, self.y + dy
            if is_open_tile((nx, ny), walls):
                possible.append((dx, dy, nx, ny))

        if not possible:
            return STOP

        opposite = opposite_dir(self.direction)
        choices = possible
        if len(possible) > 1:
            choices = [move for move in possible if (move[0], move[1]) != opposite]
            if not choices:
                choices = possible

        if self.mode == "frightened":
            return random.choice(choices)[:2]

        target = nearest_open_tile(self.get_target(pacman, ghosts), walls, open_tiles)
        path = bfs_path((self.x, self.y), target, walls)
        if len(path) >= 2:
            next_tile = path[1]
            path_dir = (next_tile[0] - self.x, next_tile[1] - self.y)
            if len(possible) == 1 or path_dir != opposite:
                return path_dir

        best_move = min(
            choices,
            key=lambda move: manhattan((move[2], move[3]), target),
        )
        return best_move[:2]

    def get_target(self, pacman, ghosts):
        pacman_tile = pacman.get_tile()

        if self.mode == "scatter":
            return SCATTER_TARGETS.get(self.name, (1, 1))

        if self.name == "blinky":
            return pacman_tile

        if self.name == "pinky":
            dx, dy = pacman.direction if pacman.direction != STOP else RIGHT
            return pacman_tile[0] + dx * 4, pacman_tile[1] + dy * 4

        if self.name == "inky":
            blinky = next((ghost for ghost in ghosts if ghost.name == "blinky"), None)
            dx, dy = pacman.direction if pacman.direction != STOP else RIGHT
            ahead = (pacman_tile[0] + dx * 2, pacman_tile[1] + dy * 2)
            if blinky:
                return ahead[0] + (ahead[0] - blinky.x), ahead[1] + (ahead[1] - blinky.y)
            return ahead

        if self.name == "clyde":
            if manhattan(self.get_tile(), pacman_tile) <= 6:
                return SCATTER_TARGETS["clyde"]
            return pacman_tile

        if self.ai_type == "random":
            return random.randint(1, GRID_WIDTH - 2), random.randint(1, GRID_HEIGHT - 2)

        return pacman_tile

    def update(self, pacman, walls, ghosts, open_tiles):
        new_dir = self.choose_direction(pacman, walls, ghosts, open_tiles)
        if new_dir == STOP:
            self.direction = STOP
            return

        new_tile = (self.x + new_dir[0], self.y + new_dir[1])
        if is_open_tile(new_tile, walls):
            self.direction = new_dir
            self.x, self.y = new_tile
        else:
            self.direction = STOP

    def draw(self, screen, animation_ms):
        cx, cy = tile_center(self.x, self.y)
        r = TILE_SIZE // 2 - 6

        if self.mode == "frightened":
            flashing = self.frightened_ms < 1800 and (animation_ms // 180) % 2 == 0
            color = FRIGHTENED_FLASH if flashing else FRIGHTENED_BLUE
            eye_color = BLACK if flashing else WHITE
        else:
            color = self.color
            eye_color = WHITE

        draw_glow_circle(screen, (cx, cy), color, r + 16, layers=6, alpha=70)
        pygame.draw.circle(screen, (0, 0, 0), (cx + 4, cy + 5), r + 1)
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(cx - r + 4, cy - 3, r * 2, r + 14), border_radius=4)

        body_rect = pygame.Rect(cx - r, cy - 5, r * 2, r + 15)
        pygame.draw.circle(screen, color, (cx, cy - 5), r)
        pygame.draw.rect(screen, color, body_rect, border_radius=5)
        pygame.draw.arc(
            screen,
            blend_color(color, WHITE, 0.38),
            pygame.Rect(cx - r + 3, cy - r - 2, r * 2 - 6, r * 2 - 6),
            math.pi * 0.95,
            math.pi * 1.78,
            2,
        )
        pygame.draw.line(screen, blend_color(color, WHITE, 0.24), (cx - r + 5, cy - 1), (cx + r - 5, cy - 1), 1)

        wave_y = cy + r + 6
        leg_points = []
        for index, offset in enumerate(range(-r, r + 1, 7)):
            y_offset = 5 if index % 2 else -1
            leg_points.append((cx + offset, wave_y + y_offset))
        pygame.draw.polygon(
            screen,
            color,
            [(cx - r, cy + 5), *leg_points, (cx + r, cy + 5)],
        )
        pygame.draw.line(screen, blend_color(color, BLACK, 0.18), (cx - r + 2, wave_y + 3), (cx + r - 2, wave_y + 3), 1)

        if self.mode == "frightened":
            pygame.draw.circle(screen, eye_color, (cx - 7, cy - 8), 3)
            pygame.draw.circle(screen, eye_color, (cx + 7, cy - 8), 3)
            mouth = [
                (cx - 10, cy + 9),
                (cx - 5, cy + 5),
                (cx, cy + 9),
                (cx + 5, cy + 5),
                (cx + 10, cy + 9),
            ]
            pygame.draw.lines(screen, eye_color, False, mouth, 2)
            return

        look_x = self.direction[0] * 2
        look_y = self.direction[1] * 2
        for eye_x in (cx - 7, cx + 7):
            pygame.draw.ellipse(screen, WHITE, pygame.Rect(eye_x - 5, cy - 14, 10, 12))
            pygame.draw.circle(screen, BLACK, (eye_x + look_x, cy - 8 + look_y), 3)
            pygame.draw.circle(screen, WHITE, (eye_x + look_x - 1, cy - 9 + look_y), 1)

    def reset(self, base_mode="scatter"):
        self.x = self.start_x
        self.y = self.start_y
        self.mode = base_mode
        self.frightened_ms = 0
        self.direction = random.choice(DIRECTIONS)


class Game:
    def __init__(self):
        validate_maze()
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Advanced Pac-Man")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)
        self.big_font = pygame.font.Font(None, 58)
        self.high_score = 0
        self.animation_ms = 0
        self.stars = [
            (
                random.randrange(0, SCREEN_WIDTH),
                random.randrange(HUD_HEIGHT, SCREEN_HEIGHT),
                random.choice((1, 1, 1, 2)),
                random.randrange(35, 120),
            )
            for _ in range(90)
        ]
        self.new_game()

    def new_game(self):
        self.score = 0
        self.lives = 3
        self.level = 1
        self.game_over = False
        self.paused = False
        self.won = False
        self.load_level()

    def load_level(self):
        self.walls = set()
        self.pellets = set()
        self.power_pellets = set()
        self.open_tiles = []

        for y, row in enumerate(MAZE):
            for x, val in enumerate(row):
                tile = (x, y)
                if val == 0:
                    self.walls.add(tile)
                else:
                    self.open_tiles.append(tile)
                    if val == 1:
                        self.pellets.add(tile)
                    elif val == 2:
                        self.power_pellets.add(tile)

        self.pacman_start = PACMAN_START
        if not is_open_tile(self.pacman_start, self.walls):
            raise ValueError("PACMAN_START must be inside the maze and not on a wall")

        for start in GHOST_STARTS:
            if not is_open_tile(start, self.walls):
                raise ValueError("Ghost starts must be inside the maze and not on walls")

        self.pacman = Pacman(*self.pacman_start)
        self.ghost_mode = "scatter"
        self.mode_timer_ms = 0
        self.pacman_timer_ms = 0
        self.ghost_timer_ms = 0
        self.ready_ms = READY_MS
        self.ghost_combo = 200
        self.particles = []
        self.pacman_trail = []
        self.screen_flash_ms = 0
        self.caught_active = False
        self.caught_elapsed_ms = 0
        self.caught_tile = self.pacman_start
        self.caught_ghost_color = CRITICAL
        self.caught_direction = RIGHT

        self.ghosts = [
            Ghost(GHOST_STARTS[0][0], GHOST_STARTS[0][1], RED, "blinky", "chase"),
            Ghost(GHOST_STARTS[1][0], GHOST_STARTS[1][1], PINK, "pinky", "ambush"),
            Ghost(GHOST_STARTS[2][0], GHOST_STARTS[2][1], CYAN, "inky", "chase"),
            Ghost(GHOST_STARTS[3][0], GHOST_STARTS[3][1], ORANGE, "clyde", "random"),
        ]

    def reset_positions(self):
        self.pacman = Pacman(*self.pacman_start)
        self.ghost_mode = "scatter"
        self.mode_timer_ms = 0
        self.pacman_timer_ms = 0
        self.ghost_timer_ms = 0
        self.ready_ms = READY_MS
        self.pacman_trail.clear()
        self.particles.clear()
        self.screen_flash_ms = 0
        self.caught_active = False
        self.caught_elapsed_ms = 0
        self.caught_direction = RIGHT
        for ghost in self.ghosts:
            ghost.reset(self.ghost_mode)

    def pacman_interval(self):
        return max(MIN_PACMAN_MOVE_MS, PACMAN_MOVE_MS - (self.level - 1) * 6)

    def ghost_interval(self):
        return max(MIN_GHOST_MOVE_MS, GHOST_MOVE_MS - (self.level - 1) * 8)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                self.new_game()
                continue

            if self.caught_active:
                continue

            if event.key in (pygame.K_SPACE, pygame.K_p):
                if not self.game_over:
                    self.paused = not self.paused
                continue

            if self.game_over:
                continue

            if event.key in (pygame.K_UP, pygame.K_w):
                self.pacman.next_direction = UP
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.pacman.next_direction = DOWN
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                self.pacman.next_direction = LEFT
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self.pacman.next_direction = RIGHT

        return True

    def update(self, dt):
        self.animation_ms += dt
        self.update_visual_effects(dt)

        if self.caught_active:
            self.update_caught_animation(dt)
            return

        if self.game_over or self.paused:
            return

        if self.ready_ms > 0:
            self.ready_ms = max(0, self.ready_ms - dt)
            return

        self.update_mode_timer(dt)
        for ghost in self.ghosts:
            ghost.tick_frightened(dt, self.ghost_mode)

        self.pacman_timer_ms += dt
        if self.pacman_timer_ms >= self.pacman_interval():
            self.pacman_timer_ms %= self.pacman_interval()
            old_tile, new_tile = self.pacman.update(self.walls)
            if old_tile != new_tile:
                self.add_pacman_trail(old_tile)
            level_changed = self.collect_current_tile()
            if level_changed:
                return
            if self.handle_collisions():
                return

        self.ghost_timer_ms += dt
        if self.ghost_timer_ms >= self.ghost_interval():
            self.ghost_timer_ms %= self.ghost_interval()
            for ghost in self.ghosts:
                ghost.set_base_mode(self.ghost_mode)
                ghost.update(self.pacman, self.walls, self.ghosts, self.open_tiles)
            self.handle_collisions()

    def update_visual_effects(self, dt):
        for trail in self.pacman_trail:
            trail["age"] += dt
        self.pacman_trail = [trail for trail in self.pacman_trail if trail["age"] < trail["life"]]

        for particle in self.particles:
            particle["age"] += dt
            particle["x"] += particle["vx"] * dt / 16
            particle["y"] += particle["vy"] * dt / 16
            particle["vy"] += particle["gravity"] * dt / 16
        self.particles = [
            particle for particle in self.particles if particle["age"] < particle["life"]
        ]

        self.screen_flash_ms = max(0, self.screen_flash_ms - dt)

    def update_caught_animation(self, dt):
        self.caught_elapsed_ms += dt
        progress = self.caught_elapsed_ms / CAUGHT_ANIMATION_MS

        if progress < 1:
            if int(self.caught_elapsed_ms) % 120 < dt:
                color = random.choice((YELLOW, PREMIUM_GOLD, self.caught_ghost_color, WHITE))
                self.spawn_particles(self.caught_tile, color, count=4, speed=2.7, life=360)
            return

        self.caught_active = False
        self.finish_life_loss()

    def add_pacman_trail(self, tile):
        cx, cy = tile_center(*tile)
        self.pacman_trail.append(
            {
                "x": cx,
                "y": cy,
                "age": 0,
                "life": 260,
                "radius": self.pacman.radius + 2,
            }
        )
        if len(self.pacman_trail) > 7:
            self.pacman_trail.pop(0)

    def spawn_particles(self, tile, color, count=10, speed=2.2, life=420):
        cx, cy = tile_center(*tile)
        for _ in range(count):
            angle = random.uniform(0, math.tau)
            velocity = random.uniform(speed * 0.35, speed)
            self.particles.append(
                {
                    "x": cx,
                    "y": cy,
                    "vx": math.cos(angle) * velocity,
                    "vy": math.sin(angle) * velocity,
                    "gravity": random.uniform(-0.015, 0.035),
                    "age": 0,
                    "life": random.randint(int(life * 0.65), int(life * 1.25)),
                    "radius": random.randint(2, 5),
                    "color": color,
                }
            )

    def trigger_caught_animation(self, ghost):
        self.caught_active = True
        self.caught_elapsed_ms = 0
        self.caught_tile = self.pacman.get_tile()
        self.caught_ghost_color = ghost.color
        self.caught_direction = self.pacman.direction if self.pacman.direction != STOP else RIGHT
        self.pacman.direction = STOP
        self.pacman.next_direction = STOP
        self.screen_flash_ms = 420
        self.spawn_particles(self.caught_tile, CRITICAL, count=42, speed=4.7, life=820)

    def update_mode_timer(self, dt):
        self.mode_timer_ms += dt
        duration = SCATTER_MS if self.ghost_mode == "scatter" else CHASE_MS
        if self.mode_timer_ms < duration:
            return

        self.mode_timer_ms = 0
        self.ghost_mode = "chase" if self.ghost_mode == "scatter" else "scatter"
        for ghost in self.ghosts:
            if ghost.mode != "frightened":
                ghost.mode = self.ghost_mode
                if ghost.direction != STOP:
                    ghost.direction = opposite_dir(ghost.direction)

    def collect_current_tile(self):
        pac_tile = self.pacman.get_tile()
        if pac_tile in self.pellets:
            self.pellets.remove(pac_tile)
            self.add_score(10)
            self.spawn_particles(pac_tile, WHITE, count=5, speed=1.4, life=260)

        if pac_tile in self.power_pellets:
            self.power_pellets.remove(pac_tile)
            self.add_score(50)
            self.ghost_combo = 200
            self.screen_flash_ms = 280
            self.spawn_particles(pac_tile, SPARK, count=28, speed=4.2, life=650)
            for ghost in self.ghosts:
                ghost.frighten()

        if not self.pellets and not self.power_pellets:
            self.level += 1
            self.add_score(LEVEL_BONUS)
            self.load_level()
            return True

        return False

    def add_score(self, amount):
        self.score += amount
        self.high_score = max(self.high_score, self.score)

    def handle_collisions(self):
        if self.caught_active:
            return True

        for ghost in self.ghosts:
            if ghost.get_tile() != self.pacman.get_tile():
                continue

            if ghost.mode == "frightened":
                self.add_score(self.ghost_combo)
                self.ghost_combo = min(self.ghost_combo * 2, 1600)
                self.spawn_particles(ghost.get_tile(), ghost.color, count=24, speed=3.8, life=620)
                ghost.reset(self.ghost_mode)
            else:
                self.trigger_caught_animation(ghost)
            return True
        return False

    def lose_life(self):
        self.trigger_caught_animation(next(iter(self.ghosts)))

    def finish_life_loss(self):
        self.lives -= 1
        if self.lives <= 0:
            self.game_over = True
            self.won = False
            self.high_score = max(self.high_score, self.score)
            return

        self.reset_positions()

    def draw(self):
        self.draw_background()
        self.draw_hud()
        self.draw_maze()
        self.draw_pellets()
        self.draw_trails()

        if not self.caught_active:
            self.pacman.draw(self.screen, self.animation_ms)
        for ghost in self.ghosts:
            ghost.draw(self.screen, self.animation_ms)
        if self.caught_active:
            self.draw_caught_animation()
        self.draw_particles()

        if self.ready_ms > 0 and not self.game_over:
            self.draw_center_message("READY!", "Use arrows or WASD")
        elif self.paused:
            self.draw_center_message("PAUSED", "Press Space or P to continue")
        elif self.game_over:
            self.draw_center_message("GAME OVER", "Press R to restart")

        self.draw_vignette()
        self.draw_screen_flash()
        pygame.display.flip()

    def draw_background(self):
        for y in range(SCREEN_HEIGHT):
            ratio = y / max(1, SCREEN_HEIGHT - 1)
            color = tuple(
                int(BG_TOP[index] + (BG_BOTTOM[index] - BG_TOP[index]) * ratio)
                for index in range(3)
            )
            pygame.draw.line(self.screen, color, (0, y), (SCREEN_WIDTH, y))

        for x, y, radius, alpha in self.stars:
            twinkle = 0.45 + 0.55 * math.sin((self.animation_ms + x * 13 + y * 7) / 700)
            star_color = blend_color((16, 24, 52), (125, 211, 252), twinkle)
            pygame.draw.circle(self.screen, star_color, (x, y), radius)
            if alpha > 80:
                pygame.draw.circle(self.screen, blend_color(star_color, WHITE, 0.3), (x, y), 1)

        board_rect = pygame.Rect(0, HUD_HEIGHT, SCREEN_WIDTH, GRID_HEIGHT * TILE_SIZE)
        pygame.draw.rect(self.screen, BLACK, board_rect)
        pygame.draw.rect(self.screen, (3, 8, 24), board_rect.inflate(-14, -14), border_radius=18)
        draw_glow_circle(
            self.screen,
            (SCREEN_WIDTH // 2, HUD_HEIGHT + GRID_HEIGHT * TILE_SIZE // 2),
            NEON_PURPLE,
            230,
            layers=8,
            alpha=34,
        )
        draw_glow_circle(
            self.screen,
            (SCREEN_WIDTH // 2, HUD_HEIGHT + 110),
            WALL_HOT,
            170,
            layers=7,
            alpha=24,
        )

        grid = pygame.Surface((SCREEN_WIDTH, GRID_HEIGHT * TILE_SIZE), pygame.SRCALPHA)
        for x in range(0, SCREEN_WIDTH, TILE_SIZE):
            pygame.draw.line(grid, (32, 54, 112, 26), (x, 0), (x, GRID_HEIGHT * TILE_SIZE))
        for y in range(0, GRID_HEIGHT * TILE_SIZE, TILE_SIZE):
            pygame.draw.line(grid, (32, 54, 112, 18), (0, y), (SCREEN_WIDTH, y))
        self.screen.blit(grid, (0, HUD_HEIGHT))

        scanlines = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        for y in range(HUD_HEIGHT, SCREEN_HEIGHT, 5):
            pygame.draw.line(scanlines, (255, 255, 255, 10), (0, y), (SCREEN_WIDTH, y))
        self.screen.blit(scanlines, (0, 0))

    def draw_hud(self):
        pygame.draw.rect(self.screen, HUD_BG, pygame.Rect(0, 0, SCREEN_WIDTH, HUD_HEIGHT))
        pygame.draw.line(self.screen, WALL_HOT, (0, HUD_HEIGHT - 1), (SCREEN_WIDTH, HUD_HEIGHT - 1), 2)

        left_panel = pygame.Rect(12, 10, 300, 52)
        mid_panel = pygame.Rect(326, 10, 190, 52)
        right_panel = pygame.Rect(530, 10, 218, 52)
        draw_panel(self.screen, left_panel)
        draw_panel(self.screen, mid_panel)
        draw_panel(self.screen, right_panel)

        draw_text_shadow(self.screen, self.font, "ADVANCED PAC-MAN", (24, 15), YELLOW)
        draw_text_shadow(self.screen, self.small_font, f"Score {self.score}", (24, 42), TEXT, shadow=(3, 5, 15), offset=(1, 1))
        draw_text_shadow(self.screen, self.small_font, f"High {self.high_score}", (150, 42), MUTED, shadow=(3, 5, 15), offset=(1, 1))
        level = self.small_font.render(f"Level {self.level}", True, TEXT)
        lives = self.small_font.render(f"Lives {self.lives}", True, TEXT)

        frightened = any(ghost.mode == "frightened" for ghost in self.ghosts)
        mode_text = "FRIGHTENED" if frightened else self.ghost_mode.upper()
        mode_color = FRIGHTENED_FLASH if frightened else WALL_EDGE
        mode = self.small_font.render(mode_text, True, mode_color)

        self.screen.blit(mode, (mid_panel.centerx - mode.get_width() // 2, 18))
        pygame.draw.rect(
            self.screen,
            mode_color,
            pygame.Rect(mid_panel.x + 18, 44, mid_panel.width - 36, 5),
            border_radius=5,
        )

        self.screen.blit(level, (right_panel.x + 16, 18))
        self.screen.blit(lives, (right_panel.x + 16, 42))
        for index in range(self.lives):
            cx = right_panel.right - 22 - index * 23
            pygame.draw.circle(self.screen, YELLOW, (cx, 45), 7)
            pygame.draw.polygon(self.screen, BLACK, [(cx, 45), (cx + 8, 41), (cx + 8, 49)])

    def draw_maze(self):
        glow = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        for x, y in self.walls:
            glow_rect = tile_rect(x, y, inset=1)
            pygame.draw.rect(glow, (37, 99, 235, 58), glow_rect, border_radius=11)
        self.screen.blit(glow, (0, 0))

        trace = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        open_set = set(self.open_tiles)
        pulse = 0.55 + 0.45 * math.sin(self.animation_ms / 950)
        trace_color = with_alpha(blend_color(WALL_EDGE, NEON_PURPLE, 0.35), int(42 + 34 * pulse))
        for x, y in self.open_tiles:
            start = tile_center(x, y)
            if (x + 1, y) in open_set:
                pygame.draw.line(trace, trace_color, start, tile_center(x + 1, y), 2)
            if (x, y + 1) in open_set:
                pygame.draw.line(trace, trace_color, start, tile_center(x, y + 1), 2)
        self.screen.blit(trace, (0, 0))

        for x, y in self.walls:
            shadow = tile_rect(x, y, inset=2).move(3, 4)
            outer = tile_rect(x, y, inset=3)
            mid = tile_rect(x, y, inset=5)
            inner = tile_rect(x, y, inset=9)
            pygame.draw.rect(self.screen, WALL_SHADOW, shadow, border_radius=10)
            pygame.draw.rect(self.screen, WALL_HOT, outer, border_radius=10)
            pygame.draw.rect(self.screen, WALL_EDGE, mid, border_radius=8)
            pygame.draw.rect(self.screen, WALL_FILL, inner, border_radius=5)
            pygame.draw.line(self.screen, blend_color(WALL_HOT, WHITE, 0.25), (outer.left + 7, outer.top + 5), (outer.right - 7, outer.top + 5), 1)
            pygame.draw.line(self.screen, blend_color(WALL_FILL, BLACK, 0.22), (inner.left + 3, inner.bottom - 3), (inner.right - 3, inner.bottom - 3), 1)

        # Subtle guide dots in empty corridors make motion easier to read.
        for x, y in self.open_tiles:
            if (x, y) in self.pellets or (x, y) in self.power_pellets:
                continue
            cx, cy = tile_center(x, y)
            pygame.draw.circle(self.screen, (10, 28, 64), (cx, cy), 2)

    def draw_pellets(self):
        pellet_pulse = 1 + 0.25 * math.sin(self.animation_ms / 180)
        power_pulse = 1 + 0.18 * math.sin(self.animation_ms / 120)

        for x, y in self.pellets:
            cx, cy = tile_center(x, y)
            radius = max(3, int(4 * pellet_pulse))
            pygame.draw.circle(self.screen, (45, 55, 78), (cx, cy), radius + 3)
            pygame.draw.circle(self.screen, WHITE, (cx, cy), radius)
            pygame.draw.circle(self.screen, blend_color(WHITE, YELLOW, 0.35), (cx - 1, cy - 1), max(1, radius - 2))

        for x, y in self.power_pellets:
            cx, cy = tile_center(x, y)
            glow_radius = int(15 * power_pulse)
            core_radius = int(9 * power_pulse)
            draw_glow_circle(self.screen, (cx, cy), POWER, glow_radius + 12, layers=6, alpha=105)
            pygame.draw.circle(self.screen, (64, 64, 64), (cx, cy), glow_radius)
            pygame.draw.circle(self.screen, POWER, (cx, cy), core_radius)
            pygame.draw.circle(self.screen, SPARK, (cx - 3, cy - 3), max(2, core_radius // 3))

    def draw_trails(self):
        for trail in self.pacman_trail:
            progress = trail["age"] / trail["life"]
            alpha = int(120 * (1 - progress))
            radius = max(2, int(trail["radius"] * (1 - progress * 0.35)))
            trail_surface = pygame.Surface((radius * 2 + 4, radius * 2 + 4), pygame.SRCALPHA)
            pygame.draw.circle(
                trail_surface,
                with_alpha(YELLOW, alpha),
                (radius + 2, radius + 2),
                radius,
            )
            self.screen.blit(trail_surface, (trail["x"] - radius - 2, trail["y"] - radius - 2))

    def draw_particles(self):
        for particle in self.particles:
            progress = particle["age"] / particle["life"]
            alpha = int(210 * (1 - progress))
            radius = max(1, int(particle["radius"] * (1 - progress * 0.55)))
            color = particle["color"]
            spark = pygame.Surface((radius * 6, radius * 6), pygame.SRCALPHA)
            center = radius * 3, radius * 3
            pygame.draw.circle(spark, with_alpha(color, max(20, alpha // 4)), center, radius * 3)
            pygame.draw.circle(spark, with_alpha(color, alpha), center, radius)
            self.screen.blit(spark, (int(particle["x"] - center[0]), int(particle["y"] - center[1])))

    def draw_caught_animation(self):
        progress = clamp(self.caught_elapsed_ms / CAUGHT_ANIMATION_MS, 0, 1)
        eased = ease_out_cubic(progress)
        cx, cy = tile_center(*self.caught_tile)

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, int(74 * ease_in_out(min(progress * 1.35, 1)))))
        self.screen.blit(overlay, (0, 0))

        pulse = math.sin(progress * math.pi)
        ring_color = blend_color(self.caught_ghost_color, CRITICAL, 0.45)
        shock = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        for index in range(4):
            ring_progress = clamp(progress * 1.25 - index * 0.16, 0, 1)
            if ring_progress <= 0:
                continue
            radius = int(18 + ring_progress * (95 + index * 20))
            alpha = int(150 * (1 - ring_progress))
            rect = pygame.Rect(0, 0, radius * 2, radius * 2)
            rect.center = (cx, cy)
            pygame.draw.ellipse(shock, with_alpha(ring_color, alpha), rect, 3)
        self.screen.blit(shock, (0, 0))

        draw_glow_circle(
            self.screen,
            (cx, cy),
            blend_color(YELLOW, CRITICAL, eased),
            int(70 + 60 * pulse),
            layers=8,
            alpha=int(125 * (1 - progress * 0.55)),
        )

        radius = max(3, int(self.pacman.radius * (1 - eased * 0.72)))
        wobble = math.sin(self.animation_ms / 42) * (1 - progress) * 7
        body_center = (int(cx + wobble), cy)
        pygame.draw.circle(self.screen, (0, 0, 0), (body_center[0] + 4, body_center[1] + 5), radius + 2)
        pygame.draw.circle(self.screen, blend_color(YELLOW, CRITICAL, eased * 0.65), body_center, radius)
        pygame.draw.circle(
            self.screen,
            blend_color(PREMIUM_GOLD, WHITE, 0.35),
            (body_center[0] - max(2, radius // 3), body_center[1] - max(2, radius // 3)),
            max(2, radius // 4),
        )

        bite_angle = direction_angle(self.caught_direction)
        mouth = 0.35 + eased * 2.35
        mouth_points = [
            body_center,
            (
                body_center[0] + int((radius + 20) * math.cos(bite_angle + mouth)),
                body_center[1] + int((radius + 20) * math.sin(bite_angle + mouth)),
            ),
            (
                body_center[0] + int((radius + 20) * math.cos(bite_angle - mouth)),
                body_center[1] + int((radius + 20) * math.sin(bite_angle - mouth)),
            ),
        ]
        pygame.draw.polygon(self.screen, BLACK, mouth_points)

        shard_count = 14
        for index in range(shard_count):
            angle = math.tau * index / shard_count + self.animation_ms / 320
            distance = 18 + eased * 74 + 8 * math.sin(index + self.animation_ms / 90)
            shard_x = cx + int(math.cos(angle) * distance)
            shard_y = cy + int(math.sin(angle) * distance)
            shard_radius = max(1, int(5 * (1 - progress)))
            pygame.draw.circle(
                self.screen,
                with_alpha(blend_color(PREMIUM_GOLD, CRITICAL, progress), int(210 * (1 - progress))),
                (shard_x, shard_y),
                shard_radius,
            )

        label_alpha = int(230 * pulse)
        if label_alpha > 0:
            label = self.font.render("CAUGHT!", True, blend_color(TEXT, CRITICAL, 0.45))
            label_surface = pygame.Surface((label.get_width() + 18, label.get_height() + 12), pygame.SRCALPHA)
            pygame.draw.rect(
                label_surface,
                (9, 16, 38, min(190, label_alpha)),
                label_surface.get_rect(),
                border_radius=8,
            )
            label_surface.blit(label, (9, 6))
            self.screen.blit(label_surface, (cx - label_surface.get_width() // 2, cy - 78))

    def draw_vignette(self):
        vignette = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        edge_steps = 18
        for index in range(edge_steps):
            alpha = int(8 + index * 4.2)
            rect = pygame.Rect(index * 3, HUD_HEIGHT + index * 3, SCREEN_WIDTH - index * 6, GRID_HEIGHT * TILE_SIZE - index * 6)
            pygame.draw.rect(vignette, (0, 0, 0, alpha), rect, width=5, border_radius=18)
        pygame.draw.rect(vignette, (255, 255, 255, 18), pygame.Rect(8, HUD_HEIGHT + 8, SCREEN_WIDTH - 16, GRID_HEIGHT * TILE_SIZE - 16), width=1, border_radius=18)
        self.screen.blit(vignette, (0, 0))

    def draw_screen_flash(self):
        if self.screen_flash_ms <= 0:
            return

        alpha = int(90 * (self.screen_flash_ms / 340))
        flash = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        flash.fill((255, 255, 255, alpha))
        self.screen.blit(flash, (0, 0))

    def draw_center_message(self, title, subtitle):
        overlay = pygame.Surface((SCREEN_WIDTH, GRID_HEIGHT * TILE_SIZE), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 168))
        self.screen.blit(overlay, (0, HUD_HEIGHT))

        center_y = HUD_HEIGHT + GRID_HEIGHT * TILE_SIZE // 2
        box = pygame.Rect(0, 0, 430, 132)
        box.center = (SCREEN_WIDTH // 2, center_y)
        draw_panel(self.screen, box, fill=(9, 16, 38), edge=WALL_HOT)
        title_text = self.big_font.render(title, True, YELLOW)
        subtitle_text = self.font.render(subtitle, True, TEXT)
        draw_glow_circle(self.screen, (SCREEN_WIDTH // 2, center_y - 18), YELLOW, 72, layers=7, alpha=55)
        self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, center_y - 44))
        self.screen.blit(subtitle_text, (SCREEN_WIDTH // 2 - subtitle_text.get_width() // 2, center_y + 12))

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS)
            running = self.handle_events()
            self.update(dt)
            self.draw()

        pygame.quit()
        sys.exit()


# -------------------------------
# Run the game
# -------------------------------
if __name__ == "__main__":
    game = Game()
    game.run()
