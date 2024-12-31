# Import library pygame untuk membuat game
import pygame
import math

# Inisialisasi pygame
pygame.init()

# Definisi ukuran layar dan zoom
width, height = 1920, 1080
zoom = 0.4

# Set mode layar
screen = pygame.display.set_mode((int(width * zoom), int(height * zoom)))
pygame.display.set_caption("Sepeda dengan Pemandangan")

# Fungsi untuk menggambar latar belakang
def draw_background():
    sky_color = (135, 206, 250)
    pygame.draw.rect(screen, sky_color, (0, 0, width * zoom, height * zoom), 0)

    grass_color = (0, 106, 0)
    pygame.draw.rect(screen, grass_color, (0, int(400 * zoom), width * zoom, (height - 400) * zoom), 0)

    sun_color = (255, 255, 0)
    pygame.draw.circle(screen, sun_color, (int(175 * zoom), int(100 * zoom)), int(50 * zoom))

# Fungsi untuk menggambar bebatuan
def draw_rocks():
    rock_color = (169, 169, 169)  # Warna abu-abu untuk bebatuan

    rocks = [
        (150, 550), (250, 500), (350, 550),
        (550, 520), (650, 480), (750, 520),
        (950, 500), (1050, 550), (1150, 500),
        (200, 600), (400, 650), (600, 600),
        (800, 550), (1000, 600), (1200, 550),
        (300, 700), (500, 750), (700, 700),
        (1000, 700), (1200, 750), (1400, 700),
        (300, 600), (500, 650), (700, 600),
        (900, 650), (1100, 600), (1300, 650),
    ]

    for rock in rocks:
        pygame.draw.circle(screen, rock_color, (int(rock[0] * zoom), int(rock[1] * zoom)), int(10 * zoom))

# Fungsi untuk menggambar awan
def draw_cloud(x, y):
    cloud_color = (255, 255, 255)
    pygame.draw.circle(screen, cloud_color, (int(x * zoom), int(y * zoom)), int(30 * zoom))
    pygame.draw.circle(screen, cloud_color, (int((x + 40) * zoom), int(y * zoom)), int(40 * zoom))
    pygame.draw.circle(screen, cloud_color, (int((x + 80) * zoom), int(y * zoom)), int(30 * zoom))

# Fungsi untuk menggambar latar belakang dengan awan
def draw_background_with_clouds(cloud_positions):
    draw_background()
    for cloud_pos in cloud_positions:
        draw_cloud(*cloud_pos)

# Fungsi untuk mengupdate posisi awan
def update_cloud_positions(cloud_positions, cloud_speed):
    updated_positions = [(x + cloud_speed, y) for x, y in cloud_positions]
    
    # Check jika awan telah melewati batas kanan layar, kemudian reset posisi
    for i in range(len(updated_positions)):
        x, y = updated_positions[i]
        if x > width * zoom * 3.5:
            updated_positions[i] = (-100, y)  # Pindahkan awan ke kiri layar
    
    return updated_positions

# Fungsi untuk menggambar tanaman
def draw_plant(x, y):
    stem_color = (0, 128, 0)
    leaf_color = (0, 255, 0)
    dark_factor = 0.7  # Faktor gelap untuk membuat warna lebih gelap
    stem_width = int(5 * zoom)

    # Gambar batang
    pygame.draw.line(screen, (int(stem_color[0] * dark_factor), int(stem_color[1] * dark_factor), int(stem_color[2] * dark_factor)),
                     (int(x * zoom), int(y * zoom)), (int(x * zoom), int((y - 100) * zoom)), stem_width)

    # Gambar daun
    pygame.draw.polygon(screen, (int(leaf_color[0] * dark_factor), int(leaf_color[1] * dark_factor), int(leaf_color[2] * dark_factor)),
                        [
                            (int((x - 10) * zoom), int((y - 50) * zoom)),
                            (int((x + 10) * zoom), int((y - 50) * zoom)),
                            (int(x * zoom), int((y - 80) * zoom))
                        ], 0)

    pygame.draw.polygon(screen, (int(leaf_color[0] * dark_factor), int(leaf_color[1] * dark_factor), int(leaf_color[2] * dark_factor)),
                        [
                            (int((x - 10) * zoom), int((y - 80) * zoom)),
                            (int((x + 10) * zoom), int((y - 80) * zoom)),
                            (int(x * zoom), int((y - 110) * zoom))
                        ], 0)

# Fungsi untuk menggambar latar belakang dengan awan dan tanaman
def draw_background_with_clouds_and_plants(cloud_positions):
    draw_background_with_clouds(cloud_positions)

    draw_plant(100, 400)
    draw_plant(300, 350)
    draw_plant(500, 420)
    draw_plant(700, 380)
    draw_plant(900, 400)

# Fungsi untuk menggambar latar belakang dengan awan, tanaman, dan bebatuan
def draw_background_with_clouds_plants_and_rocks(cloud_positions):
    draw_background_with_clouds_and_plants(cloud_positions)
    draw_rocks()

