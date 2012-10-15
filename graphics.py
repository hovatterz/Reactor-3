from libtcodpy import *
from globals import *
from tiles import *
import numpy

def init_libtcod():
	console_init_root(WINDOW_SIZE[0],WINDOW_SIZE[1],WINDOW_TITLE,renderer=RENDERER)
	console_set_custom_font(FONT,FONT_LAYOUT)
	sys_set_fps(FPS)

	RGB_BACK_BUFFER[0] = numpy.zeros((WINDOW_SIZE[1],WINDOW_SIZE[0]))
	RGB_BACK_BUFFER[1] = numpy.zeros((WINDOW_SIZE[1],WINDOW_SIZE[0]))
	RGB_BACK_BUFFER[2] = numpy.zeros((WINDOW_SIZE[1],WINDOW_SIZE[0]))
	RGB_FORE_BUFFER[0] = numpy.zeros((WINDOW_SIZE[1],WINDOW_SIZE[0]))
	RGB_FORE_BUFFER[1] = numpy.zeros((WINDOW_SIZE[1],WINDOW_SIZE[0]))
	RGB_FORE_BUFFER[2] = numpy.zeros((WINDOW_SIZE[1],WINDOW_SIZE[0]))
	CHAR_BUFFER[0] = numpy.zeros((WINDOW_SIZE[1],WINDOW_SIZE[0]))

def start_of_frame():
	console_fill_background(0,RGB_BACK_BUFFER[0],RGB_BACK_BUFFER[1],RGB_BACK_BUFFER[2])
	console_fill_foreground(0,RGB_FORE_BUFFER[0],RGB_FORE_BUFFER[1],RGB_FORE_BUFFER[2])
	console_fill_char(0,CHAR_BUFFER[0])

def blit_tile(x,y,tile):
	_tile = get_tile(tile)

	blit_char(x,y,_tile['icon'],_tile['color'][0],_tile['color'][1])

def blit_char(x,y,char,fore_color=None,back_color=None):
	if fore_color:
		RGB_FORE_BUFFER[0][y,x] = fore_color.r
		RGB_FORE_BUFFER[1][y,x] = fore_color.g
		RGB_FORE_BUFFER[2][y,x] = fore_color.b

	if back_color:
		RGB_BACK_BUFFER[0][y,x] = back_color.r
		RGB_BACK_BUFFER[1][y,x] = back_color.g
		RGB_BACK_BUFFER[2][y,x] = back_color.b

	CHAR_BUFFER[0][y,x] = ord(char)

def blit_string(x,y,text):
	console_print(0,x,y,text)

def darken_tile(x,y,amt):
	for r in range(3):
		if RGB_FORE_BUFFER[r][y,x]-amt<0:
			RGB_FORE_BUFFER[r][y,x] = 0
		else:
			RGB_FORE_BUFFER[r][y,x] -= amt

		if RGB_BACK_BUFFER[r][y,x]-amt<0:
			RGB_BACK_BUFFER[r][y,x] = 0
		else:
			RGB_BACK_BUFFER[r][y,x] -= amt

def lighten_tile(x,y,amt):
	for r in range(3):
		if RGB_FORE_BUFFER[r][y,x]+amt>255:
			RGB_FORE_BUFFER[r][y,x] = 255
		else:
			RGB_FORE_BUFFER[r][y,x] += amt

		if RGB_BACK_BUFFER[r][y,x]+amt>255:
			RGB_BACK_BUFFER[r][y,x] = 255
		else:
			RGB_BACK_BUFFER[r][y,x] += amt

def end_of_frame():
	console_flush()

def window_is_closed():
	return console_is_window_closed()