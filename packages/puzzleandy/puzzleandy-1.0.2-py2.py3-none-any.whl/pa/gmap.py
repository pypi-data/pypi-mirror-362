from coloraide import Color
import cv2
import numpy as np

def bgr2gray(rgb):
	gray = cv2.cvtColor(rgb,cv2.COLOR_BGR2GRAY)
	return gray

def rgb2bgr(rgb):
	bgr = cv2.cvtColor(rgb,cv2.COLOR_RGB2BGR)
	return bgr

def __gmap(im,interp):
	gray = bgr2gray(im)
	x = np.linspace(0,1,256)
	y = np.empty((256,3),np.uint8)
	for i in range(256):
		rgba_float = np.array(interp(x[i]))
		rgb_float = rgba_float[:3]
		rgb_uint = np.array(rgb_float*255,np.uint8)
		y[i] = rgb_uint
	rgb = y[gray]
	im = rgb2bgr(rgb)
	return im

def black_red(im):
	interp = Color.interpolate([
		'black',
		'red'
		],space='srgb')
	im = __gmap(im,interp)
	return im

def black_teal_white(im):
	interp = Color.interpolate([
		'black',
		Color('hsv',[180,0.18,0.32]),
		Color('hsv',[184,0.16,0.67]),
		'white'
		],space='srgb')
	im = __gmap(im,interp)
	return im

def black_sepia_white(im):
	interp = Color.interpolate([
		'black',
		Color('hsv',[26,0.07,0.31]),
		Color('hsv',[44,0.09,0.65]),
		'white'
		],space='srgb')
	im = __gmap(im,interp)
	return im

def black_pink_white(im):
	interp = Color.interpolate([
		'black',
		Color('hsv',[2,0.23,0.37]),
		Color('hsv',[359,0.16,0.72]),
		'white'
		],space='srgb')
	im = __gmap(im,interp)
	return im

def black_blue_white(im):
	interp = Color.interpolate([
		'black',
		Color('hsv',[211,0.69,0.49]),
		Color('hsv',[209,0.52,0.89]),
		'white'
		],space='srgb')
	im = __gmap(im,interp)
	return im

def black_red_orange(im):
	interp = Color.interpolate([
		'black',
		Color('hsv',[8,0.89,0.87]),
		Color('hsv',[38,0.90,1.00])
		],space='srgb')
	im = __gmap(im,interp)
	return im

def black_green_white(im):
	interp = Color.interpolate([
		'black',
		Color('hsv',[81,0.39,0.32]),
		Color('hsv',[80,0.14,0.65]),
		'white'
		],space='srgb')
	im = __gmap(im,interp)
	return im

def black_purple_white(im):
	interp = Color.interpolate([
		'black',
		Color('hsv',[269,0.23,0.37]),
		Color('hsv',[284,0.11,0.70]),
		'white'
		],space='srgb')
	im = __gmap(im,interp)
	return im

def black_cyan(im):
	interp = Color.interpolate([
		'black',
		Color('hsv',[198,0.82,0.93])
		],space='srgb')
	im = __gmap(im,interp)
	return im

def black_orange(im):
	interp = Color.interpolate([
		'black',
		Color('hsv',[30,1.00,1.00])
		],space='srgb')
	im = __gmap(im,interp)
	return im

def black_magenta(im):
	interp = Color.interpolate([
		'black',
		Color('hsv',[313,1.00,1.00])
		],space='srgb')
	im = __gmap(im,interp)
	return im

def black_yellow(im):
	interp = Color.interpolate([
		'black',
		Color('hsv',[57,1.00,1.00])
		],space='srgb')
	im = __gmap(im,interp)
	return im

def black_blue(im):
	interp = Color.interpolate([
		'black',
		Color('hsv',[202,1.00,0.39]),
		],space='srgb')
	im = __gmap(im,interp)
	return im

def black_blue_white_2(im):
	interp = Color.interpolate([
		'black',
		Color('hsv',[224,0.65,0.58]),
		Color('hsv',[218,0.46,0.91]),
		'white'
		],space='srgb')
	im = __gmap(im,interp)
	return im

