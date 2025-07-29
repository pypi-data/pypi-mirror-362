def levels_generator(start_color, finish_color, levels):
    get_color = lambda a, b, c, d: int(a + (float(c) / (d - 1)) * (b - a))
    for step in range(levels):
        yield tuple(get_color(start_color[x], finish_color[x], step, levels) for x in range(3)), step
