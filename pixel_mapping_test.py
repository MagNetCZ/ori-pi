from pixel_mapping import *

strip_length = 12

mapping = PixelMapping(10, strip_length * 3, 60)


def map_strip_down(col, lamp_row, channel, start_index, lamp):
    row = lamp_row * strip_length
    return mapping.map_strip_down(strip_length, channel, start_index, lamp, col, row)

def map_strip_up(col, lamp_row, channel, start_index, lamp):
    row = ((lamp_row + 1) * strip_length) - 1
    return mapping.map_strip_up(strip_length, channel, start_index, lamp, col, row)


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


mapping.set_lamp(7, 255,255,255)

channel = mapping.get_channel(1)

print channel
print len(channel)
