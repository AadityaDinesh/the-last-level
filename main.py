import pygame
import sys
import math
import random
import asyncio  # <-- ADDED FOR WEB COMPATIBILITY

# ============================================================
# THE LAST LEVEL
# ============================================================

pygame.init()

GAME_WIDTH = 960
GAME_HEIGHT = 540

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

FPS = 60

screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT),
    pygame.FULLSCREEN | pygame.SCALED
)

pygame.display.set_caption("THE LAST LEVEL")

canvas = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
clock = pygame.time.Clock()
random.seed(17)

# ============================================================
# COLORS
# ============================================================
GRASS = (48, 86, 49)
GRASS_DARK = (31, 61, 37)
GRASS_LIGHT = (65, 105, 56)

PATH = (108, 82, 60)
PATH_DARK = (83, 62, 48)
PATH_LIGHT = (132, 98, 67)

WATER = (25, 72, 103)
WATER_DARK = (17, 51, 75)
WATER_LIGHT = (40, 105, 135)

TREE_DARK = (15, 43, 27)
TREE = (23, 68, 34)
TREE_MID = (31, 84, 39)
TREE_LIGHT = (48, 105, 45)

TRUNK_DARK = (54, 37, 25)
TRUNK = (91, 57, 31)
TRUNK_LIGHT = (111, 68, 36)

ROCK_DARK = (56, 60, 61)
ROCK = (91, 94, 91)
ROCK_LIGHT = (125, 126, 116)

HOUSE_WALL = (112, 70, 43)
HOUSE_WALL_DARK = (78, 49, 35)
HOUSE_WALL_LIGHT = (143, 91, 49)

ROOF = (43, 36, 38)
ROOF_DARK = (29, 27, 30)
ROOF_LIGHT = (65, 51, 51)

WINDOW = (66, 113, 125)
WINDOW_LIGHT = (111, 159, 166)

WOOD = (105, 63, 34)
WOOD_DARK = (62, 40, 27)

GRAVE = (91, 93, 99)
GRAVE_LIGHT = (116, 118, 122)
GRAVE_DARK = (57, 59, 65)

PLAYER = (38, 88, 177)
PLAYER_LIGHT = (68, 125, 220)

NPC_RED = (151, 47, 47)
NPC_RED_DARK = (99, 34, 37)

SKIN = (198, 139, 101)
SKIN_LIGHT = (222, 159, 113)

BLACK = (9, 10, 13)
VERY_DARK = (14, 16, 19)
WHITE = (237, 234, 220)
GREY = (142, 144, 149)

GOLD = (190, 142, 48)
GOLD_LIGHT = (245, 194, 66)

RED = (205, 63, 59)
BLUE = (65, 130, 205)
YELLOW = (224, 177, 48)
PURPLE = (126, 76, 175)

# ============================================================
# FONTS & STATES
# ============================================================
font = pygame.font.Font(None, 25)
small_font = pygame.font.Font(None, 19)
medium_font = pygame.font.Font(None, 31)
large_font = pygame.font.Font(None, 54)
huge_font = pygame.font.Font(None, 76)

TITLE = 0
PLAYING = 1
ENDING = 2
SECRET = 3
PAUSED = 4

game_state = TITLE

dialogue_active = False
dialogue_index = 0
current_dialogue = []
ending_timer = 0
clue_stage = 0

player = pygame.Rect(100, 250, 22, 28)
PLAYER_SPEED = 3.4

npc = pygame.Rect(445, 250, 26, 34)
npc_dialogue = [
    "You're looking for the exit, aren't you?",
    "The gate is locked, but three hidden keys lie scattered in this realm.",
    "The terminal, the stone, and the sign each hold a piece of the seal.",
    "You must inspect all three relics to awaken the lock, then reach the end."
]

house = pygame.Rect(560, 55, 220, 160)
house_door = pygame.Rect(647, 190, 45, 25)

graveyard = pygame.Rect(515, 335, 265, 170)
graves = [
    pygame.Rect(545, 365, 23, 34),
    pygame.Rect(598, 355, 25, 38),
    pygame.Rect(650, 375, 24, 35),
    pygame.Rect(707, 355, 24, 38),
    pygame.Rect(565, 440, 25, 35),
    pygame.Rect(620, 425, 24, 39),
    pygame.Rect(675, 445, 24, 36),
    pygame.Rect(728, 425, 25, 39),
]

pond = pygame.Rect(20, 325, 175, 115)
gate = pygame.Rect(895, 215, 30, 125)
exit_zone = pygame.Rect(925, 215, 35, 125)
gate_open = False

paths = [
    pygame.Rect(0, 225, 960, 62),
    pygame.Rect(420, 255, 75, 285),
    pygame.Rect(770, 235, 190, 55)
]

