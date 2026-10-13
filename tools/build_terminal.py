from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import random

# ============================================================
# RK // TERMINAL ANIMATION
# ============================================================

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

GIF_PATH = ASSETS / "rk-terminal-header.gif"
PREVIEW_PATH = ASSETS / "rk-terminal-preview.png"

WIDTH = 1000
HEIGHT = 360

BACKGROUND = (5, 9, 8)
PANEL = (9, 15, 12)
GREEN = (57, 255, 122)
DIM_GREEN = (27, 125, 67)
MUTED = (105, 151, 119)
WHITE = (202, 224, 207)
RED = (255, 91, 91)
YELLOW = (255, 201, 91)
BLUE = (91, 190, 255)

# Compact typography ensures every scene fits.
FONT_SIZE = 14
LINE_HEIGHT = 20

LEFT = 30
TOP = 56

HOLD_FRAMES = 8

random.seed(17)

# ============================================================
# FONTS
# ============================================================

def load_font(size):
    candidates = [
        "C:/Windows/Fonts/CascadiaMono.ttf",
        "C:/Windows/Fonts/consola.ttf",
        "C:/Windows/Fonts/lucon.ttf",
        "C:/Windows/Fonts/cour.ttf",
    ]

    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)

    return ImageFont.load_default()


FONT = load_font(FONT_SIZE)
SMALL_FONT = load_font(11)
BOLD_FONT = load_font(15)

# ============================================================
# TERMINAL SCENES
# ============================================================

SCENES = [
    [
        ("rk@github:~$ whoami", GREEN),
        ("RK", WHITE),
        ("Independent trading-technology builder", MUTED),
        ("", GREEN),
        ("rk@github:~$ cat /etc/mission", GREEN),
        ("Understand the markets.", WHITE),
        ("Build the technology.", WHITE),
        ("Grow toward the enterprise.", WHITE),
        ("", GREEN),
        ("[ SYSTEM ]  Curiosity -> Research -> Engineering", DIM_GREEN),
    ],
    [
        ("rk@github:~$ systemctl status current-work", GREEN),
        ("", GREEN),
        ("trading-technology.service", WHITE),
        ("   Loaded: active (development)", MUTED),
        ("   State:  researching and building", GREEN),
        ("", GREEN),
        ("systems-engineering.service", WHITE),
        ("   Loaded: active (development)", MUTED),
        ("   State:  testing and refining", GREEN),
        ("", GREEN),
        ("security-discipline.service", WHITE),
        ("   State:  hardening and verification", GREEN),
    ],
    [
        ("rk@github:~$ tree -L 1 ~/work", GREEN),
        ("", GREEN),
        ("~/work", WHITE),
        ("|-- trading-technology/", MUTED),
        ("|-- systems-engineering/", MUTED),
        ("|-- security-research/", MUTED),
        ("|-- knowledge-systems/", MUTED),
        ("`-- experiments/", MUTED),
        ("", GREEN),
        ("rk@github:~$ git status --short", GREEN),
        (" M  research-notes.md", YELLOW),
        ("?? experiments/", BLUE),
    ],
    [
        ("rk@github:~$ python market_structure.py", GREEN),
        ("", GREEN),
        ("[INIT] Loading market data...", MUTED),
        ("[SCAN] Detecting structural swings...", MUTED),
        ("[SCAN] Mapping liquidity references...", MUTED),
        ("[TEST] Validating structural conditions...", MUTED),
        ("", GREEN),
        ("Research status: IN PROGRESS", YELLOW),
        ("No signal accepted without verification.", WHITE),
        ("", GREEN),
        ("rk@github:~$ cat /etc/philosophy", GREEN),
        ("Build deliberately. Test rigorously.", WHITE),
    ],
]

# ============================================================
# BACKGROUND AND WINDOW
# ============================================================

