from typing import Union


class color(str):
    """
    color((r, g, b))\n
    color("#000000")
    """
    def __init__(self, rgb:Union[tuple[int, int, int], str]) -> None:
        if not isinstance(rgb, (str, tuple)):
            raise TypeError(rgb, "have to be an hexa color or a tuple")
        
        self.value:tuple[int, int, int] = (0, 0, 0)

        if isinstance(rgb, str):
            self.value = (int((rgb.lstrip('#'))[:2], 16), int((rgb.lstrip('#'))[2:4], 16), int((rgb.lstrip('#'))[4:6], 16))
        else:
            self.value = rgb
    
    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, color) and (self.value == __value.value)
    
    def __str__(self) -> str:
        return ('#{:02x}{:02x}{:02x}'.format(*self.value)).upper()
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __sub__(self, other) -> 'color':
        if isinstance(other, color):
            return color(tuple((a-b) for a,b in list(zip(self.value, other.value)))) # type: ignore
        else:
            raise ValueError("Unsupported operand type")
        
    def __add__(self, other) -> 'color':
        if isinstance(other, color):
            return color(tuple((a+b) for a,b in list(zip(self.value, other.value)))) # type: ignore
        else:
            raise ValueError("Unsupported operand type")

    def __int__(self) -> int:
        return (self.value[0] << 16) + (self.value[1] << 8) + self.value[2]
    
    def hsv(self) -> tuple:
        rgb = self.value

        r, g, b = rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0

        max_value = max(r, g, b)
        min_value = min(r, g, b)

        v = max_value * 100

        s = max_value or ((max_value - min_value) / max_value) * 100

        if max_value == min_value:
            h = 0
        else:
            if max_value == r:
                h = ((g - b) / (max_value - min_value)) % 6
            elif max_value == g:
                h = ((b - r) / (max_value - min_value)) + 2
            elif max_value == b:
                h = ((r - g) / (max_value - min_value)) + 4
            h *= 60

        h = (h+360)%360

        return (int(h), int(s), int(v))


def color_moy(*args:color) -> color:
    def moy(args:tuple) -> int:
        i = 0
        som = 0
        for item in args:
            som += item
            i+=1
        return som//i
    return color(tuple(map(moy, zip(*map(lambda x: x.value, args))))) # type: ignore


def rgb_distance(color1:color, color2:color) -> float:
    r1, g1, b1 = color1.value
    r2, g2, b2 = color2.value
    return ((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)**(1/2)

def find_closest_color(tc:color, cl:list[color]):
    closest_distance = float('inf')
    for c in cl:
        distance = rgb_distance(tc, c)
        if distance < closest_distance:
            closest_distance = distance
            closest_color = c
            sub = tc - c

    return closest_color, sub

def croix(value:color, val:list[color], pal:list[color]) -> color:

    start, sub = find_closest_color(value, val)
    
    end = val[(val.index(start) + (-1 if (int(start) > int(value)) else 1))%len(val)]

    percent = int(value - start) * 100 / int(end - start)



    other_start = int(pal[val.index(start)])

    other_end = int(pal[(val.index(start) + (-1 if (int(start) > int(value)) else 1))%len(pal)])

    final = int(other_end + (percent * (other_start - other_end) / 100))

    return color(hex(final)[2:].upper().zfill(6))

def hsv_to_rgb(h, s, v):

    h = (h % 360) / 360.0
    s = max(0, min(1, s / 100.0))
    v = max(0, min(1, v / 100.0))

    if s == 0:
        r = g = b = int(v * 255)
    else:
        h *= 6
        i = int(h)
        f = h - i
        p = int(255 * v * (1 - s))
        q = int(255 * v * (1 - s * f))
        t = int(255 * v * (1 - s * (1 - f)))

        if i == 0:
            r, g, b = int(v * 255), t, p
        elif i == 1:
            r, g, b = q, int(v * 255), p
        elif i == 2:
            r, g, b = p, int(v * 255), t
        elif i == 3:
            r, g, b = p, q, int(v * 255)
        elif i == 4:
            r, g, b = t, p, int(v * 255)
        else:
            r, g, b = int(v * 255), p, q

    return r, g, b

def getpourcent(form:color, to:color, c:color) -> list[float]:
    
    one_:tuple[int, ...] = tuple(map(clamp, form.hsv()))
    two_:tuple[int, ...] = tuple(map(clamp, to.hsv()))
    trois:tuple[int, ...] = tuple(map(clamp, c.hsv()))

    f:list[float] = []

    for i in range(3):
        one = min(one_, two_, key=lambda x: x[i])
        two = max(one_, two_, key=lambda x: x[i])

        cent = two[i] - one[i]
        val = trois[i] - one[i]

        pourcent = one[i]/100 if cent == 0 else (val/cent)

        f.append(pourcent)

    return f

def getcolor(form:color, to:color, percent:list[float]) -> color:

    f = []
    for i in range(3):
        one_ = tuple(map(clamp, form.hsv()))
        two_ = tuple(map(clamp, to.hsv()))

        one = min(one_, two_, key=lambda x: x[0])[i]
        two = max(one_, two_, key=lambda x: x[0])[i]

        value = one + int((percent[i]) * (two - one))
        
        f.append(value)

    return color(hsv_to_rgb(*f))

def clamp(n):
    p = n%5
    n += 5-p if round(p)>2 else -p
    return n

def transfo(moule:list[color], objectif:list[color], c:color) -> color:
    return getcolor(objectif[0], objectif[1], getpourcent(moule[0], moule[1], c))