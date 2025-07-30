from math import ceil, fabs 
from collections import deque
import time

from numpy import arange

from lgbt.consts import COLS, upper_bound, paint, cursor
from lgbt.basicobjects import ConsoleObject


class DrawLimiter():
	def __init__(self, interval):
		self._interval = interval
		self._last_update = None
	
	def __call__(self, func):
		def wrapper(*args, **kwargs):
			if self._last_update == None:
				self._last_update = time.perf_counter()
			
			interval = time.perf_counter() - self._last_update
			if interval > self._interval:
				self._last_update = time.perf_counter()
				func(*args, **kwargs)
				return

		return wrapper

class Histogram(ConsoleObject):
	def __init__(self, size=(5,14), gap=' ', max_value=0.5, fix=True, coord=(1,1)):
		super(Histogram, self).__init__(coord=coord)
		self._size = size
		self._fix = fix
		self._max_value = max_value
		self._gap = gap
		self._table = deque([[" "]*self._size[0]] * self._size[1], maxlen=self._size[1])  
		self._colours = deque(['RED'] * self._size[1], maxlen=self._size[1])
		self._last_values = deque([0.0] * self._size[1], maxlen=self._size[1])
		self._current_column = 0
		self._y_label = [0.0] * self._size[0] 
		self._update_y_label()

	def _update_y_label(self):
		self._y_label[:] = map(lambda x: f'{x:.2} ', arange(0.0, self._max_value, self._max_value / self._size[0]).tolist())
		self._y_label.reverse()

	def _advanced_join(self, iterable):
		str_iterable = [str(item) for item in iterable]
		if not str_iterable:
			return ""
		
		parts = []
		parts.append(self._paint(str=str_iterable[0],index=0))
		for i in range(1, len(str_iterable)):
			parts.append(self._gap)
			parts.append(self._paint(str=str_iterable[i], index=i))
		return "".join(parts)

	def _paint(self, str, index):
		return paint(str=str, color=self._colours[index], count=1)

	def draw(self):
		self.cursor(1,1)
		result = list(zip(*list(self._table)))
		for i in range(len(result)):
			self.cursor(self._coord[0], self._coord[1]+i)
			self.put_in_buffer(self._advanced_join(result[i]))

	def update(self, value):
		self._colours[self._current_column] = 'RED' if value > 0 else 'BLUE'
		value = fabs(value)
		if (value > self._max_value):
			if not self._fix:
				self._max_value *= 2
				self._update_y_label()
				for i in range(self._current_column):
					self._table[i] = self._create_column(self._last_values[i])
			else:
				value = self._max_value
	
		self._last_values[self._current_column] = value	
		self._table[self._current_column] = self._create_column(value)
		
	def _create_column(self, y):
		steps_length = self._max_value / self._size[0]

		k = y / steps_length

		up_bound = ceil(k)
		low_bound = int(k)

		if up_bound == low_bound:
			return (" " * (self.size[0] - low_bound)) + (COLS[1.0] * low_bound)  
		else:
			return (" " * (self.size[0] - up_bound) ) + (upper_bound(k - low_bound)) + (COLS[1.0] * low_bound)
		
	def next(self):
		if self._current_column < self._size[1] - 1:
			self._current_column += 1
		else:
			self._table.append([[" "]*self._size[0]])
			self._last_values.append(0.0) 
			self._colours.append('RED')
		

	@property
	def y_label(self):
		return self._y_label

	@property
	def coord(self):
		return self._coord

	@coord.setter	
	def coord(self, coord):
		self._coord = coord	
	
	@property
	def size(self):
		n = len(self._gap)
		return (self._size[0], (self._size[1] * (1 + n)) - n)

	@size.setter
	def size(self, value):
		self._size = value

class Window(ConsoleObject):
	def __init__(self, obj, coord=(1,1)):
		super(Window, self).__init__(coord=coord)
		self._size = ( obj.size[0], obj.size[1] + 2 )
		self._obj = obj
		self._obj.coord = (self._coord[0] + 6, self._coord[1] + 1)
		if not hasattr(obj, "draw") or not hasattr(obj, "update"): 
			raise ValueError("Invalid object to draw in Window")
	
	@DrawLimiter(0.1)
	def draw(self):
		y_label = self._obj.y_label

		left =  '┌' + ( '│' * self._size[0]) + '└'
		middle = [ '─'+ ( ' ' * self._size[0]) + '─'] * (self._size[1])
		right =  '┐' + ( '│' * self._size[0]) + '┘'

		bounds = [left, *middle, right]
		result_bounds = list(zip(*bounds))
		result_y_label = list(zip(*[y_label]))

		for i in range(len(result_y_label)):
			self.cursor(self._coord[0], self._coord[1] + 1 + i)
			self.put_in_buffer(''.join(result_y_label[i]))

		for i in range(len(result_bounds)):
			self.cursor(self._coord[0]+4, self._coord[1] + i)
			self.put_in_buffer(''.join(result_bounds[i]))
		
		self._obj.draw()
		self._obj.flush(self._buffer)

	def update(self, value):
		self._obj.update(value)

	@DrawLimiter(0.1)
	def next(self):
		self._obj.next()

	@property
	def coord(self):
		return self._coord	

	@coord.setter
	def coord(self, value):
		self._coord = value
		self._obj.coord = (self._coord[0] + 6, self._coord[1] + 1)

	@property
	def size(self):
		return (self._size[0] + 2, self._size[1] + 6)

	@size.setter
	def size(self, value):
		self._size = value
