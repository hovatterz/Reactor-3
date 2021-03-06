from copy import deepcopy
from globals import *

import zones as zns
import life as lfe

import render_los
import numbers
import zones
import alife
import numpy
import tiles

import logging
import time
import sys

def astar(life, start, end, zones, chunk_mode=False, map_size=MAP_SIZE):
	_stime = time.time()
	
	_path = {'start': tuple(start),
	         'end': tuple(end),
	         'olist': [tuple(start)],
	         'clist': [],
	         'segments': [],
	         'map': [],
	         'map_size': map_size,
	         'chunk_mode': chunk_mode}
	
	if chunk_mode:
		_path['start'] = (_path['start'][0]/WORLD_INFO['chunk_size'], _path['start'][1]/WORLD_INFO['chunk_size'])
		_path['end'] = (_path['end'][0]/WORLD_INFO['chunk_size'], _path['end'][1]/WORLD_INFO['chunk_size'])
		_path['olist'][0] = (_path['start'][0], _path['start'][1])

	_path['fmap'] = numpy.zeros((_path['map_size'][1], _path['map_size'][0]), dtype=numpy.int16)
	_path['gmap'] = numpy.zeros((_path['map_size'][1], _path['map_size'][0]), dtype=numpy.int16)
	_path['hmap'] = numpy.zeros((_path['map_size'][1], _path['map_size'][0]), dtype=numpy.int16)
	_path['pmap'] = []
	_path['tmap'] = numpy.zeros((_path['map_size'][0], _path['map_size'][1]), dtype=numpy.int16)
	
	for x in range(_path['map_size'][0]):
		_path['pmap'].append([0] * _path['map_size'][1])

	_path['map'] = numpy.zeros((_path['map_size'][1], _path['map_size'][0]))
	_path['map'] -= 2
	
	#KEY:
	#0: Unwalkable
	#1: Walkable
	
	for zone in [zns.get_slice(z) for z in zones]:
		for _open_pos in zone['map']:
			if chunk_mode:
				_path['map'][_open_pos[1]/WORLD_INFO['chunk_size'], _open_pos[0]/WORLD_INFO['chunk_size']] = 1
			else:
				_path['map'][_open_pos[1], _open_pos[0]] = 1
	
	_path['hmap'][_path['start'][1], _path['start'][0]] = (abs(_path['start'][0]-_path['end'][0])+abs(_path['start'][1]-_path['end'][1]))*10
	_path['fmap'][_path['start'][1], _path['start'][0]] = _path['hmap'][_path['start'][1],_path['start'][0]]

	return walk_path({}, _path)

def walk_path(life, path):
	if path['map'][path['end'][1], path['end'][0]] == -2:
		logging.warning('Pathfinding: Attempted to create path ending in an unpathable area.')

		return False

	node = path['olist'][0]

	_clist = path['clist']
	_olist = path['olist']
	_gmap = path['gmap']
	_hmap = path['hmap']
	_fmap = path['fmap']
	_pmap = path['pmap']
	_stime = time.time()

	while len(_olist):
		_olist.remove(node)

		if tuple(node) == path['end']:
			_olist = []
			break

		_clist.append(node)
		_lowest = {'pos': None, 'f': 9000}

		for adj in getadj(path, node):
			if not adj in _olist:
				if abs(node[0]-adj[0])+abs(node[1]-adj[1]) == 1:
					_gmap[adj[1],adj[0]] = _gmap[node[1],node[0]]+10
				else:
					_gmap[adj[1],adj[0]] = _gmap[node[1],node[0]]+14

				xDistance = abs(adj[0]-path['end'][0])
				yDistance = abs(adj[1]-path['end'][1])
				if xDistance > yDistance:
					_hmap[adj[1],adj[0]] = 14*yDistance + 10*(xDistance-yDistance)
				else:
					_hmap[adj[1],adj[0]] = 14*xDistance + 10*(yDistance-xDistance)

				_fmap[adj[1],adj[0]] = _gmap[adj[1],adj[0]]+_hmap[adj[1],adj[0]]
				_pmap[adj[0]][adj[1]] = node

				_olist.append(adj)

		for o in _olist:			
			if _fmap[o[1],o[0]] < _lowest['f']:
				_lowest['pos'] = o
				_lowest['f'] = _fmap[o[1],o[0]]

		if _lowest['pos']:
			node = _lowest['pos']

	return find_path(path)

