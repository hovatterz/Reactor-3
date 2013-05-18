from globals import *

import life as lfe

import weapons
import chunks
import combat
import brain

import logging
import numbers
import maps
import time

def judge_item(life, item):
	_score = 0
	
	if brain.get_flag(life, 'no_weapon') and item['type'] == 'gun':
		_score += 30
	elif brain.get_flag(life, 'no_backpack') and item['type'] == 'backpack':
		_score += 30
	
	return _score

def judge_self(life):
	_confidence = 0
	_limb_confidence = 0
	
	for limb in [life['body'][limb] for limb in life['body']]:
		#TODO: Mark as target?
		if not limb['bleeding']:
			_limb_confidence += 1
		
		if not limb['bruised']:
			_limb_confidence += 2
		
		if not limb['broken']:
			_limb_confidence += 3
	
	#TODO: There's a chance to fake confidence here
	#If we're holding a gun, that's all the other ALifes see
	#and they judge based on that (unless they've heard you run
	#out of ammo.)
	#For now we'll consider ammo just because we can...
	_self_armed = lfe.get_held_items(life,matches=[{'type': 'gun'}])
	
	if _self_armed:
		_weapon = lfe.get_inventory_item(life,_self_armed[0])
		_feed = weapons.get_feed(_weapon)
		
		if _feed and _feed['rounds']:
			_confidence += 30
		else:
			_confidence -= 30
	
	return _confidence+_limb_confidence

def get_combat_rating(life):
	_score = 0
	
	#TODO: CLose? Check equipped items only. Far away? Check inventory.
	if lfe.get_held_items(life, matches=[{'type': 'gun'}]) or lfe.get_all_inventory_items(life, matches=[{'type': 'gun'}]):
		_score += 10
	
	return _score

def judge(life, target):
	_like = 0
	_dislike = 0
	_is_hostile = False
	_surrendered = False
	
	if target['life']['asleep']:
		return 0

	if 'greeting' in target['received']:
		_like += 1
	
	_like += target['trust']
	
	#if 'greeting' in target['sent']:
	#	_like += 1
	
	for memory in lfe.get_memory(life, matches={'target': target['life']['id']}):
		if memory['text'] == 'friendly':
			_like += 2
		
		elif memory['text'] == 'hostile':
			_is_hostile = True
			_dislike += 2
		
		elif memory['text'] == 'traitor':
			_dislike += 2
		
		elif memory['text'] == 'shot by':
			_dislike += 2
		
		elif memory['text'] == 'compliant':
			_like += 2
		
		elif memory['text'] == 'surrendered':
			_surrendered = True

	#First impressions go here
	if WORLD_INFO['ticks']-target['met_at_time']<=50 and not brain.get_impression(life, target['life'], 'had_weapon'):
		if lfe.get_held_items(target['life'], matches=[{'type': 'gun'}]):
			brain.add_impression(life, target['life'], 'had_weapon', -3)
	
	if brain.get_impression(life, target['life'], 'had_weapon'):
		if not lfe.get_held_items(target['life'], matches=[{'type': 'gun'}]):
			_like += abs(target['impressions']['had_weapon']['score'])
	
	for impression in target['impressions']:
		_score = target['impressions'][impression]['score']
		
		if _score < 0:
			#print '-',impression
			_dislike += abs(_score)
		else:
			#print '+',impression
			_like += _score
	
	_like *= brain.get_trust(life, target['life']['id'])
	
	if _is_hostile:
		if _surrendered:
			target['flags']['surrendered'] = True
		else:
			_life_combat_score = get_combat_rating(life)
			_target_combat_score = get_combat_rating(target['life'])
			brain.flag_alife(life, target['life'], 'combat_score', value=_life_combat_score-_target_combat_score)
			
			logging.warning('** ALife combat scores for %s vs. %s: %s **' % (' '.join(life['name']), ' '.join(target['life']['name']), _life_combat_score-_target_combat_score))
	
	return _like-_dislike

def judge_chunk(life, chunk_id, long=False, visited=False):
	chunk = CHUNK_MAP[chunk_id]
	
	if long:
		_max_score = SETTINGS['chunk size']*6
		_distance = (numbers.distance(life['pos'], chunk['pos'])/float(SETTINGS['chunk size']))
	else:
		_max_score = SETTINGS['chunk size']*4
		_distance = 0
	
	_initial = False
	if not chunk_id in life['known_chunks']:
		life['known_chunks'][chunk_id] = {'last_visited': 0,
			'digest': chunk['digest']}
		_initial = True
	
	_score = numbers.clip(_max_score-_distance, 0, _max_score)
	for _life in [LIFE[i] for i in LIFE]:
		if _life['id'] == life['id']:
			continue
		
		#if chunks.is_in_chunk(_life, chunk_id):
		#	if _life['id'] in life['know']:
		#		_score += lfe.get_known_life(life, _life['id'])['score']*.5
	
	if visited:
		life['known_chunks'][chunk_id]['last_visited'] = WORLD_INFO['ticks']
	
	if long:
		_score += len(chunk['items'])
	else:
		for item in chunk['items']:
			_item = brain.remember_known_item(life, item)
			if _item:
				_score += _item['score']

	maps.refresh_chunk(chunk_id)
	life['known_chunks'][chunk_id]['score'] = _score
	
	return _score
	#if _initial:
	#	logging.debug('%s judged chunk #%s with score %s' % (' '.join(life['name']), chunk_id, _score))