def draw_background():
    image = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
    draw = ImageDraw.Draw(image)

    # Main terminal frame
    draw.rounded_rectangle(
        (8, 8, WIDTH - 8, HEIGHT - 8),
        radius=10,
        fill=PANEL,
        outline=(35, 61, 43),
        width=1,
    )

    # Title bar
    draw.rounded_rectangle(
        (9, 9, WIDTH - 9, 43),
        radius=9,
        fill=(15, 23, 18),
    )

    draw.rectangle(
        (9, 30, WIDTH - 9, 43),
        fill=(15, 23, 18),
    )

    draw.ellipse((23, 21, 33, 31), fill=RED)
    draw.ellipse((41, 21, 51, 31), fill=YELLOW)
    draw.ellipse((59, 21, 69, 31), fill=GREEN)

    title = "rk@github — terminal"
    title_width = draw.textlength(title, font=SMALL_FONT)

    draw.text(
        ((WIDTH - title_width) / 2, 18),
        title,
        font=SMALL_FONT,
        fill=MUTED,
    )

    # Right-side system trace
    panel_x = 755

    draw.line(
        (panel_x, 55, panel_x, HEIGHT - 25),
        fill=(27, 52, 35),
        width=1,
    )

    draw.text(
        (panel_x + 20, 66),
        "SYSTEM TRACE",
        font=SMALL_FONT,
        fill=DIM_GREEN,
    )

    trace_items = [
        ("IDENTITY", "RK"),
        ("MODE", "BUILD"),
        ("FOCUS", "MARKETS"),
        ("METHOD", "VERIFY"),
        ("STATUS", "ACTIVE"),
    ]

    y = 100

    for label, value in trace_items:
        draw.text(
            (panel_x + 20, y),
            label,
            font=SMALL_FONT,
            fill=MUTED,
        )

        draw.text(
            (panel_x + 20, y + 17),
            value,
            font=SMALL_FONT,
            fill=GREEN,
        )

        y += 43

    # Subtle scanlines
    for scan_y in range(48, HEIGHT - 10, 4):
        draw.line(
            (15, scan_y, WIDTH - 15, scan_y),
            fill=(9, 18, 12),
            width=1,
        )

    # Restore the divider above the scanlines
    draw.line(
        (panel_x, 55, panel_x, HEIGHT - 25),
        fill=(27, 52, 35),
        width=1,
    )

    return image


# ============================================================
# RENDER A SINGLE FRAME
# ============================================================

def render_scene(scene, reveal_count, cursor_visible=True):
    image = draw_background()
    draw = ImageDraw.Draw(image)

    # Reserve the lower section for the status bar.
    status_line_y = HEIGHT - 35
    content_bottom = status_line_y - 12

    # Calculate the available vertical space.
    available_height = content_bottom - TOP
    max_visible_lines = available_height // LINE_HEIGHT

    # All current scenes fit without overlapping the footer.
    visible_scene = scene[:max_visible_lines]

    consumed = 0
    cursor_x = LEFT
    cursor_y = TOP
    cursor_placed = False

    for line_index, (line, color) in enumerate(visible_scene):
        y = TOP + line_index * LINE_HEIGHT

        # Defensive boundary check.
        if y + LINE_HEIGHT > content_bottom:
            break

        characters_remaining = max(0, reveal_count - consumed)
        visible_characters = min(len(line), characters_remaining)
        visible_text = line[:visible_characters]

        if visible_text:
            draw.text(
                (LEFT, y),
                visible_text,
                font=FONT,
                fill=color,
            )

        # Place the cursor at the current typing position.
        if (
            not cursor_placed
            and len(line) > 0
            and reveal_count <= consumed + len(line)
        ):
            cursor_x = LEFT + draw.textlength(
                visible_text,
                font=FONT,
            )

            cursor_y = y
            cursor_placed = True

        consumed += len(line)

    # Blinking typing cursor
    if cursor_visible and cursor_placed:
        draw.rectangle(
            (
                int(cursor_x + 2),
                cursor_y + 2,
                int(cursor_x + 9),
                cursor_y + FONT_SIZE + 2,
            ),
            fill=GREEN,
        )

    # Fixed status bar, always below the terminal text.
    draw.line(
        (LEFT, status_line_y - 6, WIDTH - 30, status_line_y - 6),
        fill=(26, 49, 33),
        width=1,
    )

    draw.text(
        (LEFT, status_line_y),
        "RK // INDEPENDENT TRADING-TECHNOLOGY BUILDER",
        font=SMALL_FONT,
        fill=DIM_GREEN,
    )

    draw.text(
        (WIDTH - 175, status_line_y),
        "SESSION: ACTIVE",
        font=SMALL_FONT,
        fill=GREEN,
    )

    return image