def getadj(path, pos, checkclist=True):
	adj = []

	for r in [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]:
		_x = pos[0]+r[0]
		_y = pos[1]+r[1]

		if _x<0 or _x>=path['map_size'][0] or _y<0 or _y>=path['map_size'][1] or path['map'][_y,_x]==-2:
			continue

		if (_x,_y) in path['clist'] and checkclist:
			continue

		adj.append((_x,_y))

	return adj

def find_path(path):
	if path['map'][path['end'][1], path['end'][0]] == -2:
		return [[path['start'][0], path['start'][1], 0]]

	node = path['pmap'][path['end'][0]][path['end'][1]]
	_path = [[path['end'][0],path['end'][1],int(path['map'][path['end'][1],path['end'][0]])]]
	_broken = False
	
	while not tuple(node) == tuple(path['start']):
		#print 'iter', node, path['start'], path['end'], path['chunk_mode']
		if not node:
			_broken = True
			break
		else:
			_path.insert(0,(node[0], node[1], int(path['map'][node[1], node[0]])))

		path['tmap'][node[0]][node[1]] = 1
		node = path['pmap'][node[0]][node[1]]

	return _path

def short_path(life, start, end):
	_s = time.time()
	_line = render_los.draw_line(start[0], start[1], end[0], end[1])
	
	if numbers.distance(start, end)>30:
		return False
	
	if not _line:
		return [start]
	
	_line.pop(0)
	
	for pos in _line:
		if not lfe.can_traverse(life, pos):
			return False
	
	return _line

def chunk_path(life, start, end, zones):
	return astar(life, start, end, zones, map_size=(MAP_SIZE[0]/WORLD_INFO['chunk_size'], MAP_SIZE[1]/WORLD_INFO['chunk_size']), chunk_mode=True)

def walk_chunk_path(life):
	_existing_chunk_path = alife.brain.get_flag(life, 'chunk_path')
	
	if _existing_chunk_path['path']:
		_next_chunk = _existing_chunk_path['path'].pop(0)
		_next_pos = WORLD_INFO['chunk_map']['%s,%s' % (_next_chunk[0]*WORLD_INFO['chunk_size'], _next_chunk[1]*WORLD_INFO['chunk_size'])]['pos']
		
		return create_path(life, life['pos'], _next_pos, _existing_chunk_path['zones'], ignore_chunk_path=True)
	else:
		alife.brain.unflag(life, 'chunk_path')

def create_path(life, start, end, zones, ignore_chunk_path=False):
	if not ignore_chunk_path:
		_existing_chunk_path = alife.brain.get_flag(life, 'chunk_path')
		
		if _existing_chunk_path:
			return walk_chunk_path(life)
		
	_shortpath = short_path(life, start, end)
	if _shortpath:
		return _shortpath
	
	if len(zones) == 1 and (numbers.distance(start, end) >= 100 and not ignore_chunk_path):
		_chunk_path = {'path': chunk_path(life, start, end, zones),
		               'start': start,
		               'end': end,
		               'zones': zones}
		alife.brain.flag(life, 'chunk_path', _chunk_path)
		_next_pos = _chunk_path['path'][0][:2]
		_next_pos = (_next_pos[0]*WORLD_INFO['chunk_size'], _next_pos[1]*WORLD_INFO['chunk_size'])
		
		return astar(life, start, _next_pos, zones)
	
	return astar(life, start, end, zones)