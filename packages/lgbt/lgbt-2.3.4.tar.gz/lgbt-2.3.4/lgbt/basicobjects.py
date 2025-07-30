from abc import ABC, abstractmethod
import time
import os
import psutil
import threading
import sys

import GPUtil
from cpuinfo import get_cpu_info

from lgbt.consts import SHORT_FLAGS,BIG_FLAGS, HAND_KEYS, HEROES

class Anim():
	def __init__(self, list_anim):
		self.anim = list_anim
		self.n = len(self.anim)

	def __call__(self, iter):
		return self.anim[int(iter)%self.n]

class ConsoleObject():
	def __init__(self, coord=(1,1)):
		self._coord = coord
		self._time = None
		self._value = None
		self._buffer = []

	@property
	def time(self):
		return self._time
	
	@time.setter
	def time(self, value):
		self._time = value

	@property
	def coord(self):
		return self._coord
	
	@coord.setter
	def coord(self, value):
		self._coord = value

	@abstractmethod
	def draw(self):
		pass

	@abstractmethod
	def update(self, value):
		if self._time == None:
			self._time = time.perf_counter()
		self._value = value
		
	def cursor(self, column, row):
		self._buffer.append(f"\033[{row};{column}H")

	def put_in_buffer(self, value):
		self._buffer.append(value)

	def flush(self, buffer=None):
		if buffer == None:
			sys.stdout.write("".join(self._buffer))
			sys.stdout.flush()
			self._buffer.clear()
		else:
			buffer.extend(self._buffer)
			self._buffer.clear()
		

class TextLabel(ConsoleObject):
	def __init__(self, desc, hero='rainbow', n=10, coord=(1, 1)):
		super(TextLabel, self).__init__(coord)
		self._desc = desc
		self._hero = HEROES[hero]
		self._n = n
		self._update_func = None
		self._anim = None
		self._value = 0
		if n < len(self._desc):
			self._anim = Anim(self._create_string_anim(self._desc)) 
			self._update_func = lambda: self._anim(self._value)[:self._n]
		else:
			self._update_func = lambda: self._desc + (" " * (self._n - len(self._desc)))

	def _rotate_left(self, s, n):
		n = n % len(s)  
		return s[n:] + s[:n]

	def _create_string_anim(self, str):
		ext_str = str + (" " * len(str))
		anim = []
		for i in range(len(ext_str)):
			anim.append(self._rotate_left(ext_str, i))

		return anim
	
	@property
	def desc(self):
		return self._hero + " " + self._update_func()

	@desc.setter
	def desc(self, value):
		self._desc = value
		if self._n < len(self._desc):
			self._anim = Anim(self._create_string_anim(self._desc)) 
			self._update_func = lambda: self._anim(self._value)[:self._n]
		else:
			self._update_func = lambda: self._desc + (" " * (self._n - len(self._desc)))

	def draw(self):
		self.cursor(self._coord[0], self._coord[1])
		self.put_in_buffer(self._hero + " ")
		self.put_in_buffer(self._update_func())

	def update(self, value):
		super().update(value)
		
	def __len__(self):
		return self._n + 2
	
class Bar(ConsoleObject):
	def __init__(self, total, mode, type='long', coord=(1, 1)):
		super(Bar, self).__init__(coord)
		self._bar = SHORT_FLAGS[mode].split(HAND_KEYS['RESET']) if type == 'short' else BIG_FLAGS[mode].split(HAND_KEYS['RESET'])
		self._bar.pop()
		self._bar_width = 63 if type == 'long' else 21
		self._part_bars = []
		self._total = total
		self._start_time = None
		self._value = None
		self._stats = {
			"percent" : 0.0,
			"filled" : 0
			}
		
		self._fill_bar()
	
	def _fill_bar(self):
		n = len(self._bar)
		curr_str = ""
		for i, simb in enumerate(self._bar, 1):
			curr_str += simb
			self._part_bars.append((curr_str + HAND_KEYS['RESET']) + (" " * (n - i)) )

	def _translate_count(self, iter):
		if iter >= 1000000:
			return f'{iter/1000000:.0f}M'
		if iter >= 1000:
			return f'{iter/1000:.0f}K'
		return f'{iter:.0f}'
	
	def _translate_time(self, sec):
		total_seconds = int(sec)
		if total_seconds > 3600:
			hours = total_seconds // 3600
			remaining_seconds = total_seconds % 3600
			minutes = remaining_seconds // 60
			seconds = remaining_seconds % 60
			return f'{hours}:{minutes:02}:{seconds:02}'
		else:
			seconds = total_seconds % 60
			minutes = total_seconds // 60
			return f'{minutes:02}:{seconds:02}'
	
	def update(self, value):
		super().update(value)
		self._stats['percent'] = (self._value / self._total) * 100  
		self._stats['filled']  = round(self._value / self._total * (len(self._bar)-1))

	def draw(self):
		self.cursor(self._coord[0], self._coord[1])
		percent = self._stats['percent'] 
		filled = self._stats['filled']
		self.put_in_buffer(f"{percent:03.0f}% {self._part_bars[filled]}")		

	def __len__(self):
		return self._bar_width + 5

