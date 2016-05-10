from pixel_mapping import *
import opc, time, random

strip_length = 12
channels = 4
height = strip_length * 3
width = 10
lamps = 9

mapping = PixelMapping(10, strip_length * 3, 60)
client = opc.Client('192.168.1.100:7890')

def map_strip_down(col, lamp_row, channel, start_index, lamp):
    row = lamp_row * strip_length
    return mapping.map_strip_down(col, row, strip_length, channel, start_index, lamp)

def map_strip_up(col, lamp_row, channel, start_index, lamp):
    row = ((lamp_row + 1) * strip_length) - 1
    return mapping.map_strip_up(col, row, strip_length, channel, start_index, lamp)


#channel 0
channel = 0
index = map_strip_down(4, 2, channel, 0, 6)
index = map_strip_up(3, 2, channel, index, 5)
index = map_strip_down(2, 2, channel, index, 5)
index = map_strip_up(1, 2, channel, index, 4)
index = map_strip_down(0, 2, channel, index, 4)

#channel 1
channel = 1
index = map_strip_down(5, 2, channel, 0, 6)
index = map_strip_up(6, 2, channel, index, 7)
index = map_strip_down(7, 2, channel, index, 7)
index = map_strip_up(8, 2, channel, index, 8)
index = map_strip_down(9, 2, channel, index, 8)

#channel 2
channel = 2
index = map_strip_up(2, 1, channel, 0, 1)
index = map_strip_down(3, 1, channel, index, 1)
index = map_strip_up(6, 1, channel, index, 3)
index = map_strip_down(7, 1, channel, index, 3)


#channel 3
channel = 3
index = map_strip_up(4, 1, channel, 0, 2)
index = map_strip_up(5, 0, channel, index, 0)
index = map_strip_down(4, 0, channel, index, 0)
index = map_strip_down(5, 1, channel, index, 2)

lamp = 0
x = 0
y = 0
counter = 0

blue = (0,0,255)
red = (255,0,0)

color_primary = (255,255,255)
#color_primary = (0,0,255)
#color_secondary = (100,100,100)
color_secondary = (100,100,100)
color_highlight = (70,70,255)
#color_highlight = (255,0,0)

def loop_y(y):
    return y % height

def color_mult(color, multiplier):
    return (float(color[0]) * multiplier, float(color[1]) * multiplier, float(color[2]) * multiplier)

def put_pixels():
    channel_pixels = mapping.get_output()
    client.put_pixels(channel_pixels)

def deco_randomxy():
    mapping.set_y(random.randint(0, height), color_secondary)
    mapping.set_x(random.randint(0, width), color_secondary)

def deco_lamp_flicker(lamp):
    #mapping.set_lamp(
    pass

def program_bootup():
    global lamp, x, y, width, height, counter
    
    mapping.clear()

    mapping.set_lamp(lamp, color_highlight)
    #mapping.set_x(x, 255,255,255)

    for i in range(10):
        mapping.set_y(loop_y(y - i), color_mult(color_primary, 1.0 - i * 0.1))    
    
    if (counter % 2) == 0:
        lamp = random.randint(0, 8)

    if random.random() < 0.5:
        deco_randomxy()

    x = (x + 1) % 10
    y = loop_y(y+1)

    counter += 1

    put_pixels()
    time.sleep(.8)

lamp_columns = [
    [ 8 ],
    [ 3, 7 ],
    [ 0, 2, 6 ],
    [ 1, 5 ],
    [ 4 ]
    ]

def program_around():
    global counter, lamp
    
    mapping.clear()

    for lamp in lamp_columns[counter % len(lamp_columns)]:
        mapping.set_lamp(lamp, color_primary)

    deco_randomxy()

    counter -= 1

    put_pixels()
    time.sleep(.4)

def program_around_random():
    global counter, lamp
    
    mapping.clear()

    for lamp in lamp_columns[random.randint(0, len(lamp_columns) - 1)]:
        mapping.set_lamp(lamp, color_primary)

    for lamp in lamp_columns[random.randint(0, len(lamp_columns) - 1)]:
        mapping.set_lamp(lamp, color_primary)

    deco_randomxy()

    put_pixels()
    time.sleep(.4)


def pixel_noise(pixel):
    pixel

def random_color():
    if random.random() < 0.3:
        return color_primary

    return color_highlight

def program_noise_init():
    mapping.iterate_pixels(lambda pixel: pixel.set_rgb(color_mult(random_color(), random.random())))

def program_noise():
    #mapping.iterate_pixels(lambda pixel: pixel.set_rgb(color_mult(pixel.get_rgb(), random.random() * 2)))
    for lamp in range(0, lamps):
        lamp_pixels = mapping.get_lamp(lamp)
        lamp_mult = (random.random() - 0.5) * 1 + 1
        for pixel in lamp_pixels:
            pixel_mult = (random.random() - 0.5) * 0.25 + 1
            pixel.set_rgb(color_mult(pixel.get_rgb(), lamp_mult * pixel_mult))
            

    put_pixels()
    time.sleep(.3)

def program_init():
    pass

def random_lamp():
    return random.randint(0, lamps - 1)

def program_transition():
    mapping.clear()
    
    for i in range(3):
        mapping.fill_pixels(color_primary)
        mapping.set_lamp(random_lamp(), (0,0,0))
        mapping.set_lamp(random_lamp(), (0,0,0))
        mapping.set_lamp(random_lamp(), (0,0,0))
        put_pixels()
        put_pixels()
        time.sleep(0.2)
        mapping.clear()
        put_pixels()
        put_pixels()

    mapping.fill_pixels(color_primary)
    put_pixels()
    time.sleep(0.2)
    mapping.clear()
    put_pixels()

    time.sleep(0.3)

class Program:
    def __init__(self, function, function_init, duration):
        self.function = function
        self.duration = duration
        self.function_init = function_init

programs = [
    Program(program_bootup, program_init, 30),
    Program(program_bootup, program_init, 40),
    Program(program_around, program_init, 10),
    Program(program_around_random, program_init, 10),
    Program(program_noise, program_noise_init, 15),
    Program(program_noise, program_noise_init, 15)
    ]

program_index = 3
last_program_index = program_index
cur_program = programs[program_index]
last_switch = time.time()

while (True):
    program_transition()
    
    cur_program.function_init()
    
    while (time.time() - last_switch < cur_program.duration):
        cur_program.function()

    last_switch = time.time()

    while (program_index == last_program_index):
        program_index = random.randint(0, len(programs) - 1)
    last_program_index = program_index
    cur_program = programs[program_index]

print channel_pixels
print len(channel_pixels)
