import math
import bisect
import matplotlib.pyplot as plt


def list_round(list_to_round, dec_places):
    output = list()
    for t in list_to_round:
        a = tuple(map(lambda x: round(x, dec_places), t))
        output.append(a)
    return output


def get_distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt(abs(x1 - x2)**2 + abs(y1 - y2)**2)


class Line:
    """
    Class used to represent and calculate a line parameter of Path.
    """
    def __init__(self, start, end_p):
        self.pointer = start
        self.end_x = end_p[0]
        self.end_y = end_p[1]

    def how_many_pionts(self, line_length, density):
        return math.ceil(line_length / 10 * density)

    def calculate_dots(self, density):
        dots = list()
        px, py = self.pointer
        dx = self.end_x - px
        dy = self.end_y - py
        line_length = math.sqrt(dx**2 + dy**2)
        no_dots = self.how_many_pionts(line_length, density)
        dots_fraction = 1 / no_dots
        for i in range(no_dots):
            dots.append((px + i * dots_fraction * dx, py + i * dots_fraction * dy))
        dots.append((self.end_x, self.end_y))
        # rounding points
        dots_r = list_round(dots, 2)
        return dots_r
    

class Bezier_Base:
    """
    Base class for bezier and shapes.
    """

    def __init__(self, start, control_p, end_p):
        self.pionter = start
        self.control_x = control_p[0]
        self.control_y = control_p[1]
        self.end_x = end_p[0]
        self.end_y = end_p[1]
        self._build_lut()
        self.total_length = self.lut[len(self.lut) - 1][1]

    def get_piont(self, t):
        raise Exception("Get point method not implemented!")

    def _build_lut(self, steps=1000):
        """ Creates an array consisting of tuples (t_i, total_distance_from_beggining) with step entries. """
        self.lut = []
        old_point = self.get_piont(0)
        total_length = 0.0
        self.lut.append((old_point, total_length))
        for i in range(1, steps + 1):
            t = i / steps
            point = self.get_piont(t)
            total_length += get_distance(old_point, point)
            self.lut.append((t, total_length))
            old_point = point
        return total_length

    def get_t_from_length(self, length):
        """Returns parameter t for input length (from the beggining)."""
        if length <= 0.0:
            return 0.0
        if length >= self.total_length:
            return 1.0

        lengths = [entry[1] for entry in self.lut]
        id = bisect.bisect_left(lengths, length)
        t0, s0 = self.lut[id - 1]
        t1, s1 = self.lut[id]

        factor = (length - s0) / (s1 - s0)
        t = t0 + factor * (t1 - t0)
        return t

    def create_dots(self, density):
        d_s = 10 / density
        output = []
        no_dots = math.ceil(self.total_length / d_s)
        d_s = self.total_length / no_dots
        for i in range(no_dots + 1):
            t = self.get_t_from_length(i * d_s)
            point = self.get_piont(t)
            output.append(point)
        return list_round(output, 2)


class Bezier_Q(Bezier_Base):
    """
    Class used to represent and calculate a Q and q parameter of Path.
    """
    def __init__(self, start, control_p, end_p):
        self.pionter = start
        self.control_x = control_p[0]
        self.control_y = control_p[1]
        self.end_x = end_p[0]
        self.end_y = end_p[1]
        self._build_lut()
        self.total_length = self.lut[len(self.lut) - 1][1]

    def get_piont(self, t):
        if t < 0 or t > 1:
            raise ValueError("t has to be in range <0, 1>")
        x = (1 - t)**2 * self.pionter[0] + 2 * (1 - t) * t * self.control_x + t**2 * self.end_x
        y = (1 - t)**2 * self.pionter[1] + 2 * (1 - t) * t * self.control_y + t**2 * self.end_y
        return (x, y)

# class Bezier_C:
#     """
#     Class used to represent and calculate a C and c parameter of Path.
#     """


# def __init__(self, start, control_p1, control_p2, end_p):
#     self.pionter = start
#     self.control_x1 = control_p1[0]
#     self.control_y1 = control_p1[1]
#     self.control_x2 = control_p2[0]
#     self.control_y2 = control_p2[1]
#     self.end_x = end_p[0]
#     self.end_y = end_p[1]
#     self._build_lut()
#     self.total_length = self.lut[len(self.lut) - 1][1]

### control code to grafically plot the curve  

#Bezier_Q
# start_p = (0.0, 0.0)
# control_p = (15, 15)
# end_p = (5.0, 0.0)

# bezier = Bezier_Q(start_p, control_p, end_p)
# plt.plot([start_p[0], control_p[0], end_p[0]], [start_p[1], control_p[1], end_p[1]], 'r*', markersize=10)
# dots = bezier.create_dots(15)
# x, y = zip(*dots)

#line

# line = Line((0, 0), (0, 10))
# dots = line.calculate_dots(5)
# x, y = zip(*dots)

# #ploting logic

# plt.plot(x, y, 'yo')
# plt.axis((-1, 16, -1, 16))
# plt.gca().axes.set_yinverted(True)

# #tick size
# plt.gca().xaxis.set_major_locator(plt.MultipleLocator(1))
# plt.gca().yaxis.set_major_locator(plt.MultipleLocator(1))

# plt.grid(visible=True, which="both")
# plt.show()
