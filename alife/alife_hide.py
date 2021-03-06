#This is intended to be an example of how the new ALife
#system works.
from globals import *

import life as lfe

import judgement
import movement
import sight
import brain

import logging

STATE = 'hiding'
TIER = TIER_COMBAT-.2

def conditions(life, alife_seen, alife_not_seen, targets_seen, targets_not_seen, source_map):
	RETURN_VALUE = STATE_UNCHANGED
	
	if not lfe.execute_raw(life, 'state', 'hide'):
		if life['state'] == STATE:
			lfe.clear_actions(life)
			
		return False
	
	if not life['state'] == STATE:
		RETURN_VALUE = STATE_CHANGE
	
	return RETURN_VALUE

def tick(life):
	_threats = judgement.get_threats(life, recent_only=True, limit_distance=sight.get_vision(life))
	#_knows = brain.knows_alife_by_id(life, _threat)
	movement.escape(life, _threats)
