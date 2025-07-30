import math

def rectangle_area(length, breadth):
    return length * breadth

def square_area(side):
    return side ** 2

def circle_area(radius):
    return math.pi * radius ** 2

def rhombus_area(diagonal1, diagonal2):
    return 0.5 * diagonal1 * diagonal2

def triangle_area(base, height):
    return base * height * 0.5

def eq_triangle_area(side):
    return (3 ** 0.5 / 4) * side ** 2

def parallelogram_area(base, height):
    return base * height

def trapezium_area(base1, base2, height):
    return 0.5 * (base1 + base2) * height

def cube_volume(side):
    return side ** 3

def cuboid_volume(length, breadth, height):
    return length * breadth * height

def cylinder_volume(radius, height):
    return math.pi * radius ** 2 * height

def cone_volume(radius, height):
    return (1/3) * math.pi * radius ** 2 * height

def sphere_volume(radius):
    return (4/3) * math.pi * radius ** 3

def heron_area(a, b, c):
    s = (a + b + c) / 2
    return (s * (s - a) * (s - b) * (s - c)) ** 0.5

def rectangle_perimeter(length, breadth):
    return 2 * (length + breadth)

def square_perimeter(side):
    return 4 * side

def triangle_perimeter(a, b, c):
    return a + b + c

def circle_circumference(radius):
    return 2 * math.pi * radius

def rhombus_perimeter(side):
    return 4 * side

def parallelogram_perimeter(base, side):
    return 2 * (base + side)

def trapezium_perimeter(a, b, c, d):
    return a + b + c + d

def pythagoras_hypotenuse(a, b):
    return (a**2 + b**2) ** 0.5

def pythagoras_missing_side(hypotenuse, side):
    return (hypotenuse**2 - side**2) ** 0.5