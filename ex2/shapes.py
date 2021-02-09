#########################################################################
# FILE: shapes.py
# WRITER: Benjamin Maman, benm, 341145811
# EXERCISE: intro2cs ex2 2017-2018
# DESCRIPTION: A function to calcul area of differents shapes
#########################################################################

import math


def circle_area(radius):
    """Receive a radius of a circle and return area"""
    return math.pi * radius ** 2


def rectangle_area(edge_a, edge_b):
    """Receive edges sizes and return area of the rectangle"""
    return edge_a * edge_b


def trapeze_area(base_a, base_b, distance):
    """Receive basis sizes, distance and return area of the trapeze"""
    return ((base_a + base_b) / 2) * distance


def shape_area():
    """A function that compute the area of different shape"""

    # Asking the chosen shape...
    shape = input('Choose shape (1=circle, 2=rectangle, 3=trapezoid):')

    if shape == '1':  # User choose circle
        radius = float(input())  # Asking for the rayon
        return circle_area(radius)

    elif shape == '2':  # User choose rectangle
        edge_a = float(input())  # Asking for the sides
        edge_b = float(input())
        return rectangle_area(edge_a, edge_b)

    elif shape == '3':  # User choose trapeze
        base_a = float(input())  # Asking for the dimensions
        base_b = float(input())
        distance = float(input())
        return trapeze_area(base_a, base_b, distance)

    else:
        return None