class ClassicBar(Bar):
	def __init__(self, total, mode, type='long', coord=(1, 1)):
		super(ClassicBar, self).__init__(total=total, mode=mode, type=type, coord=coord)
		self._stats.update({
			'passed_time':0.0,
			'remaining_time' : 0.0,
			'speed' : 0.0,
			'current_iter': 0,
			'total_iter' : self._total
			})

	def draw(self):
		super().draw()
		shift = super().__len__()
		self.cursor(self.coord[0]+shift + 2, self.coord[1])
		passed_time = self._translate_time(self._stats['passed_time'])
		remaining_time = self._translate_time(self._stats['remaining_time'])
		speed =  self._translate_count(self._stats['speed'])
		current_iter = self._translate_count(self._stats['current_iter'])
		total = self._translate_count(self._stats['total_iter'])
		self.put_in_buffer(f"[{current_iter}/{total}, {passed_time}<{remaining_time}, {speed}it/s]{HAND_KEYS['CLEAN']}")

	def update(self, value):
		super().update(value)
		self._stats['passed_time'] = time.perf_counter() - self._time
		self._stats['speed'] = self._value / self._stats['passed_time']
		self._stats['remaining_time'] = (self._total - self._value) / self._stats['speed'] 
		self._stats['current_iter'] = self._value

class LegacyBar(ClassicBar):
	def __init__(self, total, desc="", hero='rainbow', mode='default', type='long', coord=(1, 1)):
		super().__init__(total, mode, type, coord)
		self._text_label = TextLabel(desc=desc, hero=hero)

	def draw(self):
		desc = self._text_label.desc
		percent = self._stats['percent']
		filled = self._stats['filled']
		passed_time = self._translate_time(self._stats['passed_time'])
		remaining_time = self._translate_time(self._stats['remaining_time'])
		speed =  self._translate_count(self._stats['speed'])
		current_iter = self._translate_count(self._stats['current_iter'])
		total = self._translate_count(self._stats['total_iter'])
		self.put_in_buffer(f"\r{desc}{percent:03.0f}% {self._part_bars[filled]} {current_iter}/{total} [{passed_time}<{remaining_time}, {speed}it/s]{HAND_KEYS['CLEAN']}")

	def update(self, value):
		super().update(value)
		anim_speed = (time.perf_counter() - self._time) * 10
		self._text_label.update(anim_speed)

class GPUBar(Bar):
	def __init__(self, total=100, mode='nvidia', type='short', coord=(1, 1), device_id=0):
		super(GPUBar, self).__init__(100, 'nvidia', 'short', coord)
		self._stop_event = threading.Event()

		self._device_id = device_id
		self._gpu = GPUtil.getGPUs()[self._device_id]
		self._stats.update({
 	       "gpu_percent": self._gpu.load * 100,
 	       "mem_used": self._gpu.memoryUsed,  
 	       "mem_total": self._gpu.memoryTotal, 
		})

		threading.Thread(target=self._background_update, daemon=True).start()

	def _background_update(self):
		while not self._stop_event.is_set():
			self._gpu = GPUtil.getGPUs()[self._device_id]
			time.sleep(1)

	def __del__(self):
		self._stop_event.set()

	def update(self, value=None):
		self._stats["gpu_percent"] = self._gpu.load * 100
		self._stats["mem_used"] = self._gpu.memoryUsed
		super().update(self._stats["gpu_percent"])
	
	def draw(self):
		super().draw()
		shift = super().__len__()
		self.cursor(self.coord[0]+shift+2, self.coord[1])
		self.put_in_buffer(f"[{self._stats['mem_used']:.0f}/{self._stats['mem_total']:.0f}MB]{HAND_KEYS['CLEAN']}")

class CPUBar(Bar):
	def __init__(self,  mode='default', type='short', coord=(1, 1), total=100):
		self._brand = 'intel' if 'Intel' in get_cpu_info()['brand_raw'] else 'amd'
		super(CPUBar, self).__init__(100, self._brand, 'short', coord)

		self._stop_event = threading.Event()
		self._pid = os.getpid()
		self._process = psutil.Process(self._pid)
		self._cpu_cores = psutil.cpu_count(logical=True)
		self._stats.update({
			'process_cpu' : 0.0,
			'mem_total' :  psutil.virtual_memory().total,
			'mem_used' : psutil.virtual_memory().used})
		
		threading.Thread(target=self._background_update, daemon=True).start()

	def _background_update(self):
		while not self._stop_event.is_set():
			self._stats['process_cpu'] = self._process.cpu_percent(interval=1) / self._cpu_cores
	
	def __del__(self):
		self._stop_event.set()

	def update(self, value=None):
		self._stats['mem_used'] = psutil.virtual_memory().used
		super().update(self._stats['process_cpu'])

	def draw(self):
		super().draw()
		shift = super().__len__()
		self.cursor(self.coord[0]+shift+2, self.coord[1])
		self.put_in_buffer(f"[{self._stats['mem_used']/ (1024**2):.0f}/{self._stats['mem_total']/(1024**2):.0f}MB]{HAND_KEYS['CLEAN']}")

