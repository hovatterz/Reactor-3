from globals import *
import life as lfe

import references
import judgement
import movement
import chunks
import speech

import numbers
import random
import combat
import items
import brain
import sight
import maps
import time

def loot(life):
	#What do we need to do?
	#	- Get items?
	#	- Find shelter?
	
	manage_hands(life)
	
	if brain.get_flag(life, 'no_weapon'):
		_nearby_weapons = sight.find_known_items(life, matches=[{'type': 'gun'}])
		
		if _nearby_weapons:
			movement.collect_nearby_wanted_items(life, matches=[{'type': 'gun'}])
			
			for ai in [life['know'][i] for i in life['know']]:
				if ai['score']<=0:
					continue
				
			return True
	
	elif not brain.get_flag(life, 'no_weapon'):
		_ammo_matches = []
		_feed_matches = []
		for weapon in combat.has_weapon(life):
			_ammo_matches.append({'type': 'bullet','ammotype': weapon['ammotype']})
			_feed_matches.append({'type': weapon['feed'],'ammotype': weapon['ammotype']})
		
		if sight.find_known_items(life, matches=_ammo_matches):
			movement.collect_nearby_wanted_items(life, matches=_ammo_matches)
			return True
		elif sight.find_known_items(life, matches=_feed_matches):
			movement.collect_nearby_wanted_items(life, matches=_feed_matches)
			return True
	
	if brain.get_flag(life, 'no_backpack'):
		_nearby_backpacks = sight.find_known_items(life, matches=[{'type': 'backpack'}])
		
		if _nearby_backpacks:
			movement.collect_nearby_wanted_items(life, matches=[{'type': 'backpack'}])
			return True

def manage_hands(life):
	for item in [lfe.get_inventory_item(life, item) for item in lfe.get_held_items(life)]:
		_equip_action = {'action': 'equipitem',
				'item': item['id']}
		
		if len(lfe.find_action(life,matches=[_equip_action])):
			continue
		
		if lfe.can_wear_item(life, item):
			lfe.add_action(life,_equip_action,
				401,
				delay=lfe.get_item_access_time(life,item['id']))
			continue
		
		if not 'CANWEAR' in item['flags'] and lfe.get_all_storage(life):
			_store_action = {'action': 'storeitem',
				'item': item['id'],
				'container': lfe.get_all_storage(life)[0]['id']}
			
			if len(lfe.find_action(life,matches=[_store_action])):
				continue
			
			lfe.add_action(life,_store_action,
				401,
				delay=lfe.get_item_access_time(life,item['id']))

def manage_inventory(life):
	for item in [lfe.get_inventory_item(life, item) for item in lfe.get_all_unequipped_items(life, check_hands=False)]:
		_equip_action = {'action': 'equipitem',
				'item': item['id']}
		
		if len(lfe.find_action(life,matches=[_equip_action])):
			continue
		
		if lfe.can_wear_item(life, item):
			lfe.add_action(life,
				_equip_action,
				401,
				delay=lfe.get_item_access_time(life, item['id']))
			continue

def explore_known_chunks(life):
	#Our first order of business is to figure out exactly what we're looking for.
	#There's a big difference between exploring the map looking for a purpose and
	#exploring the map with a purpose. Both will use similar routines but I wager
	#it'll actually be a lot harder to do it without there being some kind of goal
	#to at least start us in the right direction.
	
	#This function will kick in only if the ALife is idling, so looting is handled
	#automatically.
	
	#Note: Determining whether this fuction should run at all needs to be done inside
	#the module itself.	
	_chunk_key = chunks.find_best_known_chunk(life)	
	_chunk = maps.get_chunk(_chunk_key)
	
	if chunks.is_in_chunk(life, '%s,%s' % (_chunk['pos'][0], _chunk['pos'][1])):
		life['known_chunks'][_chunk_key]['last_visited'] = time.time()
		return False
	
	_pos_in_chunk = random.choice(_chunk['ground'])
	lfe.clear_actions(life)
	lfe.add_action(life,{'action': 'move','to': _pos_in_chunk},200)

def explore_unknown_chunks(life):
	if life['path']:
		return True
	
	_chunk_key = references.path_along_reference(life, 'buildings')
	
	if not _chunk_key:
		_chunk_key = references.path_along_reference(life, 'roads')
	
	if not _chunk_key:
		_best_reference = references._find_best_unknown_reference(life, 'roads')['reference']
		if not _best_reference:
			return False
		
		_chunk_key = references.find_nearest_key_in_reference(life, _best_reference, unknown=True)
	
	_walkable_area = chunks.get_walkable_areas(life, _chunk_key)
	if not _walkable_area:
		return False
	
	_closest_pos = {'pos': None, 'distance': -1}
	for pos in _walkable_area:
		_distance = numbers.distance(life['pos'], pos, old=False)
				
		if _distance <= 1:
			_closest_pos['pos'] = pos
			break
		
		if not _closest_pos['pos'] or _distance<_closest_pos['distance']:
			_closest_pos['pos'] = pos
			_closest_pos['distance'] = _distance
	
	#print _chunk_key, _closest_pos['pos']
	
	lfe.clear_actions(life)
	lfe.add_action(life,{'action': 'move','to': _closest_pos['pos']},200)
