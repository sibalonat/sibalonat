"""
Bauhaus "Triadic Balloon" — A Daily Journey

A geometric balloon traverses a 1200x300 stage from left to right
over 24 hours, telling a daily story in three acts.

Inspired by:
  - Paul Klee, "Red Balloon" (1922) — balloon over geometric city
  - Oskar Schlemmer, "Triadic Ballet" (1922) — three-act color structure
  - Lyonel Feininger, "Cathedral of Socialism" (1919) — angular cityscape
  - Herbert Bayer, Universal typeface (1925) — geometric letterforms
  - Wassily Kandinsky, color theory (1923) — primary color assignments

Acts (after Schlemmer):
  I   Yellow  (Hours 0–7)   Dawn  — balloon enters from left, small
  II  Red     (Hours 8–15)  Day   — balloon at center, largest
  III Blue    (Hours 16–22) Dusk  — balloon recedes right, shrinking
  IV  Black   (Hour 23)     Night — mn+ signature revealed
"""

import math
import random
from datetime import datetime
from PIL import Image, ImageDraw


# ── Bauhaus primary palette ──────────────────────────────────────────────────

YELLOW = (255, 209, 0)
RED    = (237, 41, 57)
BLUE   = (0, 82, 180)
BLACK  = (0, 0, 0)
WHITE  = (255, 255, 255)

# ── Act palettes (Schlemmer's Triadic Ballet) ────────────────────────────────

ACTS = {
    'yellow': {
        'bg':        (248, 243, 228),    # warm parchment
        'sky':       (252, 240, 195),    # golden haze
        'city_base': (175, 155, 120),    # warm sandstone
        'city_accent': YELLOW,
        'balloon_top': YELLOW,
        'balloon_bot': RED,
        'accent':    BLUE,
        'divider':   (200, 180, 140),
    },
    'red': {
        'bg':        (248, 242, 238),    # warm white
        'sky':       (248, 228, 218),    # warm blush
        'city_base': (155, 140, 130),    # warm gray
        'city_accent': RED,
        'balloon_top': RED,
        'balloon_bot': BLUE,
        'accent':    YELLOW,
        'divider':   (185, 165, 155),
    },
    'blue': {
        'bg':        (228, 235, 248),    # cool lavender
        'sky':       (195, 212, 240),    # twilight blue
        'city_base': (105, 115, 145),    # cool slate
        'city_accent': BLUE,
        'balloon_top': BLUE,
        'balloon_bot': YELLOW,
        'accent':    RED,
        'divider':   (140, 150, 180),
    },
    'black': {
        'bg':        (35, 35, 42),       # near-black
        'sky':       (25, 25, 32),       # deep night
        'city_base': (65, 65, 78),       # charcoal
        'city_accent': WHITE,
        'balloon_top': WHITE,
        'balloon_bot': RED,
        'accent':    YELLOW,
        'divider':   (50, 50, 60),
    },
}


# ── Act resolution ───────────────────────────────────────────────────────────

def get_act(hour):
    """Map hour (0-23) to a Triadic Ballet act."""
    if hour <= 7:
        return 'yellow'
    if hour <= 15:
        return 'red'
    if hour <= 22:
        return 'blue'
    return 'black'


# ── Position & perspective ───────────────────────────────────────────────────

def get_balloon_position(hour, width=1200, height=300):
    """
    Compute balloon center-x, top-y, and scale for a given hour.

    Scale follows a sine arch: small at edges (distant),
    largest at center (closest to the viewer).
    Vertical position oscillates gently (wind).
    """
    progress = hour / 23.0                      # 0.0 → 1.0

    # Horizontal: linear left-to-right
    margin = 130
    x = margin + (width - 2 * margin) * progress

    # Scale: sine arch  0.45 at edges → 1.0 at midpoint
    scale = 0.45 + 0.55 * math.sin(math.pi * progress)

    # Vertical: base position + wind oscillation + perspective shift
    y_base = 55
    y_wind = 15 * math.sin(2 * math.pi * hour / 8)
    y_perspective = (1.0 - scale) * (-12)       # smaller → floats higher
    y = y_base + y_wind + y_perspective

    return x, y, scale


# ── Drawing: background ─────────────────────────────────────────────────────

def draw_background(draw, width, height, act):
    """Two-tone background with a thin Bauhaus divider line."""
    third = height // 3
    draw.rectangle([0, 0, width, third], fill=act['sky'])
    draw.rectangle([0, third, width, height], fill=act['bg'])
    # thin horizontal rule (the Bauhaus loves a clean datum line)
    draw.rectangle([0, third - 1, width, third + 1], fill=act['divider'])


# ── Drawing: cityscape ──────────────────────────────────────────────────────

def _building_color(base, rng, variance=25):
    """Return a color near `base` with random variance."""
    return tuple(
        max(0, min(255, c + rng.randint(-variance, variance)))
        for c in base
    )