class Tracker:
	def __init__(self, number=None):
		if type(number) in [float, int, type(None)]:
			self._number = number
		elif type(number) == type(self):
			self = number
		else:
			raise ValueError("Not correct type of variable")

	@property
	def item(self):
		return self._number
	
	@item.setter
	def item(self, value):
		if type(value) in [float, int, type(None)]:
			self._number = value
		elif type(value) == type(self):
			self = value
		else:
			raise ValueError("Not correct type of variable")

	
	def __str__(self):
		return str(self._number)
	
	def __add__(self, value):
		if type(value) == type(self):
			return Tracker(self._number + value.item())
		elif type(value) in [float, int]:
			return Tracker(self._number + value)
		else:
			raise ValueError("Not correct type of variable")
		
	def __sub__(self, value):
		if type(value) == type(self):
			return Tracker(self._number - value.item())
		elif type(value) in [float, int]:
			return Tracker(self._number - value)
		else:
			raise ValueError("Not correct type of variable")
		
	def __mul__(self, value):
		if type(value) == type(self):
			return Tracker(self._number * value.item())
		elif type(value) in [float, int]:
			return Tracker(self._number * value)
		else:
			raise ValueError("Not correct type of variable")
		
	def __truediv__(self, value):
		if type(value) == type(self):
			return Tracker(self._number / value.item())
		elif type(value) in [float, int]:
			return Tracker(self._number / value)
		else:
			raise ValueError("Not correct type of variable")
		
	def __floordiv__(self, value):
		if type(value) == type(self):
			return Tracker(self._number // value.item())
		elif type(value) in [float, int]:
			return Tracker(self._number // value)
		else:
			raise ValueError("Not correct type of variable")
		
	def __mod__(self, value):
		if type(value) == type(self):
			return Tracker(self._number % value.item())
		elif type(value) in [float, int]:
			return Tracker(self._number % value)
		else:
			raise ValueError("Not correct type of variable")
		
	def __pow__(self, value):
		if type(value) == type(self):
			return Tracker(self._number ** value.item())
		elif type(value) in [float, int]:
			return Tracker(self._number ** value)
		else:
			raise ValueError("Not correct type of variable")
		
	def __eq__(self, value):
		if type(value) == type(self):
			return self._number == value.item()
		elif type(value) in [float, int, type(None)]:
			return self._number == value
		else:
			raise ValueError("Not correct type of variable")

	def __ne__(self, value):
		if type(value) == type(self):
			return self._number != value.item()
		elif type(value) in [float, int, type(None)]:
			return self._number != value
		else:
			raise ValueError("Not correct type of variable")
		
	def __lt__(self, value):
		if type(value) == type(self):
			return self._number < value.item()
		elif type(value) in [float, int]:
			return self._number < value
		else:
			raise ValueError("Not correct type of variable")

	def __gt__(self, value):
		if type(value) == type(self):
			return self._number > value.item()
		elif type(value) in [float, int]:
			return self._number > value
		else:
			raise ValueError("Not correct type of variable")
	
	def __le__(self, value):
		if type(value) == type(self):
			return self._number <= value.item()
		elif type(value) in [float, int]:
			return self._number <= value
		else:
			raise ValueError("Not correct type of variable")
		
	def __ge__(self, value):
		if type(value) == type(self):
			return self._number >= value.item()
		elif type(value) in [float, int]:
			return self._number >= value
		else:
			raise ValueError("Not correct type of variable")
		
	def __iadd__(self, value):
		if type(value) == type(self):
			self._number += value.item()
			return self
		elif type(value) in [float, int]:
			self._number += value
			return self
		else:
			raise ValueError("Not correct type of variable")
		
	def __isub__(self, value):
		if type(value) == type(self):
			self._number -= value.item()
			return self
		elif type(value) in [float, int]:
			self._number -= value
			return self
		else:
			raise ValueError("Not correct type of variable")
		
	def __imul__(self, value):
		if type(value) == type(self):
			self._number *= value.item()
			return self
		elif type(value) in [float, int]:
			self._number *= value
			return self
		else:
			raise ValueError("Not correct type of variable")
		
	def __itruediv__(self, value):
		if type(value) == type(self):
			self._number /= value.item()
			return self
		elif type(value) in [float, int]:
			self._number /= value
			return self
		else:
			raise ValueError("Not correct type of variable")
		
	def __ifloordiv__(self, value):
		if type(value) == type(self):
			self._number //= value.item()
			return self
		elif type(value) in [float, int]:
			self._number //= value
			return self
		else:
			raise ValueError("Not correct type of variable")
		
	def __ipow__(self, value):
		if type(value) == type(self):
			self._number **= value.item()
			return self
		elif type(value) in [float, int]:
			self._number **= value
			return self
		else:
			raise ValueError("Not correct type of variable")
		
	def __pos__(self):
		self._number = +self._number
		return self
	
	def __neg__(self):
		self._number = -self._number
		return self

	def __abs__(self):
		return +self