from PIL import Image, ImageDraw, ImageFilter
import os
import random
import time
import numpy as np

def create_random_color():
    """Generate a random RGB color."""
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def create_radial_gradient(width, height, color1, color2):
    """Create an image with a radial gradient from color1 to color2."""
    image = Image.new("RGB", (width, height))
    center_x, center_y = width // 2, height // 2
    max_radius = np.sqrt(center_x**2 + center_y**2)

    for y in range(height):
        for x in range(width):
            distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)
            ratio = distance / max_radius
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            image.putpixel((x, y), (r, g, b))

    return image

def add_geometric_pattern(image, shape_count, max_size):
    """Add symmetrical geometric shapes with varied transparency."""
    draw = ImageDraw.Draw(image, "RGBA")
    width, height = image.size

    for _ in range(shape_count):
        size = random.randint(20, max_size)
        x = random.randint(size, width - size)
        y = random.randint(size, height - size)
        shape_type = random.choice(["circle", "hexagon"])
        color = create_random_color() + (random.randint(50, 150),)

        if shape_type == "circle":
            draw.ellipse((x - size, y - size, x + size, y + size), fill=color)
        else:
            draw_regular_polygon(draw, (x, y), size, 6, color)

def draw_regular_polygon(draw, center, radius, sides, fill):
    """Draw a regular polygon given the number of sides."""
    angle_step = 2 * np.pi / sides
    points = [
        (
            center[0] + radius * np.cos(i * angle_step),
            center[1] + radius * np.sin(i * angle_step),
        )
        for i in range(sides)
    ]
    draw.polygon(points, fill=fill)

def add_subtle_grid(image, grid_spacing, grid_color):
    """Add a subtle grid overlay to the image."""
    draw = ImageDraw.Draw(image)
    width, height = image.size

    for x in range(0, width, grid_spacing):
        draw.line((x, 0, x, height), fill=grid_color)
    for y in range(0, height, grid_spacing):
        draw.line((0, y, width, y), fill=grid_color)

def add_texture_overlay(image, intensity):
    """Add a noise-based texture overlay to the image."""
    overlay = Image.effect_noise(image.size, intensity)
    overlay = overlay.convert("RGB")
    image = Image.blend(image, overlay, 0.1)  # Blend with slight transparency
    return image

def save_image(image, save_directory, filename):
    """Save the image to the specified directory."""
    os.makedirs(save_directory, exist_ok=True)
    save_path = os.path.join(save_directory, filename)
    image.save(save_path)
    print(f"Image saved to {save_path}")

def generate_and_save_image():
    # Define the dimensions
    width, height = 10920, 8080

    # Generate colors
    color1 = create_random_color()
    color2 = create_random_color()

    # Create the gradient background
    background = create_radial_gradient(width, height, color1, color2)

    # Add geometric patterns
    add_geometric_pattern(background, shape_count=50, max_size=100)

    # Add a subtle grid
    add_subtle_grid(background, grid_spacing=100, grid_color=(255, 255, 255, 30))

    # Add texture overlay
    background = add_texture_overlay(background, intensity=50)

    # Define the directory for saving the image
    save_directory = os.path.join(os.path.expanduser("~"), "Desktop")

    # Generate a unique filename with timestamp
    timestamp = int(time.time())
    filename = f"artistic_background_{timestamp}.png"

    # Save the image
    save_image(background, save_directory, filename)

# Run the image generation and saving function
generate_and_save_image()