def judge_all_chunks(life):
	logging.warning('%s is judging all chunks.' % (' '.join(life['name'])))
	_stime = time.time()
	
	for chunk in CHUNK_MAP:
		judge_chunk(life, chunk)
	
	logging.warning('%s completed judging all chunks (took %s.)' % (' '.join(life['name']), time.time()-_stime))

def judge_reference(life, reference, reference_type, known_penalty=False):
	#TODO: Length
	_score = 0
	_count = 0
	_closest_chunk_key = {'key': None, 'distance': -1}
	
	for key in reference:
		if known_penalty and key in life['known_chunks']:
			continue
		
		_count += 1
		_chunk = maps.get_chunk(key)
		_chunk_center = (_chunk['pos'][0]+(SETTINGS['chunk size']/2),
			_chunk['pos'][1]+(SETTINGS['chunk size']/2))
		_distance = numbers.distance(life['pos'], _chunk_center)
		
		if not _closest_chunk_key['key'] or _distance<_closest_chunk_key['distance']:
			_closest_chunk_key['key'] = key
			_closest_chunk_key['distance'] = _distance
		
		#Judge: ALife
		for ai in _chunk['life']:
			if ai == life['id']:
				continue
			
			if not lfe.can_see(life, LIFE[ai]['pos']):
				continue
			
			_knows = brain.knows_alife(life, LIFE[ai])
			if not _knows:
				continue
				
			_score += _knows['score']
		
		#How long since we've been here?
		#if key in life['known_chunks']:
		#	_last_visit = numbers.clip(abs((life['known_chunks'][key]['last_visited']-WORLD_INFO['ticks'])/FPS), 2, 99999)
		#	_score += _last_visit
		#else:
		#	_score += WORLD_INFO['ticks']/FPS
		
	#Take length into account
	_score += _count
	
	#Subtract distance in chunks
	_score -= _closest_chunk_key['distance']/SETTINGS['chunk size']
	
	#TODO: Average time since last visit (check every key in reference)
	#TODO: For tracking last visit use world ticks
	
	return _score

def judge_camp(life, camp):
	#This is kinda complicated so I'll do my best to describe what's happening.
	#The ALife keeps track of chunks it's aware of, which we'll use when
	#calculating how much of a camp we know about (value between 0..1)
	#First we score the camp based on what we DO know, which is pretty cut and dry:
	#
	#We consider:
	#	How big the camp is vs. how many people we think we're going to need to fit in it (not a factor ATM)
	#		A big camp won't be attractive to just one ALife, but a faction will love the idea of having a larger base
	#	Distance from other camps
	#		Certain ALife will prefer isolation
	#
	#After scoring this camp, we simply multiply by the percentage of the camp
	#that is known. This will encourage ALife to discover a camp first before
	#moving in.
	
	_bonus = 0
	_known_chunks_of_camp = []
	for _chunk_key in camp:
		if not _chunk_key in life['known_chunks']:
			continue
		
		_known_chunks_of_camp.append(_chunk_key)
	
	_percent_known = len(_known_chunks_of_camp)/float(len(camp))
	
	_known_camps = [c['reference'] for c in life['known_camps'].values()]
	#print _known_camps
	if camp in _known_camps:
		print 'ssssssssssssssssss'
	#print _known_camps
	#if lfe.get_memory(life, matches={'text': 'heard about camp', 'camp': camp}):
	#	_bonus += 2
	#	print 'bonus!!!!!!!!!'
	
	#TODO: Why does this cause a crash?
	#return int(round(_percent_known*10))
	return (len(camp)*_percent_known)+_bonus

def judge_job(life, job):
	_score = 0
	for factor in job['factors']:
		if factor['type'] == 'alife':
			_alife = brain.knows_alife_by_id(life, factor['value'])
			
			if not _alife:
				continue
			
			_score += judge(life, _alife)

	return _score

def judge_raid(life, raiders, camp):
	# score >= 0: We can handle it
	# 		<  0: We can't handle it 
	_score = 0
	for raider in raiders:
		_knows = brain.knows_alife_by_id(life, raider)
		if not _knows:
			#TODO: Confidence
			_score -= 2
			continue
		
		if not brain.get_alife_flag(life, _knows['life'], 'combat_score'):
			judge(life, _knows)
		
		if brain.get_alife_flag(life, _knows['life'], 'combat_score'):
			_score += _knows['flags']['combat_score']
	
	logging.debug('RAID: %s judged raid with score %s' % (' '.join(life['name']), _score))
	
	return _score

#TODO: Should be in brain.py?
def get_trust(life, target_id):
	_knows = brain.knows_alife_by_id(life, target_id)
	
	return WORLD_INFO['ticks']-_knows['met_at_time']

def believe_which_alife(life, alife):
	_scores = {}
	for ai in alife:
		_score = get_trust(life, ai)
		_scores[_score] = ai
	
	return _scores[max(_scores)]
		
