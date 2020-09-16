import random
from PIL import Image, ImageDraw


def ring(draw, x, y, size, thickness=2, outline="black", fill="white"):
    """
    :param draw: ImageDraw object
    :param x: x coordinate of top left point
    :param y: y coordinate of top left point
    :param size: size of the ring
    :param thickness: thickness of the line
    :param outline: outline colour
    :param fill: fill colour
    :return: None
    """
    # outer circle
    x1 = x
    x2 = x + size
    y1 = y
    y2 = y + size
    draw.ellipse([x1, y1, x2, y2], fill=outline)

    # inner circle
    x1 = x + thickness/2
    x2 = x + size - thickness/2
    y1 = y + thickness/2
    y2 = y + size - thickness/2
    draw.ellipse([x1, y1, x2, y2], fill=fill)


colours = ["red", "white", "blue", "green", "yellow", "pink"]


def main():
    diameter = 20
    radius = 10
    spacing = 15
    thickness = 10
    x_number = 50
    y_number = 25

    x_size = x_number * (diameter + spacing) + spacing
    y_size = y_number * (diameter + spacing) + spacing

    img = Image.new('RGB', (x_size, y_size), color='black')

    d = ImageDraw.Draw(img)

    points = [
        [
            {
                "colour": random.choice(colours),
                "x": (x * (diameter + spacing) + spacing),
                "y": (y * (diameter + spacing)) + spacing
            } for y in range(y_number)
        ] for x in range(x_number)
    ]

    # get out lines
    lines = []

    # do this by indexing, easier than iterating over the list
    # need to only check down, right and the bottom diagonal
    for r in range(len(points)):
        for c in range(len(points[0])):  # just check the len of the first row, all the same diameter
            # checking right
            try:
                if points[r][c]["colour"] == points[r][c+1]["colour"]:
                    lines.append((
                        (points[r][c]["x"] + radius, points[r][c]["y"] + radius),
                        (points[r][c+1]["x"] + radius, points[r][c+1]["y"] + radius),
                        points[r][c]["colour"]
                    ))
            except IndexError:
                pass

            # checking down
            try:
                if points[r][c]["colour"] == points[r+1][c]["colour"]:
                    lines.append((
                        (points[r][c]["x"] + radius, points[r][c]["y"] + radius),
                        (points[r+1][c]["x"] + radius, points[r+1][c]["y"] + radius),
                        points[r][c]["colour"]
                    ))
            except IndexError:
                pass

            # rd diagonal
            try:
                if points[r][c]["colour"] == points[r+1][c+1]["colour"]:
                    lines.append((
                        (points[r][c]["x"] + radius, points[r][c]["y"] + radius),
                        (points[r+1][c+1]["x"] + radius, points[r+1][c+1]["y"] + radius),
                        points[r][c]["colour"]
                    ))
            except IndexError:
                pass

            # ru diagonal
            try:
                # for the ru diagonal we need an extra guard for negative indexes
                if points[r][c]["colour"] == points[r-1][c+1]["colour"] and r - 1 > 0:
                    lines.append((
                        (points[r][c]["x"] + radius, points[r][c]["y"] + radius),
                        (points[r-1][c+1]["x"] + radius, points[r-1][c+1]["y"] + radius),
                        points[r][c]["colour"]
                    ))
            except IndexError:
                pass

    # draw our lines
    for line in lines:
        d.line(
            [
                (line[0][0], line[0][1]),
                (line[1][0], line[1][1])
            ],
            fill=line[2],
            width=5
        )

    # from pprint import pprint
    # pprint(points)

    # adding circles
    for row in points:
        for col in row:
            ring(d, x=col['x'], y=col['y'], size=diameter, thickness=thickness, outline=col['colour'], fill="black")

    img.save('out/example.png')


if __name__ == "__main__":
    main()