def black_green_yellow(im):
	interp = Color.interpolate([
		'black',
		Color('hsv',[118,0.95,0.57]),
		Color('hsv',[68,1.00,1.00])
		],space='srgb')
	im = __gmap(im,interp)
	return im

def black_green(im):
	interp = Color.interpolate([
		'black',
		Color('hsv',[100,1.00,1.00]),
		],space='srgb')
	im = __gmap(im,interp)
	return im

def black_orange_white(im):
	interp = Color.interpolate([
		'black',
		Color('hsv',[10,0.91,0.47]),
		Color('hsv',[28,1.00,0.74]),
		Color('hsv',[44,0.90,0.90]),
		'white'
		],space='srgb')
	im = __gmap(im,interp)
	return im

def black_sepia_white_2(im):
	interp = Color.interpolate([
		'black',
		Color('hsv',[42,0.28,0.31]),
		Color('hsv',[43,0.24,0.56]),
		Color('hsv',[43,0.23,0.82]),
		'white'
		],space='srgb')
	im = __gmap(im,interp)
	return im

def black_yellow_white(im):
	interp = Color.interpolate([
		'black',
		Color('hsv',[49,0.78,0.27]),
		Color('hsv',[49,0.78,0.53]),
		Color('hsv',[49,0.78,0.83]),
		'white'
		],space='srgb')
	im = __gmap(im,interp)
	return im

def black_green_2(im):
	interp = Color.interpolate([
		Color('hsv',[120,1.00,0.02]),
		Color('hsv',[120,0.45,0.28]),
		Color('hsv',[112,0.31,0.56])
		],space='srgb')
	im = __gmap(im,interp)
	return im

def black_blue_purple_magenta(im):
	interp = Color.interpolate([
		'black',
		Color('hsv',[250,0.83,0.41]),
		Color('hsv',[266,0.71,0.53]),
		Color('hsv',[280,0.78,0.75]),
		Color('hsv',[295,1.00,1.00]),
		],space='srgb')
	im = __gmap(im,interp)
	return im

def black_gold_white(im):
	interp = Color.interpolate([
		'black',
		Color('hsv',[51,1.00,0.27]),
		Color('hsv',[51,0.88,0.56]),
		Color('hsv',[51,0.75,0.81]),
		'white'
		],space='srgb')
	im = __gmap(im,interp)
	return im

def black_blue_2(im):
	interp = Color.interpolate([
		'black',
		Color('hsv',[240,1.00,0.63]),
		Color('hsv',[210,1.00,1.00])
		],space='srgb')
	im = __gmap(im,interp)
	return im

def black_chartreuse(im):
	interp = Color.interpolate([
		'black',
		Color('hsv',[74,1.00,0.43]),
		Color('hsv',[66,0.82,0.89])
		],space='srgb')
	im = __gmap(im,interp)
	return im

def black_brown_chartreuse_white(im):
	interp = Color.interpolate([
		'black',
		Color('hsv',[37,1.00,0.32]),
		Color('hsv',[64,1.00,0.49]),
		Color('hsv',[59,0.99,0.74]),
		'white',
		],space='srgb')
	im = __gmap(im,interp)
	return im

def black_cyan_white(im):
	interp = Color.interpolate([
		'black',
		Color('hsv',[192,1.00,0.33]),
		Color('hsv',[190,0.94,0.61]),
		Color('hsv',[187,0.35,0.80]),
		'white',
		],space='srgb')
	im = __gmap(im,interp)
	return im

def black_cyan_2(im):
	interp = Color.interpolate([
		'black',
		Color('hsv',[180,0.48,0.61])
		],space='srgb')
	im = __gmap(im,interp)
	return im

def black_red_blue_beige(im):
	interp = Color.interpolate([
		'black',
		Color('hsv',[354,0.81,0.46]),
		Color('hsv',[187,0.81,0.60]),
		Color('hsv',[42,0.24,0.81])
		],space='srgb')
	im = __gmap(im,interp)
	return im