def _muted(color, base):
    """Blend a color halfway toward a base."""
    return tuple((a + b) // 2 for a, b in zip(color, base))


def draw_cityscape(draw, width, height, day_seed, act):
    """
    Feininger-inspired geometric skyline along the bottom ~80 px.
    Seeded by day-of-year so it stays consistent within a single day.
    """
    rng = random.Random(day_seed)
    ground_h = 22
    city_floor = height - ground_h
    base = act['city_base']

    # ground plane
    draw.rectangle([0, city_floor, width, height], fill=base)

    # buildings — back layer (tall, lighter)
    buildings_back = []
    for _ in range(rng.randint(10, 16)):
        bw = rng.randint(30, 70)
        bh = rng.randint(45, 80)
        bx = rng.randint(0, width - bw)
        color = _building_color(base, rng, variance=18)
        buildings_back.append((bx, city_floor - bh, bx + bw, city_floor, color))

    for b in buildings_back:
        draw.rectangle([b[0], b[1], b[2], b[3]], fill=b[4], outline=BLACK, width=1)

    # buildings — front layer (shorter, darker)
    for _ in range(rng.randint(8, 14)):
        bw = rng.randint(20, 55)
        bh = rng.randint(25, 55)
        bx = rng.randint(0, width - bw)
        color = _building_color(base, rng, variance=12)
        draw.rectangle(
            [bx, city_floor - bh, bx + bw, city_floor],
            fill=color, outline=BLACK, width=1,
        )

    # accent spires — tall, narrow, in the act's primary color (muted)
    accent_muted = _muted(act['city_accent'], base)
    for _ in range(rng.randint(2, 4)):
        sw = rng.randint(8, 18)
        sh = rng.randint(55, 85)
        sx = rng.randint(0, width - sw)
        draw.rectangle(
            [sx, city_floor - sh, sx + sw, city_floor],
            fill=accent_muted, outline=BLACK, width=1,
        )


# ── Drawing: diamond balloon ────────────────────────────────────────────────

def draw_balloon(draw, x, y, scale, act):
    """
    Bauhaus diamond / kite balloon.

    The envelope is a diamond built from horizontal rectangles:
    upper half in one primary, lower half in another
    (Kandinsky: warm rises, cool descends).
    A small accent square sits at the equator.
    A string leads down to a rectangular basket.
    """
    top_color = act['balloon_top']
    bot_color = act['balloon_bot']
    acc_color = act['accent']

    half_w = int(38 * scale)
    half_h = int(48 * scale)
    cx = int(x)
    cy = int(y + half_h)                   # equator of the diamond

    rows_per_half = max(4, int(8 * scale))
    row_h = max(2, int(half_h / rows_per_half))

    # ── upper half (tapers up) ──
    for i in range(rows_per_half):
        frac = (i + 1) / rows_per_half
        rw = max(2, int(half_w * frac))
        ry = cy - half_h + i * row_h
        draw.rectangle(
            [cx - rw, ry, cx + rw, ry + row_h],
            fill=top_color, outline=BLACK, width=1,
        )

    # ── lower half (tapers down) ──
    for i in range(rows_per_half):
        frac = max(0.08, 1.0 - (i + 1) / rows_per_half)
        rw = max(2, int(half_w * frac))
        ry = cy + i * row_h
        draw.rectangle(
            [cx - rw, ry, cx + rw, ry + row_h],
            fill=bot_color, outline=BLACK, width=1,
        )

    # ── accent square at equator ──
    a = max(3, int(8 * scale))
    draw.rectangle(
        [cx - a, cy - a, cx + a, cy + a],
        fill=acc_color, outline=BLACK, width=1,
    )

    # ── string ──
    string_top = cy + half_h
    string_len = max(10, int(22 * scale))
    draw.rectangle([cx, string_top, cx + 1, string_top + string_len], fill=BLACK)

    # ── basket ──
    bw = max(5, int(12 * scale))
    bh = max(3, int(6 * scale))
    by = string_top + string_len
    draw.rectangle(
        [cx - bw // 2, by, cx + bw // 2, by + bh],
        fill=BLACK, outline=BLACK, width=1,
    )


# ── Drawing: mn+ signature ──────────────────────────────────────────────────

def draw_mnplus(draw, width, height, act):
    """
    Herbert Bayer–style geometric "mn+" for the finale frame.
    Positioned left-of-center so the arrived balloon can sit at the right.
    """
    fg = act['balloon_top']       # WHITE on the black finale
    plus_fg = act['accent']       # YELLOW accent for the +

    # ── metrics ──
    cx = width // 3               # left-center anchor
    cy = height // 2 - 15
    bar = 10                      # stroke thickness
    lh  = 90                      # letter height
    lw  = 55                      # letter width
    gap = 22                      # spacing between letters

    sx = cx - (lw * 3 + gap * 2) // 2   # starting x

    top = cy - lh // 2
    bot = cy + lh // 2

    # ── M ──
    mx = sx
    # left stem
    draw.rectangle([mx, top, mx + bar, bot], fill=fg, outline=BLACK, width=1)
    # right stem
    draw.rectangle([mx + lw - bar, top, mx + lw, bot], fill=fg, outline=BLACK, width=1)
    # left shoulder
    draw.rectangle(
        [mx + bar, top, mx + lw // 2, top + lh // 3],
        fill=fg, outline=BLACK, width=1,
    )
    # right shoulder
    draw.rectangle(
        [mx + lw // 2, top, mx + lw - bar, top + lh // 3],
        fill=fg, outline=BLACK, width=1,
    )
    # center descender (the V peak)
    draw.rectangle(
        [mx + lw // 2 - bar // 2, top + lh // 6,
         mx + lw // 2 + bar // 2, top + lh // 2],
        fill=fg, outline=BLACK, width=1,
    )

    # ── N ──
    nx = mx + lw + gap
    # left stem
    draw.rectangle([nx, top, nx + bar, bot], fill=fg, outline=BLACK, width=1)
    # right stem
    draw.rectangle([nx + lw - bar, top, nx + lw, bot], fill=fg, outline=BLACK, width=1)
    # diagonal bridge (approximated with a thick bar)
    draw.rectangle(
        [nx + bar, top + lh // 6, nx + lw - bar, top + lh // 6 + bar * 2],
        fill=fg, outline=BLACK, width=1,
    )

    # ── + ──
    px = nx + lw + gap
    plus_size = lh * 2 // 3
    pcx = px + lw // 2
    # vertical bar
    draw.rectangle(
        [pcx - bar // 2, cy - plus_size // 2,
         pcx + bar // 2, cy + plus_size // 2],
        fill=plus_fg, outline=BLACK, width=1,
    )
    # horizontal bar
    draw.rectangle(
        [pcx - plus_size // 2, cy - bar // 2,
         pcx + plus_size // 2, cy + bar // 2],
        fill=plus_fg, outline=BLACK, width=1,
    )


# ── Drawing: geometric accents ──────────────────────────────────────────────

def draw_accents(draw, width, height, hour, act):
    """
    Small Kandinsky-esque geometric markers in the sky.
    Deterministic (seeded by hour) so each frame has consistent accents.
    """
    rng = random.Random(hour * 137 + 59)

    # 2-3 small squares in the upper part of the canvas
    for _ in range(rng.randint(2, 3)):
        s = rng.randint(6, 14)
        ax = rng.randint(40, width - 40)
        ay = rng.randint(15, height // 3 - 20)
        color = rng.choice([act['city_accent'], act['accent'], act['divider']])
        draw.rectangle([ax, ay, ax + s, ay + s], fill=color, outline=BLACK, width=1)


# ── Frame generation ─────────────────────────────────────────────────────────

def generate_triadic_frame(hour=None, day_seed=None, width=1200, height=300):
    """
    Generate a single frame of the Triadic Balloon journey.

    Args:
        hour:     Current hour 0-23.  None → datetime.now().hour
        day_seed: Seed for the cityscape.  None → day-of-year
        width:    Image width  (default 1200)
        height:   Image height (default 300)

    Returns:
        PIL.Image.Image
    """
    if hour is None:
        hour = datetime.now().hour
    if day_seed is None:
        day_seed = datetime.now().timetuple().tm_yday

    act_name = get_act(hour)
    act = ACTS[act_name]

    img = Image.new('RGB', (width, height), act['bg'])
    draw = ImageDraw.Draw(img)

    # 1 — background & datum line
    draw_background(draw, width, height, act)

    # 2 — geometric accents (behind the balloon)
    draw_accents(draw, width, height, hour, act)

    # 3 — cityscape (consistent within the day)
    draw_cityscape(draw, width, height, day_seed, act)

    # 4 — balloon (or finale)
    x, y, scale = get_balloon_position(hour, width, height)
    if hour == 23:
        # finale: small balloon at far right + mn+ signature
        draw_balloon(draw, x, y, scale * 0.55, act)
        draw_mnplus(draw, width, height, act)
    else:
        draw_balloon(draw, x, y, scale, act)

    return img


# ── Backward-compatible entry point ─────────────────────────────────────────

def generate_image(theme='triadic', width=1200, height=300, seed=None,
                   hour=None, day_seed=None):
    """
    Public API.  Now delegates to the triadic frame generator.
    The `theme` and `seed` args are kept for backward compat but ignored.
    """
    return generate_triadic_frame(
        hour=hour, day_seed=day_seed, width=width, height=height,
    )


# ── CLI ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    import os
    out = 'test_frames'
    os.makedirs(out, exist_ok=True)
    for h in range(24):
        img = generate_triadic_frame(hour=h, day_seed=42)
        img.save(f'{out}/frame_{h:02d}.png')
        print(f'frame {h:02d}  act={get_act(h)}')
    print(f'\nSaved 24 frames to {out}/')
