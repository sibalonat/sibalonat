"""
Bauhaus-style image generator for balloon and mnpluss themes.
"""
import random
from PIL import Image, ImageDraw


# Bauhaus color palette
BAUHAUS_COLORS = [
    (255, 209, 0),    # Yellow
    (237, 41, 57),    # Red
    (0, 82, 180),     # Blue
    (0, 0, 0),        # Black
    (255, 255, 255),  # White
]

SECONDARY_COLORS = [
    (255, 128, 0),    # Orange
    (102, 51, 153),   # Purple
    (0, 128, 0),      # Green
]


def create_bauhaus_balloon(width=1200, height=300, seed=None):
    """
    Generate a Bauhaus-style balloon made entirely of rectangles.
    """
    if seed:
        random.seed(seed)
    
    # Create clean background
    bg_color = random.choice(BAUHAUS_COLORS)
    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Choose balloon style randomly
    balloon_style = random.choice(['composed', 'stacked', 'grid'])
    
    # Position balloon
    balloon_x = width // 2 + random.randint(-150, 150)
    balloon_y = 100
    
    balloon_color = random.choice([c for c in BAUHAUS_COLORS if c != bg_color])
    accent_color = random.choice([c for c in BAUHAUS_COLORS if c not in [bg_color, balloon_color]])
    
    if balloon_style == 'composed':
        # Balloon made of symmetric rectangles forming oval shape
        # Center vertical rectangles
        for i in range(5):
            w = 15 + (2 - abs(2 - i)) * 15  # Wider in middle
            h = 25
            y = balloon_y + i * 22
            draw.rectangle(
                [balloon_x - w, y, balloon_x + w, y + h],
                fill=balloon_color,
                outline=(0, 0, 0),
                width=2
            )
        
        # Side rectangles for width
        for i in range(3):
            w = 12
            h = 20
            y = balloon_y + 25 + i * 22
            offset = 35 - i * 5
            # Left side
            draw.rectangle(
                [balloon_x - offset - w, y, balloon_x - offset + w, y + h],
                fill=balloon_color,
                outline=(0, 0, 0),
                width=2
            )
            # Right side (mirror)
            draw.rectangle(
                [balloon_x + offset - w, y, balloon_x + offset + w, y + h],
                fill=balloon_color,
                outline=(0, 0, 0),
                width=2
            )
    
    elif balloon_style == 'stacked':
        # Balloon made of stacked horizontal rectangles
        widths = [30, 50, 60, 60, 50, 30]  # Balloon shape
        for i, w in enumerate(widths):
            h = 18
            y = balloon_y + i * 20
            draw.rectangle(
                [balloon_x - w, y, balloon_x + w, y + h],
                fill=balloon_color,
                outline=(0, 0, 0),
                width=2
            )
        
        # Accent rectangle
        draw.rectangle(
            [balloon_x - 20, balloon_y + 50, balloon_x + 20, balloon_y + 70],
            fill=accent_color,
            outline=(0, 0, 0),
            width=2
        )
    
    else:  # grid
        # Balloon made of small grid rectangles
        grid_size = 15
        rows = 7
        cols = 5
        for row in range(rows):
            for col in range(cols):
                # Create oval shape with grid
                distance_from_center = abs(col - 2) / 2 + abs(row - 3) / 3
                if distance_from_center < 1.5:
                    x = balloon_x - 30 + col * grid_size
                    y = balloon_y + row * grid_size
                    # Alternate colors for some variety
                    color = balloon_color if (row + col) % 3 != 0 else accent_color
                    draw.rectangle(
                        [x, y, x + grid_size - 2, y + grid_size - 2],
                        fill=color,
                        outline=(0, 0, 0),
                        width=1
                    )
    
    # String - thin vertical rectangle
    string_y = balloon_y + 130
    draw.rectangle(
        [balloon_x - 2, string_y, balloon_x + 2, height - 30],
        fill=(0, 0, 0),
        outline=None
    )
    
    # Add 1-2 small decorative rectangles
    for _ in range(random.randint(1, 2)):
        color = random.choice([c for c in BAUHAUS_COLORS + SECONDARY_COLORS if c != bg_color])
        w = random.randint(25, 45)
        h = random.randint(15, 35)
        
        if random.choice([True, False]):
            x = random.randint(80, width // 4)
        else:
            x = random.randint(3 * width // 4, width - 80)
        y = random.randint(50, height - 80)
        
        draw.rectangle([x, y, x + w, y + h], 
                      fill=color, outline=(0, 0, 0), width=2)
    
    return img


def create_bauhaus_mnpluss(width=1200, height=300, seed=None):
    """
    Generate "mn+" signature using only rectangles in Bauhaus style.
    """
    if seed:
        random.seed(seed)
    
    # Create clean background
    bg_color = random.choice(BAUHAUS_COLORS)
    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Choose colors
    letter_color = random.choice([c for c in BAUHAUS_COLORS if c != bg_color])
    plus_color = random.choice([c for c in BAUHAUS_COLORS if c not in [bg_color, letter_color]])
    
    # Choose style variation
    style = random.choice(['solid', 'stacked', 'outlined'])
    
    center_x = width // 2
    center_y = height // 2
    
    # Starting position for letters
    start_x = center_x - 200
    
    if style == 'solid':
        # M - two vertical rectangles with connecting top
        # Left vertical
        draw.rectangle([start_x, center_y - 80, start_x + 25, center_y + 80],
                      fill=letter_color, outline=(0, 0, 0), width=2)
        # Right vertical
        draw.rectangle([start_x + 75, center_y - 80, start_x + 100, center_y + 80],
                      fill=letter_color, outline=(0, 0, 0), width=2)
        # Top connecting diagonal (made with angled rectangles)
        draw.rectangle([start_x + 25, center_y - 80, start_x + 50, center_y - 30],
                      fill=letter_color, outline=(0, 0, 0), width=2)
        draw.rectangle([start_x + 50, center_y - 80, start_x + 75, center_y - 30],
                      fill=letter_color, outline=(0, 0, 0), width=2)
        
        # N - two verticals with diagonal
        n_start = start_x + 130
        draw.rectangle([n_start, center_y - 80, n_start + 25, center_y + 80],
                      fill=letter_color, outline=(0, 0, 0), width=2)
        draw.rectangle([n_start + 75, center_y - 80, n_start + 100, center_y + 80],
                      fill=letter_color, outline=(0, 0, 0), width=2)
        # Diagonal bridge
        draw.rectangle([n_start + 20, center_y - 40, n_start + 80, center_y - 10],
                      fill=letter_color, outline=(0, 0, 0), width=2)
        
        # + symbol
        plus_start = n_start + 150
        # Vertical
        draw.rectangle([plus_start + 30, center_y - 60, plus_start + 50, center_y + 60],
                      fill=plus_color, outline=(0, 0, 0), width=2)
        # Horizontal
        draw.rectangle([plus_start, center_y - 10, plus_start + 80, center_y + 10],
                      fill=plus_color, outline=(0, 0, 0), width=2)
    
    elif style == 'stacked':
        # M - made of stacked horizontal rectangles
        rect_height = 18
        for i in range(9):
            y = center_y - 80 + i * rect_height
            # Left side
            draw.rectangle([start_x, y, start_x + 25, y + rect_height - 2],
                          fill=letter_color, outline=(0, 0, 0), width=1)
            # Right side
            draw.rectangle([start_x + 75, y, start_x + 100, y + rect_height - 2],
                          fill=letter_color, outline=(0, 0, 0), width=1)
            # Middle connection for top part
            if i < 3:
                draw.rectangle([start_x + 25, y, start_x + 75, y + rect_height - 2],
                              fill=letter_color, outline=(0, 0, 0), width=1)
        
        # N - stacked
        n_start = start_x + 130
        for i in range(9):
            y = center_y - 80 + i * rect_height
            draw.rectangle([n_start, y, n_start + 25, y + rect_height - 2],
                          fill=letter_color, outline=(0, 0, 0), width=1)
            draw.rectangle([n_start + 75, y, n_start + 100, y + rect_height - 2],
                          fill=letter_color, outline=(0, 0, 0), width=1)
            if 2 < i < 6:
                draw.rectangle([n_start + 25, y, n_start + 75, y + rect_height - 2],
                              fill=letter_color, outline=(0, 0, 0), width=1)
        
        # + stacked
        plus_start = n_start + 150
        for i in range(7):
            y = center_y - 60 + i * rect_height
            draw.rectangle([plus_start + 30, y, plus_start + 50, y + rect_height - 2],
                          fill=plus_color, outline=(0, 0, 0), width=1)
        # Horizontal bars
        draw.rectangle([plus_start, center_y - 10, plus_start + 80, center_y + 10],
                      fill=plus_color, outline=(0, 0, 0), width=2)
    
    else:  # outlined
        # M - outline style with multiple rectangles
        # Left vertical outline
        draw.rectangle([start_x, center_y - 80, start_x + 8, center_y + 80],
                      fill=letter_color, outline=(0, 0, 0), width=2)
        draw.rectangle([start_x + 17, center_y - 80, start_x + 25, center_y + 80],
                      fill=letter_color, outline=(0, 0, 0), width=2)
        # Right vertical outline
        draw.rectangle([start_x + 75, center_y - 80, start_x + 83, center_y + 80],
                      fill=letter_color, outline=(0, 0, 0), width=2)
        draw.rectangle([start_x + 92, center_y - 80, start_x + 100, center_y + 80],
                      fill=letter_color, outline=(0, 0, 0), width=2)
        # Top bars
        draw.rectangle([start_x, center_y - 80, start_x + 50, center_y - 60],
                      fill=letter_color, outline=(0, 0, 0), width=2)
        draw.rectangle([start_x + 50, center_y - 80, start_x + 100, center_y - 60],
                      fill=letter_color, outline=(0, 0, 0), width=2)
        
        # N - outlined
        n_start = start_x + 130
        draw.rectangle([n_start, center_y - 80, n_start + 25, center_y + 80],
                      fill=letter_color, outline=(0, 0, 0), width=2)
        draw.rectangle([n_start + 75, center_y - 80, n_start + 100, center_y + 80],
                      fill=letter_color, outline=(0, 0, 0), width=2)
        draw.rectangle([n_start + 15, center_y - 20, n_start + 85, center_y],
                      fill=letter_color, outline=(0, 0, 0), width=2)
        
        # + outlined
        plus_start = n_start + 150
        draw.rectangle([plus_start + 30, center_y - 60, plus_start + 50, center_y + 60],
                      fill=plus_color, outline=(0, 0, 0), width=2)
        draw.rectangle([plus_start, center_y - 10, plus_start + 80, center_y + 10],
                      fill=plus_color, outline=(0, 0, 0), width=2)
    
    # Add small decorative rectangles
    for _ in range(random.randint(2, 3)):
        color = random.choice([c for c in SECONDARY_COLORS if c != bg_color])
        w = random.randint(20, 40)
        h = random.randint(20, 40)
        
        if random.choice([True, False]):
            x = random.randint(50, 200)
        else:
            x = random.randint(width - 200, width - 50)
        y = random.randint(40, height - 80)
        
        draw.rectangle([x, y, x + w, y + h], 
                      fill=color, outline=(0, 0, 0), width=2)
    
    return img


def generate_image(theme, width=1200, height=300, seed=None):
    """
    Generate an image based on the theme.
    
    Args:
        theme: Either 'balloon' or 'mnpluss'
        width: Image width in pixels (default 1200)
        height: Image height in pixels (default 300)
        seed: Random seed for reproducibility
    
    Returns:
        PIL Image object
    """
    if theme == 'balloon':
        return create_bauhaus_balloon(width, height, seed)
    elif theme == 'mnpluss':
        return create_bauhaus_mnpluss(width, height, seed)
    else:
        raise ValueError(f"Unknown theme: {theme}. Must be 'balloon' or 'mnpluss'")


if __name__ == '__main__':
    # Test generation
    balloon_img = generate_image('balloon', seed=42)
    balloon_img.save('test_balloon.png')
    print("Generated test_balloon.png")
    
    mnpluss_img = generate_image('mnpluss', seed=43)
    mnpluss_img.save('test_mnpluss.png')
    print("Generated test_mnpluss.png")