tree_positions = [
    (30, 55), (95, 65), (165, 48), (235, 75), (305, 48),
    (45, 150), (120, 145), (195, 165),
    (25, 465), (90, 485), (160, 455), (230, 500), (305, 465), (355, 510),
    (350, 55), (405, 80),
    (815, 50), (875, 70), (935, 45),
    (825, 135), (900, 145),
    (815, 395), (875, 445), (930, 470),
    (330, 170), (390, 125),
]
trees = [pygame.Rect(x, y, 43, 56) for x, y in tree_positions]

rocks = [
    pygame.Rect(245, 305, 27, 20),
    pygame.Rect(310, 295, 22, 17),
    pygame.Rect(365, 320, 27, 20),
    pygame.Rect(270, 425, 26, 19),
    pygame.Rect(345, 455, 28, 20),
    pygame.Rect(810, 305, 25, 19),
    pygame.Rect(850, 350, 23, 18),
    pygame.Rect(820, 515, 27, 20),
    pygame.Rect(885, 390, 25, 19),
]

flowers = [
    (235, 165), (280, 195), (320, 250), (245, 485),
    (300, 450), (395, 205), (805, 290), (835, 330),
    (805, 515), (465, 505),
]

lanterns = [
    (220, 235), (510, 240), (810, 235),
    (875, 365), (475, 325), (870, 175),
]

fences = [
    pygame.Rect(505, 325, 275, 8),
    pygame.Rect(505, 325, 8, 180),
    pygame.Rect(772, 325, 8, 180),
    pygame.Rect(505, 497, 275, 8),
]

terminal = pygame.Rect(490, 120, 36, 40)
stone = pygame.Rect(650, 280, 30, 27)
sign = pygame.Rect(440, 450, 40, 32)

terminal_dialogue = [
    "The screen flickers with digital static...",
    "A corrupted archive log reads:",
    "\"A legendary developer crafted an input order to survive his own creation.\"",
    "\"Years later, it remains the ultimate sequence etched into gaming history.\""
]

stone_dialogue = [
    "An ancient monolith glows as you approach...",
    "An inscription is etched into the stone:",
    "\"Three keys bind the seal. Without all three will yield nothing.\"",
    "\"Seek the terminal, the stone, and the post before invoking the master command.\""
]

sign_dialogue = [
    "A weathered wooden post near the main gate:",
    "Scratched into the wood:",
    "\"Once all three keys are awakened, find the exit.\"",
    "\"Only then will the ancient sequence respond to your call.\""
]

keys = [
    {"rect": pygame.Rect(315, 445, 18, 18), "color": YELLOW, "collected": False},
    {"rect": pygame.Rect(735, 130, 18, 18), "color": BLUE, "collected": False},
    {"rect": pygame.Rect(730, 485, 18, 18), "color": RED, "collected": False}
]

KONAMI_CODE = [
    pygame.K_UP, pygame.K_UP,
    pygame.K_DOWN, pygame.K_DOWN,
    pygame.K_LEFT, pygame.K_RIGHT,
    pygame.K_LEFT, pygame.K_RIGHT,
    pygame.K_b, pygame.K_a
]

konami_progress = []

secret_message = [
    "YOU FOUND IT.",
    "",
    "THE GAME WAS NEVER THE CHALLENGE.",
    "",
    "YOUR NEXT CLUE:",
    "",
    "THE SPACE BEHIND A PLACE, WHERE EVERYONE COMES TOGETHER."
]

def collected_count():
    return sum(1 for key in keys if key["collected"])

def near(rect, distance=48):
    return player.colliderect(rect.inflate(distance, distance))

