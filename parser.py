import xml.etree.ElementTree as ET
from math import sqrt, ceil


ns = {'ink': '{http://www.w3.org/2000/svg}'}


class Parser:
    """
    this is class for parsing raw inkscape svg.
    """
    def __init__(self, file_path):
        self.tree = ET.parse(file_path)
        self.root = self.tree.getroot()

    def get_layers(self):
        layers = list()
        for layer in self.root.findall('{http://www.w3.org/2000/svg}g'):
            layers.append(layer)
            # print(layer.get("id"))
        return (layers)

    def get_elements(self, layer):
        elements = list(layer.iter())
        elements.pop(0)
        return elements


def list_round(list_to_round, dec_places):
    output = list()
    for t in list_to_round:
        a = tuple(map(lambda x: round(x, dec_places), t))
        output.append(a)
    return output


class Path:
    """
    class used to extract points from path
    """
    def __init__(self, path):
        if not path.get('d'):
            raise TypeError("Is not a path (must have a 'd' attribute)")
        self.path = path
        self.pointer = (0, 0)
        self.points = list()

    def calc_M(self, x, y):
        self.pointer = (x, y)

    def calc_m(self, x, y):
        self.pointer[0] += x
        self.pointer[1] += y

    def how_many_pionts(self, line_length, density):
        return ceil(line_length / 10 * density)

    def calc_L(self, x, y, density):
        dots = list()
        px, py = self.pointer
        dy = y - py
        dx = x - px
        line_length = sqrt(dx**2 + dy**2)
        no_dots = self.how_many_pionts(line_length, density)
        dots_fraction = 1 / no_dots
        for i in range(no_dots):
            dots.append((px + i * dots_fraction * dx, py + i * dots_fraction * dy))
        dots.append((x, y))
        # rounding points
        dots_r = list_round(dots, 2)
        return dots_r
    
    def calc_l(self, x, y, density):
        dots = list()
        px, py = self.pointer
        line_length = sqrt(x**2 + y**2)
        no_dots = self.how_many_pionts(line_length, density)
        dots_fraction = 1 / no_dots
        for i in range(no_dots):
            dots.append((px + i * dots_fraction * x, py + i * dots_fraction * y))
        dots.append((px + x, py + y))
        # rounding points
        dots_r = list_round(dots, 2)
        return dots_r

    def calc_Q(self, cx,  cy, x, y)

parser = Parser("example.svg")
layers = parser.get_layers()
path1 = Path(parser.get_elements(layers[0])[0])
path1.calc_l(20, 20, 1)
pass