# Fungsi untuk menggambar rangka sepeda
def draw_frame(x, y, reflect=False):
    points = [(165, 465), (317, 220), (400, 465), (600, 220), (695, 465)]
    line_fill = (200, 150, 155)
    line_width = int(15 * zoom)

    for i in range(len(points) - 1):
        x_point = int((points[i][0] + x) * zoom)
        y_point = int((points[i][1] + y) * zoom)

        if reflect:
            x_point = int(width * zoom) - x_point

        pygame.draw.line(screen, line_fill, (x_point, y_point),
                         (int((points[i + 1][0] + x) * zoom), int((points[i + 1][1] + y) * zoom)), line_width)

    for p in points:
        x_p = int((p[0] + x) * zoom)
        y_p = int((p[1] + y) * zoom)

        if reflect:
            x_p = int(width * zoom) - x_p

        pygame.draw.circle(screen, line_fill, (x_p, y_p), line_width // 2)

# Fungsi untuk menggambar setang sepeda
def draw_handlebar(x, y, reflect=False):
    points = [(605, 220), (582, 147), (707, 140), (737, 158), (749, 185), (741, 222), (717, 246), (689, 251)]

    line_fill = (200, 150, 155)
    line_width = int(10 * zoom)

    for i in range(len(points) - 1):
        x_point = int((points[i][0] + x) * zoom)
        y_point = int((points[i][1] + y) * zoom)

        pygame.draw.line(screen, line_fill, (x_point, y_point),
                         (int((points[i + 1][0] + x) * zoom), int((points[i + 1][1] + y) * zoom)), line_width)

    for p in points:
        x_p = int((p[0] + x) * zoom)
        y_p = int((p[1] + y) * zoom)

    
        pygame.draw.circle(screen, line_fill, (x_p, y_p), line_width // 3)

# Fungsi untuk menggambar roda sepeda
def draw_wheels(x, y, offset):
    points = [(165, 465), (695, 465)]
    r = int(150 * zoom)
    
    line_fill = (0, 0, 0)
    line_width = int(10 * zoom)

    for i in range(len(points)):
        x_wheel, y_wheel = int((points[i][0] + x) * zoom), int((points[i][1] + y) * zoom)
        pygame.draw.circle(screen, line_fill, (x_wheel, y_wheel), r, line_width)

        for k in range(0, int(math.pi * 2 * 100), 30):
            x_end = int(x_wheel + math.cos(k / 100 + offset) * r)
            y_end = int(y_wheel + math.sin(k / 100 + offset) * r)
            pygame.draw.line(screen, line_fill, (x_wheel, y_wheel), (x_end, y_end), line_width)

        x1 = int(x_wheel + math.cos(offset) * r * 5 / 8)
        y1 = int(y_wheel + math.sin(offset) * r * 5 / 8)
        r1 = int(15 * zoom)
        pygame.draw.circle(screen, (0, 255, 255), (x1, y1), r1)

        x2 = int(x_wheel + math.cos(offset + math.pi) * r * 5 / 8)
        y2 = int(y_wheel + math.sin(offset + math.pi) * r * 5 / 8)
        pygame.draw.circle(screen, (0, 255, 255), (x2, y2), r1)

        offset += math.pi / 2

# Fungsi untuk menggambar burung di layar
def draw_bird_on_screen(x, y):
    bird_body_lines = [
        ((x - 10, y), (x - 5, y - 20)),
        ((x - 5, y - 20), (x + 5, y - 20)),
        ((x + 5, y - 20), (x + 10, y))
    ]

    for line in bird_body_lines:
        pygame.draw.line(screen, (0, 0, 0), (line[0][0] * zoom, line[0][1] * zoom), (line[1][0] * zoom, line[1][1] * zoom), 2)

# Fungsi utama program
def main():
    running = True
    clock = pygame.time.Clock()
    pedal_angle = math.pi / 2
    x_bike, y_bike = 0, 0

    cloud_positions = [(200, 50), (500, 100), (800, 30)]
    cloud_speed = 2

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))
        draw_background_with_clouds_plants_and_rocks(cloud_positions)

        draw_wheels(x_bike, y_bike, pedal_angle / 2)
        draw_frame(x_bike, y_bike)
        draw_handlebar(x_bike, y_bike)

        draw_bird_on_screen(100, 150)
        draw_bird_on_screen(300, 100)

        pygame.display.flip()

        # pedal_angle += 0.05
        x_bike += 3  # Pindahkan sepeda ke kanan sejauh 2 pixel setiap frame

        if x_bike > width * zoom * 3:
            x_bike = 0

        cloud_positions = update_cloud_positions(cloud_positions, cloud_speed)

        clock.tick(60)

# Memanggil fungsi utama jika script dijalankan
if __name__ == "__main__":
    main()