def draw_centered(text, y, font_object, color):
    surface = font_object.render(text, True, color)
    canvas.blit(surface, (GAME_WIDTH // 2 - surface.get_width() // 2, y))

def reset_game():
    global game_state, dialogue_active, dialogue_index
    global current_dialogue, gate_open, ending_timer
    global konami_progress, clue_stage

    player.x = 100
    player.y = 250

    for key in keys:
        key["collected"] = False

    gate_open = False
    clue_stage = 0
    dialogue_active = False
    dialogue_index = 0
    current_dialogue = npc_dialogue
    ending_timer = 0
    konami_progress = []
    game_state = PLAYING

def draw_background():
    canvas.fill(GRASS)
    for x in range(0, GAME_WIDTH, 32):
        for y in range(0, GAME_HEIGHT, 28):
            if any(path.collidepoint(x, y) for path in paths):
                continue
            offset = (x * 13 + y * 7) % 11
            if offset < 3:
                pygame.draw.line(canvas, GRASS_DARK, (x + 5, y + 9), (x + 7, y + 4), 1)

def draw_paths():
    for path in paths:
        pygame.draw.rect(canvas, PATH_DARK, path)
        inner = path.inflate(-2, -2)
        pygame.draw.rect(canvas, PATH, inner)

    for x in range(0, GAME_WIDTH, 55):
        pygame.draw.line(canvas, PATH_LIGHT, (x, 242), (x + 18, 242), 1)
        pygame.draw.line(canvas, PATH_DARK, (x + 25, 273), (x + 42, 273), 1)

def draw_pond():
    pygame.draw.ellipse(canvas, WATER_DARK, (pond.x - 7, pond.y + 5, pond.width + 14, pond.height))
    pygame.draw.ellipse(canvas, WATER, pond)
    pygame.draw.arc(canvas, WATER_LIGHT, (pond.x + 10, pond.y + 15, pond.width - 20, pond.height - 30), 0.3, 2.6, 2)
    pygame.draw.arc(canvas, WATER_LIGHT, (pond.x + 40, pond.y + 45, pond.width - 80, pond.height - 65), 0.3, 2.6, 1)
    pygame.draw.ellipse(canvas, (45, 90, 45), (55, 365, 15, 8))
    pygame.draw.ellipse(canvas, (45, 90, 45), (130, 390, 13, 7))

def draw_tree(tree):
    pygame.draw.ellipse(canvas, (27, 55, 32), (tree.x - 5, tree.bottom - 8, tree.width + 10, 14))
    pygame.draw.rect(canvas, TRUNK_DARK, (tree.centerx - 7, tree.y + 25, 14, 30))
    pygame.draw.rect(canvas, TRUNK, (tree.centerx - 4, tree.y + 25, 7, 30))
    pygame.draw.line(canvas, TRUNK_DARK, (tree.centerx, tree.y + 32), (tree.centerx - 13, tree.y + 20), 4)
    pygame.draw.line(canvas, TRUNK_DARK, (tree.centerx, tree.y + 34), (tree.centerx + 13, tree.y + 20), 4)
    pygame.draw.circle(canvas, TREE_DARK, (tree.centerx, tree.y + 19), 27)
    pygame.draw.circle(canvas, TREE, (tree.centerx - 8, tree.y + 13), 21)
    pygame.draw.circle(canvas, TREE_MID, (tree.centerx + 9, tree.y + 16), 20)
    pygame.draw.circle(canvas, TREE_LIGHT, (tree.centerx - 14, tree.y + 7), 7)
    pygame.draw.circle(canvas, TREE_MID, (tree.centerx + 5, tree.y + 2), 8)

def draw_rocks():
    for rock in rocks:
        pygame.draw.ellipse(canvas, (35, 62, 38), (rock.x - 3, rock.bottom - 2, rock.width + 6, 8))
        pygame.draw.ellipse(canvas, ROCK_DARK, rock)
        pygame.draw.ellipse(canvas, ROCK, (rock.x + 2, rock.y + 2, rock.width - 4, rock.height - 5))
        pygame.draw.line(canvas, ROCK_LIGHT, (rock.x + 5, rock.y + 4), (rock.right - 6, rock.y + 4), 1)

def draw_house():
    pygame.draw.rect(canvas, (32, 59, 34), (house.x + 8, house.y + 9, house.width, house.height))
    pygame.draw.rect(canvas, HOUSE_WALL_DARK, house)
    pygame.draw.rect(canvas, HOUSE_WALL, (house.x + 5, house.y + 5, house.width - 10, house.height - 10))

    for y in range(house.y + 25, house.bottom - 5, 28):
        pygame.draw.line(canvas, HOUSE_WALL_LIGHT, (house.x + 7, y), (house.right - 7, y), 1)

    roof_points = [
        (house.x - 28, house.y + 8),
        (house.centerx, house.y - 60),
        (house.right + 28, house.y + 8)
    ]
    pygame.draw.polygon(canvas, ROOF_DARK, roof_points)
    pygame.draw.polygon(canvas, ROOF, [
        (house.x - 18, house.y + 5),
        (house.centerx, house.y - 50),
        (house.right + 18, house.y + 5)
    ])

    for x in range(house.x - 5, house.right + 5, 22):
        pygame.draw.line(canvas, ROOF_LIGHT, (x, house.y - 2), (x + 13, house.y - 20), 2)

    chimney = pygame.Rect(house.x + 155, house.y - 38, 25, 38)
    pygame.draw.rect(canvas, ROOF_DARK, chimney)
    pygame.draw.rect(canvas, ROOF_LIGHT, (chimney.x + 3, chimney.y + 3, chimney.width - 6, 5))

    for x in [house.x + 28, house.right - 68]:
        window = pygame.Rect(x, house.y + 53, 40, 32)
        pygame.draw.rect(canvas, WOOD_DARK, window.inflate(5, 5))
        pygame.draw.rect(canvas, WINDOW, window)
        pygame.draw.rect(canvas, WINDOW_LIGHT, window, 2)
        pygame.draw.line(canvas, WINDOW_LIGHT, window.midleft, window.midright, 2)
        pygame.draw.line(canvas, WINDOW_LIGHT, window.midtop, window.midbottom, 2)

    pygame.draw.rect(canvas, WOOD_DARK, house_door.inflate(4, 4))
    pygame.draw.rect(canvas, WOOD, house_door)
    pygame.draw.line(canvas, (137, 84, 42), (house_door.x + 5, house_door.y + 6), (house_door.x + 5, house_door.bottom - 5), 2)
    pygame.draw.circle(canvas, GOLD, (house_door.right - 8, house_door.centery), 3)

def draw_graveyard():
    pygame.draw.rect(canvas, (39, 69, 42), graveyard)
    pygame.draw.rect(canvas, (35, 62, 38), graveyard.inflate(-8, -8))

    for grave in graves:
        pygame.draw.ellipse(canvas, (26, 49, 31), (grave.x - 5, grave.bottom - 2, grave.width + 10, 9))
        pygame.draw.rect(canvas, GRAVE_DARK, grave, border_radius=5)
        pygame.draw.rect(canvas, GRAVE, (grave.x + 2, grave.y + 2, grave.width - 4, grave.height - 4), border_radius=5)
        pygame.draw.rect(canvas, GRAVE_DARK, (grave.centerx - 2, grave.y - 8, 4, 14))
        pygame.draw.rect(canvas, GRAVE_DARK, (grave.centerx - 6, grave.y - 3, 12, 4))

def draw_fences():
    for fence in fences:
        pygame.draw.rect(canvas, WOOD_DARK, fence)
        if fence.width > fence.height:
            for x in range(fence.x, fence.right, 23):
                pygame.draw.rect(canvas, WOOD, (x, fence.y - 5, 7, 18))
        else:
            for y in range(fence.y, fence.bottom, 23):
                pygame.draw.rect(canvas, WOOD, (fence.x - 5, y, 18, 7))

def draw_flowers():
    for x, y in flowers:
        pygame.draw.line(canvas, (42, 91, 44), (x, y), (x, y + 10), 2)
        pygame.draw.circle(canvas, GOLD, (x, y), 3)
        pygame.draw.circle(canvas, WHITE, (x + 4, y), 3)
        pygame.draw.circle(canvas, WHITE, (x - 4, y), 3)

def draw_lantern(x, y):
    pygame.draw.rect(canvas, WOOD_DARK, (x - 3, y, 6, 34))
    pygame.draw.rect(canvas, WOOD_DARK, (x - 8, y - 12, 16, 18), border_radius=3)
    pygame.draw.rect(canvas, GOLD, (x - 5, y - 9, 10, 11), border_radius=2)
    pygame.draw.circle(canvas, GOLD_LIGHT, (x, y - 4), 4)

def draw_terminal():
    pygame.draw.rect(canvas, (27, 29, 31), terminal, border_radius=3)
    pygame.draw.rect(canvas, (17, 62, 43), (terminal.x + 5, terminal.y + 5, 26, 19))
    pygame.draw.rect(canvas, (50, 125, 75), (terminal.x + 9, terminal.y + 9, 5, 3))
    pygame.draw.rect(canvas, (50, 125, 75), (terminal.x + 17, terminal.y + 13, 7, 3))
    pygame.draw.rect(canvas, ROCK, (terminal.x + 8, terminal.bottom - 7, 20, 5))

def draw_stone():
    points = [
        (stone.x, stone.bottom),
        (stone.x + 5, stone.y),
        (stone.right, stone.y + 5),
        (stone.right - 5, stone.bottom)
    ]
    pygame.draw.polygon(canvas, ROCK_DARK, points)
    pygame.draw.line(canvas, ROCK_LIGHT, (stone.x + 7, stone.y + 5), (stone.right - 6, stone.y + 8), 2)

def draw_sign():
    pygame.draw.rect(canvas, WOOD_DARK, (sign.centerx - 3, sign.bottom - 2, 6, 25))
    pygame.draw.rect(canvas, WOOD, sign, border_radius=2)
    pygame.draw.line(canvas, GOLD, (sign.x + 8, sign.centery), (sign.right - 9, sign.centery), 2)
    pygame.draw.polygon(canvas, GOLD, [
        (sign.right - 12, sign.centery - 5),
        (sign.right - 5, sign.centery),
        (sign.right - 12, sign.centery + 5)
    ])

def draw_npc():
    pygame.draw.ellipse(canvas, (27, 55, 31), (npc.x - 5, npc.bottom - 2, npc.width + 10, 9))
    pygame.draw.rect(canvas, NPC_RED_DARK, npc, border_radius=5)
    pygame.draw.rect(canvas, NPC_RED, (npc.x + 3, npc.y + 3, npc.width - 6, npc.height - 5), border_radius=5)
    pygame.draw.circle(canvas, SKIN, (npc.centerx, npc.y - 6), 11)
    pygame.draw.circle(canvas, SKIN_LIGHT, (npc.centerx - 3, npc.y - 9), 6)
    pygame.draw.rect(canvas, (71, 48, 31), (npc.x - 6, npc.y - 17, npc.width + 12, 7))
    pygame.draw.rect(canvas, (88, 58, 35), (npc.x, npc.y - 22, npc.width, 8))
    pygame.draw.circle(canvas, BLACK, (npc.centerx - 4, npc.y - 7), 2)
    pygame.draw.circle(canvas, BLACK, (npc.centerx + 4, npc.y - 7), 2)

def draw_player():
    pygame.draw.ellipse(canvas, (27, 55, 31), (player.x - 3, player.bottom - 3, player.width + 6, 8))
    pygame.draw.rect(canvas, PLAYER, player, border_radius=4)
    pygame.draw.rect(canvas, PLAYER_LIGHT, (player.x + 3, player.y + 3, player.width - 6, 4), border_radius=2)
    pygame.draw.rect(canvas, WHITE, (player.x + 4, player.y + 8, 5, 5))
    pygame.draw.rect(canvas, WHITE, (player.x + 14, player.y + 8, 5, 5))

def draw_key(key):
    if key["collected"] or clue_stage < 3:
        return

    rect = key["rect"]
    dx = abs(player.centerx - rect.centerx)
    dy = abs(player.centery - rect.centery)

    if dx < 75 and dy < 75:
        pulse = math.sin(pygame.time.get_ticks() * 0.008)
        color = key["color"]
        pygame.draw.circle(canvas, color, rect.center, int(10 + pulse), 2)
        pygame.draw.circle(canvas, color, rect.center, 6, 3)
        pygame.draw.rect(canvas, color, (rect.centerx + 3, rect.centery - 2, 12, 4))
        pygame.draw.rect(canvas, color, (rect.centerx + 12, rect.centery + 2, 4, 6))

def draw_gate():
    if gate_open:
        pygame.draw.rect(canvas, WOOD_DARK, (gate.x, gate.y, 8, gate.height))
        pygame.draw.rect(canvas, WOOD_DARK, (gate.right - 8, gate.y, 8, gate.height))
        sign_rect = pygame.Rect(gate.x - 6, gate.y - 36, 65, 25)
        pygame.draw.rect(canvas, WOOD_DARK, sign_rect, border_radius=3)
        exit_text = small_font.render("EXIT  →", True, GOLD_LIGHT)
        canvas.blit(exit_text, (sign_rect.x + 6, sign_rect.y + 5))
    else:
        pygame.draw.rect(canvas, WOOD_DARK, gate)
        for y in range(gate.y + 5, gate.bottom, 20):
            pygame.draw.rect(canvas, GOLD, (gate.x + 5, y, gate.width - 10, 5))

def highlight(rect):
    pulse = math.sin(pygame.time.get_ticks() * 0.007)
    thickness = 2 if pulse <= 0 else 3
    outline = rect.inflate(8, 8)

    pygame.draw.rect(canvas, GOLD_LIGHT, outline, thickness, border_radius=5)

    bubble = pygame.Rect(rect.centerx - 11, rect.y - 31, 22, 22)
    pygame.draw.rect(canvas, BLACK, bubble, border_radius=5)
    pygame.draw.rect(canvas, GOLD, bubble, 2, border_radius=5)

    e = small_font.render("E", True, WHITE)
    canvas.blit(e, (bubble.centerx - e.get_width() // 2, bubble.centery - e.get_height() // 2))

def draw_hud():
    if dialogue_active:
        return

    if clue_stage >= 3:
        panel_height = 145
        panel = pygame.Rect(12, 12, 305, panel_height)
        pygame.draw.rect(canvas, BLACK, panel, border_radius=5)
        pygame.draw.rect(canvas, (157, 119, 74), panel, 2, border_radius=5)

        for i, key in enumerate(keys):
            x = 45 + i * 90
            color = key["color"]
            pygame.draw.circle(canvas, color, (x, 40), 8, 3)
            pygame.draw.rect(canvas, color, (x + 5, 37, 18, 5))
            pygame.draw.rect(canvas, color, (x + 17, 41, 5, 6))

            count = small_font.render("1 / 1" if key["collected"] else "0 / 1", True, WHITE)
            canvas.blit(count, (x + 30, 31))

        pygame.draw.line(canvas, (102, 79, 58), (panel.x + 12, 67), (panel.right - 12, 67), 2)

        title = small_font.render("OBJECTIVE", True, GOLD_LIGHT)
        canvas.blit(title, (panel.x + 15, 78))

        if clue_stage == 3:
            objective = ["Find the three keys."]
        elif clue_stage == 4:
            objective = ["Return to the gate."]
        else:
            objective = ["The gate is open."]

        for i, line in enumerate(objective):
            text = small_font.render(line, True, WHITE)
            canvas.blit(text, (panel.x + 15, 100 + i * 19))

    controls = pygame.Rect(760, 12, 188, 76)
    pygame.draw.rect(canvas, BLACK, controls, border_radius=5)
    pygame.draw.rect(canvas, (137, 108, 72), controls, 2, border_radius=5)

    lines = [
        "WASD / Arrows : Move",
        "E : Interact",
        "ESC : Pause Menu"
    ]

    for i, line in enumerate(lines):
        text = small_font.render(line, True, WHITE)
        canvas.blit(text, (controls.x + 12, controls.y + 11 + i * 21))

def draw_dialogue():
    if not dialogue_active:
        return

    panel = pygame.Rect(55, 425, 850, 105)
    pygame.draw.rect(canvas, (3, 4, 5), (panel.x + 4, panel.y + 5, panel.width, panel.height), border_radius=7)
    pygame.draw.rect(canvas, BLACK, panel, border_radius=7)
    pygame.draw.rect(canvas, (159, 120, 75), panel, 3, border_radius=7)

    portrait = pygame.Rect(70, 440, 68, 78)
    pygame.draw.rect(canvas, (25, 28, 32), portrait, border_radius=4)
    pygame.draw.circle(canvas, SKIN, (portrait.centerx, portrait.y + 27), 18)
    pygame.draw.rect(canvas, (75, 50, 32), (portrait.x + 7, portrait.y + 10, 50, 7))
    pygame.draw.rect(canvas, (92, 59, 35), (portrait.x + 19, portrait.y + 1, 30, 12))
    pygame.draw.rect(canvas, NPC_RED, (portrait.x + 12, portrait.y + 45, 44, 32), border_radius=8)

    speaker = small_font.render("STRANGER", True, GOLD_LIGHT)
    canvas.blit(speaker, (160, 438))

    text = current_dialogue[dialogue_index]
    rendered = font.render(text, True, WHITE)
    canvas.blit(rendered, (160, 468))

    key_box = pygame.Rect(732, 491, 22, 22)
    pygame.draw.rect(canvas, VERY_DARK, key_box, border_radius=4)
    pygame.draw.rect(canvas, GOLD, key_box, 2, border_radius=4)

    e_txt = small_font.render("E", True, GOLD_LIGHT)
    canvas.blit(e_txt, (key_box.centerx - e_txt.get_width() // 2, key_box.centery - e_txt.get_height() // 2))

    continue_text = small_font.render("Continue   ▶", True, GREY)
    canvas.blit(continue_text, (760, 495))

def draw_interactions():
    if dialogue_active:
        return

    if near(npc, 42):
        highlight(npc)
        return

    if near(terminal, 42):
        highlight(terminal)
        return

    if near(stone, 42):
        highlight(stone)
        return

    if near(sign, 42):
        highlight(sign)
        return

    if clue_stage >= 3:
        for key in keys:
            if not key["collected"]:
                if player.colliderect(key["rect"].inflate(25, 25)):
                    highlight(key["rect"])
                    return

def draw_pause():
    overlay = pygame.Surface((GAME_WIDTH, GAME_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    canvas.blit(overlay, (0, 0))

    panel = pygame.Rect(GAME_WIDTH // 2 - 200, GAME_HEIGHT // 2 - 130, 400, 260)
    pygame.draw.rect(canvas, BLACK, panel, border_radius=8)
    pygame.draw.rect(canvas, GOLD, panel, 3, border_radius=8)

    draw_centered("PAUSED", panel.y + 30, large_font, WHITE)
    pygame.draw.line(canvas, (102, 79, 58), (panel.x + 30, panel.y + 85), (panel.right - 30, panel.y + 85), 2)

    options = [
        "ESC  —  Resume Game",
        "R  —  Restart Level",
        "ENTER  —  Return to Title Screen"
    ]

    for i, line in enumerate(options):
        text = font.render(line, True, GOLD_LIGHT if i == 1 else WHITE)
        canvas.blit(text, (panel.x + 40, panel.y + 110 + i * 40))

def blocked(rect):
    for tree in trees:
        if rect.colliderect(tree.inflate(5, 5)):
            return True

    for rock in rocks:
        if rect.colliderect(rock):
            return True

    if rect.colliderect(npc):
        return True

    house_parts = [
        pygame.Rect(house.x, house.y, house.width, 18),
        pygame.Rect(house.x, house.y, 18, house.height),
        pygame.Rect(house.right - 18, house.y, 18, house.height),
        pygame.Rect(house.x, house.bottom - 18, house.width, 18)
    ]

    for part in house_parts:
        if rect.colliderect(part) and not rect.colliderect(house_door):
            return True

    for grave in graves:
        if rect.colliderect(grave.inflate(6, 6)):
            return True

    if rect.colliderect(terminal) or rect.colliderect(stone):
        return True

    if not gate_open and rect.colliderect(gate):
        return True

    if rect.left < 0 or rect.top < 0 or rect.right > GAME_WIDTH or rect.bottom > GAME_HEIGHT:
        return True

    return False

def move_player():
    pressed = pygame.key.get_pressed()
    dx = 0
    dy = 0

    if pressed[pygame.K_w] or pressed[pygame.K_UP]:
        dy -= PLAYER_SPEED
    if pressed[pygame.K_s] or pressed[pygame.K_DOWN]:
        dy += PLAYER_SPEED
    if pressed[pygame.K_a] or pressed[pygame.K_LEFT]:
        dx -= PLAYER_SPEED
    if pressed[pygame.K_d] or pressed[pygame.K_RIGHT]:
        dx += PLAYER_SPEED

    player.x += int(dx)
    if blocked(player):
        player.x -= int(dx)

    player.y += int(dy)
    if blocked(player):
        player.y -= int(dy)

def interact():
    global dialogue_active, dialogue_index, current_dialogue
    global clue_stage, game_state, ending_timer

    if dialogue_active:
        dialogue_index += 1
        if dialogue_index >= len(current_dialogue):
            dialogue_active = False
            dialogue_index = 0
            current_dialogue = npc_dialogue
        return

    if near(npc, 45):
        current_dialogue = npc_dialogue
        dialogue_index = 0
        dialogue_active = True
        if clue_stage == 0:
            clue_stage = 1
        return

    if clue_stage >= 3:
        for key in keys:
            if key["collected"]:
                continue
            if player.colliderect(key["rect"].inflate(28, 28)):
                key["collected"] = True
                if collected_count() == 3:
                    clue_stage = 4
                return

    if near(terminal, 45):
        current_dialogue = terminal_dialogue
        dialogue_index = 0
        dialogue_active = True
        if clue_stage < 2:
            clue_stage = 2
        return

    if near(stone, 45):
        current_dialogue = stone_dialogue
        dialogue_index = 0
        dialogue_active = True
        if clue_stage < 3:
            clue_stage = 3
        return

    if near(sign, 45):
        current_dialogue = sign_dialogue
        dialogue_index = 0
        dialogue_active = True
        return

    if gate_open and player.colliderect(exit_zone):
        game_state = ENDING
        ending_timer = 0

def draw_title():
    canvas.fill((7, 13, 11))

    for x in range(0, GAME_WIDTH, 48):
        height = 70 + ((x * 13) % 60)
        pygame.draw.rect(canvas, (10, 25, 18), (x, GAME_HEIGHT - height, 10, height))
        pygame.draw.circle(canvas, (9, 28, 18), (x + 5, GAME_HEIGHT - height), 25)

    pygame.draw.circle(canvas, (201, 190, 150), (780, 105), 38)
    pygame.draw.circle(canvas, (7, 13, 11), (795, 92), 35)

    stars = [
        (90, 75), (160, 125), (260, 65), (365, 110),
        (470, 55), (580, 100), (680, 60), (865, 155),
    ]

    for x, y in stars:
        pygame.draw.circle(canvas, (165, 160, 130), (x, y), 1)

    panel = pygame.Rect(115, 75, 730, 390)
    pygame.draw.rect(canvas, (8, 11, 12), panel, border_radius=8)
    pygame.draw.rect(canvas, (122, 91, 58), panel, 3, border_radius=8)
    pygame.draw.rect(canvas, (57, 49, 42), (panel.x + 8, panel.y + 8, panel.width - 16, panel.height - 16), 1, border_radius=5)

    pygame.draw.line(canvas, GOLD, (275, 150), (685, 150), 2)

    draw_centered("THE LAST LEVEL", 175, huge_font, WHITE)
    draw_centered("A GAME WITHIN A GAME", 245, medium_font, GOLD_LIGHT)
    draw_centered("Some things are meant to be found.", 300, small_font, GREY)
    draw_centered("Others are meant to be entered.", 325, small_font, GREY)

    button = pygame.Rect(345, 370, 270, 55)
    pulse = (math.sin(pygame.time.get_ticks() * 0.003) + 1) * 2
    pygame.draw.rect(canvas, (40, 31, 21), button.inflate(int(pulse), int(pulse)), border_radius=6)
    pygame.draw.rect(canvas, GOLD, button, 2, border_radius=6)

    start = medium_font.render("ENTER  —  BEGIN", True, WHITE)
    canvas.blit(start, (button.centerx - start.get_width() // 2, button.centery - start.get_height() // 2))

    draw_centered("WASD / ARROWS • MOVE | THE BEGINNING RESPONDS TO THE ANCIENT KEY", 495, small_font, GREY)

def draw_ending():
    canvas.fill(BLACK)
    for radius in range(200, 20, -20):
        alpha = max(0, 30 - radius // 8)
        surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT), pygame.SRCALPHA)
        pygame.draw.circle(surface, (90, 70, 35, alpha), (GAME_WIDTH // 2, 220), radius)
        canvas.blit(surface, (0, 0))

    if ending_timer < 120:
        draw_centered("YOU WIN!", 170, huge_font, WHITE)
    elif ending_timer < 240:
        draw_centered("YOU WIN!", 125, huge_font, WHITE)
        draw_centered("...", 225, medium_font, GREY)
    else:
        draw_centered("YOU WIN!", 100, huge_font, WHITE)
        pygame.draw.line(canvas, (90, 75, 55), (270, 200), (690, 200), 1)
        draw_centered("BUT YOU DIDN'T FIND IT.", 245, medium_font, WHITE)
        draw_centered("Something is still hidden.", 295, small_font, GREY)
        draw_centered("R  —  RESTART GAME", 385, medium_font, GOLD_LIGHT)
        draw_centered("ENTER  —  RETURN TO TITLE", 430, small_font, GREY)

def draw_secret():
    canvas.fill(BLACK)
    glow = pygame.Surface((GAME_WIDTH, GAME_HEIGHT), pygame.SRCALPHA)
    pygame.draw.circle(glow, (85, 45, 120, 25), (GAME_WIDTH // 2, 210), 180)
    canvas.blit(glow, (0, 0))

    y = 75
    for line in secret_message:
        if line == "YOU FOUND IT.":
            used_font, color = huge_font, PURPLE
        elif line == "YOUR NEXT CLUE:":
            used_font, color = medium_font, GOLD_LIGHT
        else:
            used_font, color = small_font, WHITE

        draw_centered(line, y, used_font, color)
        y += 55

    draw_centered("ENTER  —  RESTART", 475, small_font, GREY)

def draw_atmosphere():
    overlay = pygame.Surface((GAME_WIDTH, GAME_HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(overlay, (0, 0, 0, 22), (0, 0, GAME_WIDTH, 65))
    pygame.draw.rect(overlay, (0, 0, 0, 30), (0, GAME_HEIGHT - 70, GAME_WIDTH, 70))
    pygame.draw.rect(overlay, (0, 0, 0, 20), (0, 0, 35, GAME_HEIGHT))
    pygame.draw.rect(overlay, (0, 0, 0, 20), (GAME_WIDTH - 35, 0, 35, GAME_HEIGHT))
    canvas.blit(overlay, (0, 0))

def check_konami(event):
    global konami_progress, game_state

    if event.type != pygame.KEYDOWN or game_state != TITLE:
        return

    konami_progress.append(event.key)
    if len(konami_progress) > len(KONAMI_CODE):
        konami_progress.pop(0)

    if konami_progress == KONAMI_CODE:
        konami_progress = []
        if collected_count() == 3:
            game_state = SECRET

# ============================================================
# ASYNC MAIN LOOP (WEB COMPATIBLE)
# ============================================================
async def main():
    global game_state, ending_timer, gate_open, clue_stage

    running = True

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            check_konami(event)

            if game_state == TITLE:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    reset_game()

            elif game_state == PLAYING:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        interact()
                    elif event.key == pygame.K_ESCAPE:
                        game_state = PAUSED

            elif game_state == PAUSED:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_state = PLAYING
                    elif event.key == pygame.K_r:
                        reset_game()
                    elif event.key == pygame.K_RETURN:
                        game_state = TITLE

            elif game_state == ENDING:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        reset_game()
                    elif event.key == pygame.K_RETURN:
                        game_state = TITLE

            elif game_state == SECRET:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    reset_game()

        if game_state == PLAYING:
            if not dialogue_active:
                move_player()

            if collected_count() == 3 and not gate_open:
                gate_open = True
                clue_stage = 5

            if gate_open and player.colliderect(exit_zone):
                game_state = ENDING
                ending_timer = 0

        if game_state == ENDING:
            ending_timer += 1

        if game_state == TITLE:
            draw_title()

        elif game_state in (PLAYING, PAUSED):
            draw_background()
            draw_paths()
            draw_pond()

            for tree in trees:
                draw_tree(tree)

            draw_rocks()
            draw_graveyard()
            draw_fences()
            draw_house()
            draw_flowers()

            for x, y in lanterns:
                draw_lantern(x, y)

            draw_terminal()
            draw_stone()
            draw_sign()
            draw_gate()

            for key in keys:
                draw_key(key)

            draw_npc()
            draw_player()
            draw_atmosphere()
            draw_hud()
            draw_interactions()
            draw_dialogue()

            if game_state == PAUSED:
                draw_pause()

        elif game_state == ENDING:
            draw_ending()

        elif game_state == SECRET:
            draw_secret()

        scaled_surface = pygame.transform.scale(canvas, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(scaled_surface, (0, 0))
        pygame.display.flip()

        # Critical step: allow browser event loop to process
        await asyncio.sleep(0)

    pygame.quit()
    sys.exit()

# Run the async main function
asyncio.run(main())
