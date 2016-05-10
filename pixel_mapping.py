class Pixel:
	def __init__(self, x, y):
		self.rgb = (0,0,0)
		self.x = x
		self.y = y
		self.index = 0
		self.channel = -1
		self.lamp = -1

	def set_rgb(self, rgb):
		self.rgb = rgb

	def get_rgb(self):
		return self.rgb

class PixelMapping:
	def __init__(self, width, height, channel_size):
		self.mapping = []
		self.width = width
		self.height = height
		self.channel_size = channel_size

		for x in range(width):
			self.mapping.append([])
			for y in range(height):
				self.mapping[x].append(Pixel(x, y))

	# Mapping

	def map_strip(self, x, y, length, channel, start_index, lamp, x_step, y_step):
		for i in range(length):
			pixel = self.get_pixel(x, y)
			pixel.channel = channel
			pixel.lamp = lamp
			pixel.index = start_index + i

			x += x_step
			y += y_step

		return start_index + length

	def map_strip_down(self, x, y, length, channel, start_index, lamp):
		return self.map_strip(x, y, length, channel, start_index, lamp, 0, 1)

	def map_strip_up(self, x, y, length, channel, start_index, lamp):
		return self.map_strip(x, y, length, channel, start_index, lamp, 0, -1)

	# Selectors (Getters)

	def get_pixel(self, x, y):
		return self.mapping[x][y]

	def get_pixels(self, condition):
		pixels = []

		for x in range(self.width):
			for y in range(self.height):
				pixel = self.get_pixel(x, y)
				if (condition(pixel)):
					pixels.append(pixel)

		return pixels

	def iterate_pixels(self, function):
		for x in range(self.width):
			for y in range(self.height):
				function(self.get_pixel(x, y))

	def get_lamp(self, lamp):
		return self.get_pixels(lambda pixel: pixel.lamp == lamp)

	def get_x(self, x):
		return self.get_pixels(lambda pixel: pixel.x == x)

	def get_y(self, y):
		return self.get_pixels(lambda pixel: pixel.y == y)

	# Setters

	def fill_pixels(self, rgb):
		self.iterate_pixels(lambda pixel: pixel.set_rgb(rgb))

	def clear(self):
		self.fill_pixels((0,0,0))
		

	def set_pixels(self, pixels, rgb):
		for pixel in pixels:
			pixel.set_rgb(rgb)

	def set_lamp(self, lamp, rgb):
		self.set_pixels(self.get_lamp(lamp), rgb)

	def set_x(self, x, rgb):
		self.set_pixels(self.get_x(x), rgb)

	def set_y(self, y, rgb):
		self.set_pixels(self.get_y(y), rgb)

	# Channel output for OPC

	def get_channel(self, channel):
		output = []

		for i in range(self.channel_size):
			output.append((0, 0, 0))

		channel_pixels = self.get_pixels(lambda pixel: pixel.channel == channel)

		for pixel in channel_pixels:
			output[pixel.index] = pixel.get_rgb()	

		return output

	def get_output(self):
		output = []

		for i in range(256):
			output.append((0,0,0))

		for channel in range(4):
			channel_pixels = self.get_pixels(lambda pixel: pixel.channel == channel)

			for pixel in channel_pixels:
				output[pixel.index + channel * 64] = pixel.get_rgb()

		return output	


		