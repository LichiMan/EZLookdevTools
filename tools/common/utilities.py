def get_random_color(seed):
    random.seed(seed + "_r")
    color_red = random.uniform(0, 1)
    random.seed(seed + "_g")
    color_green = random.uniform(0, 1)
    random.seed(seed + "_b")
    color_blue = random.uniform(0, 1)
    return [color_red, color_green, color_blue]