# ============================================================
# HUMAN-SPEED TYPING
# ============================================================

def typing_delay(scene, reveal_count):
    characters = [
        character
        for line, _ in scene
        for character in line
    ]

    # Variable base speed instead of mechanical uniform typing.
    delay = random.randint(115, 210)

    if reveal_count <= 0 or reveal_count > len(characters):
        return delay

    char = characters[reveal_count - 1]

    # Brief pauses between words.
    if char == " ":
        delay += random.randint(35, 100)

    # Natural punctuation pauses.
    if char in ",;:":
        delay += random.randint(130, 250)

    elif char in ".!?":
        delay += random.randint(180, 350)

    # Small variation around symbols and paths.
    elif char in ">/[]()":
        delay += random.randint(20, 80)

    # Pause at the end of a completed line.
    position = 0

    for line, _ in scene:
        position += len(line)

        if line and position == reveal_count:
            delay += random.randint(220, 500)
            break

    # Occasional thinking pause.
    if random.random() < 0.035:
        delay += random.randint(250, 650)

    return delay


# ============================================================
# BUILD THE ANIMATION
# ============================================================

def build_animation():
    frames = []
    durations = []
    preview = None

    for scene_index, scene in enumerate(SCENES):
        total_characters = sum(
            len(line)
            for line, _ in scene
        )

        # Reveal one character per frame.
        for reveal_count in range(1, total_characters + 1):
            cursor_visible = reveal_count % 2 == 0

            frame = render_scene(
                scene,
                reveal_count,
                cursor_visible,
            )

            frames.append(frame)
            durations.append(
                typing_delay(scene, reveal_count)
            )

        # Save a still preview of the completed opening scene.
        if scene_index == 0:
            preview = render_scene(
                scene,
                total_characters,
                True,
            )

        # Hold the completed scene while the cursor blinks.
        for hold_index in range(HOLD_FRAMES):
            frames.append(
                render_scene(
                    scene,
                    total_characters,
                    hold_index % 2 == 0,
                )
            )

            durations.append(220)

    # Reduce the color palette to keep the GIF manageable.
    quantized_frames = [
        frame.quantize(
            colors=64,
            method=Image.Quantize.MEDIANCUT,
            dither=Image.Dither.NONE,
        )
        for frame in frames
    ]

    quantized_frames[0].save(
        GIF_PATH,
        save_all=True,
        append_images=quantized_frames[1:],
        duration=durations,
        loop=0,
        optimize=True,
        disposal=1,
    )

    if preview is not None:
        preview.save(PREVIEW_PATH)

    print()
    print("==========================================")
    print(" RK // TERMINAL ANIMATION")
    print("==========================================")
    print(f"GIF:      {GIF_PATH}")
    print(f"Preview:  {PREVIEW_PATH}")
    print(f"Frames:   {len(frames)}")
    print(f"Duration: {sum(durations) / 1000:.1f} seconds per loop")
    print(f"Size:     {GIF_PATH.stat().st_size / 1024:.1f} KB")
    print()
    print("Build complete.")
    print("All scenes rendered within the terminal layout.")
    print("==========================================")


if __name__ == "__main__":
    ASSETS.mkdir(parents=True, exist_ok=True)
    build_animation()