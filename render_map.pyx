from graphics import blit_tile, darken_tile, blit_char, blit_tile, get_view_by_name
from globals import MAP_CHAR_BUFFER, DARK_BUFFER
from tiles import *

import libtcodpy as tcod

import effects
import numpy
import tiles
import alife
import time

VERSION = 6

def render_map(map):
	cdef int _CAMERA_POS[2]
	cdef int _MAP_SIZE[2]
	cdef int _MAP_WINDOW_SIZE[2]
	_CAMERA_POS[0] = CAMERA_POS[0]
	_CAMERA_POS[1] = CAMERA_POS[1]
	_CAMERA_POS[2] = CAMERA_POS[2]
	_MAP_SIZE[0] = MAP_SIZE[0]
	_MAP_SIZE[1] = MAP_SIZE[1]
	_MAP_SIZE[2] = MAP_SIZE[2]
	_MAP_WINDOW_SIZE[0] = MAP_WINDOW_SIZE[0]
	_MAP_WINDOW_SIZE[1] = MAP_WINDOW_SIZE[1]
	
	cdef int x, y, z
	cdef int _X_MAX = _CAMERA_POS[0]+_MAP_WINDOW_SIZE[0]
	cdef int _Y_MAX = _CAMERA_POS[1]+_MAP_WINDOW_SIZE[1]
	cdef int _X_START = _CAMERA_POS[0]
	cdef int _Y_START = _CAMERA_POS[1]
	cdef int _RENDER_X = 0
	cdef int _RENDER_Y = 0
	
	_view = get_view_by_name('map')
	_TEMP_MAP_CHAR_BUFFER = _view['char_buffer'][1].copy()

	if _X_MAX>_MAP_SIZE[0]:
		_X_MAX = _MAP_SIZE[0]

	if _Y_MAX>_MAP_SIZE[1]:
		_Y_MAX = _MAP_SIZE[1]

	for x in range(_X_START,_X_MAX):
		_RENDER_X = x-_CAMERA_POS[0]
		for y in range(_Y_START,_Y_MAX):
			_RENDER_Y = y-_CAMERA_POS[1]
			
			if _TEMP_MAP_CHAR_BUFFER[_RENDER_Y,_RENDER_X]:
				continue
			
			DARK_BUFFER[0][_RENDER_Y, _RENDER_X] = 0
			
			_drawn = False
			_shadow = 2
			for z in range(MAP_SIZE[2]-1,-1,-1):
				if map[x][y][z]:
					if z > _CAMERA_POS[2] and SETTINGS['draw z-levels above']:
						if 'translucent' in tiles.get_raw_tile(tiles.get_tile((x, y, z))):
							if _shadow >= 2:
								_shadow += 1
						else:
							_shadow = 0
							
						if not LOS_BUFFER[0][_RENDER_Y,_RENDER_X]:
							blit_tile(_RENDER_X, _RENDER_Y, map[x][y][z], 'map')
							darken_tile(_RENDER_X, _RENDER_Y, abs((_CAMERA_POS[2]-z))*10)
							_drawn = True
					elif z == _CAMERA_POS[2]:
						if (x,y,z) in SELECTED_TILES[0] and time.time()%1>=0.5:
							blit_char(_RENDER_X,
								_RENDER_Y,
								'X',
								tcod.darker_grey,
								tcod.black,
								char_buffer=MAP_CHAR_BUFFER,
								rgb_fore_buffer=MAP_RGB_FORE_BUFFER,
								rgb_back_buffer=MAP_RGB_BACK_BUFFER)
						else:
							if _shadow > 2:
								darken_tile(_RENDER_X, _RENDER_Y, 15*(_shadow-2))
							
							blit_tile(_RENDER_X, _RENDER_Y, map[x][y][z], 'map')
							
							if SETTINGS['draw effects']:
								if LOS_BUFFER[0][_RENDER_Y,_RENDER_X]:
									effects.draw_splatter((x,y,z), (_RENDER_X,_RENDER_Y))
									effects.draw_effect((x, y))
						
						if not LOS_BUFFER[0][_RENDER_Y,_RENDER_X]:
							darken_tile(_RENDER_X, _RENDER_Y, 30)
						
						if SETTINGS['draw visible chunks']:
							_visible_chunks = alife.brain.get_flag(LIFE[SETTINGS['controlling']], 'visible_chunks')
							
							if _visible_chunks:
								for _chunk in _visible_chunks:
									if alife.chunks.position_is_in_chunk((x, y), _chunk):
										darken_tile(_RENDER_X, _RENDER_Y, abs(90))
									
						_drawn = True
					elif z < _CAMERA_POS[2] and SETTINGS['draw z-levels below']:
						blit_tile(_RENDER_X,_RENDER_Y,map[x][y][z], 'map')
						darken_tile(_RENDER_X,_RENDER_Y,abs((_CAMERA_POS[2]-z))*10)
						_drawn = True
				
					if SETTINGS['draw z-levels above'] and _drawn:
						break
			
			if not _drawn:
				blit_tile(_RENDER_X, _RENDER_Y, BLANK_TILE, 'map')
