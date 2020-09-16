import colours

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
    # only draw if we need to
    if fill is not None:
        x1 = x + thickness/2
        x2 = x + size - thickness/2
        y1 = y + thickness/2
        y2 = y + size - thickness/2
        draw.ellipse([x1, y1, x2, y2], fill=fill)


background = "#222222"
fill = "white"


# TODO - move this into a module
# TODO - allow passing in a screen size
# TODO - allow passing in colours
# TODO - allow passing in colour groups i.e. pastel
# TODO - allow passing in numbers (plus different bases???)
# TODO - allow disabling of diagonals or only diagonals


def main():
    diameter = 30
    radius = diameter / 2
    spacing = 20
    thickness = 16  # ignored if fill is none
    line_thickness = 5
    x_number = 50
    y_number = 20

    x_size = x_number * (diameter + spacing) + spacing
    y_size = y_number * (diameter + spacing) + spacing

    img = Image.new('RGB', (x_size, y_size), color=background)
    d = ImageDraw.Draw(img)

    points = [
        [
            {
                "colour": random.choice(colours.teal),
                "x": (x * (diameter + spacing) + spacing),
                "y": (y * (diameter + spacing)) + spacing
            } for y in range(y_number)
        ] for x in range(x_number)
    ]

    # get our lines to be drawn
    lines = []

    # do this by indexing, easier than iterating over the list
    # need to only check down, right, RD diagonal and RU diagonal
    for r in range(len(points)):
        for c in range(len(points[0])):  # just check the len of the first row, all the same diameter
            # R, D, RD, RU
            for r_, c_ in [(r, c+1), (r+1, c), (r+1, c+1), (r-1, c+1)]:
                try:
                    # guard around negative indexing
                    if r_ < 0:
                        continue

                    # find our if the neighbour is the same, add a line def if it is
                    if points[r][c]["colour"] == points[r_][c_]["colour"]:
                        lines.append((
                            (points[r][c]["x"] + radius, points[r][c]["y"] + radius),
                            (points[r_][c_]["x"] + radius, points[r_][c_]["y"] + radius),
                            points[r][c]["colour"]
                        ))
                except IndexError:  # ignore the index errors, expected when we hit the right/bottom
                    pass

    # draw our lines
    # TODO - randomise this as the bottom right lines are always drawn over the upper left lines
    for line in lines:
        d.line(
            [
                (line[0][0], line[0][1]),
                (line[1][0], line[1][1])
            ],
            fill=line[2],
            width=line_thickness
        )

    # adding circles
    for row in points:
        for col in row:
            ring(
                d,
                x=col['x'],
                y=col['y'],
                size=diameter,
                thickness=thickness,
                outline=col['colour'],
                fill=fill
            )

    img.save('out/example.png')


if __name__ == "__main__":
    main()
