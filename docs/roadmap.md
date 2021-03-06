Reactor 3 - Roadmap
===================

This is the roadmap for Reactor 3. Rules are as follows:

	* Each milestone must focus on a similar technical aspect (maps, AI, etc)
	* Only features from the current milestone can be completed
	* If a feature has to be bumped up a milestone, it instantly becomes top priority

Milestone 1 - Data
==================

Goal
----
To find a way to properly store and retrieve data without falling back on complicated
solutions most likely using OOP. Data should be easy to manipulate and remove, along
with being easy to store to disk.

Tasks
-----
{x} Structure of Tiles
{x} Structure of Maps

Structure of Tiles
------------------
Items and Tiles will be using dictionaries. To lower data cost, Tiles will specifically
have two parts: static and dynamic. Static parts will be referenced and not stored
locally to that Tile, and will contain things such as movement cost and icon.
The dynamic portion covers changing values, like items contained at that position
or the depth of water.

Structure of Maps
-----------------
Maps will be in the format of {x}{y}{z}, the last of which will hold the array of Tiles
for a position's Z-levels. There is no need to treat this data any differently than
a container for Tiles, so maps can easily be dumped to the disk using `JSON.dumps()`

Milestone 2-1 - Structure and Layout
==================================

Goal
----
To organize the general structure of the engine's core features - meaning that each
piece of the engine has its own file and are all properly named. In addition, basic
functions like libtcod setup and input handling should be created in a general class.

Milestone 2-2 - Core Functions
============================

Goal
----
Create and establish the inner-workings of the engine, like tile drawing and other
helper functions to make development easier. Functions should be readable outside
the context of their respective files if the programmer should choose to use the
functions without the filename prepended.

Get all the complicated systems in place first, like fast drawing and lighting.
These have been an issue in the past, so it's better to get them working optimally
now rather than later.

Milestone 2-3 - Terraform Development - Part 1
==============================================

Goal
----
Establish the basics for the level editor, Terraform. Since mouse input is currently
inoperable just hang on to keyboard input. Tiles should be selectable, placeable, and
removable. Selecting tiles should just be assigned to a set of keys until the mouse
issues are worked out.

Milestone 3-1 - The Beginning of Life - Part 1
==============================================

Goal
----
Life is an extremely complicated mess of variables all interacting at once. Sometimes
creating life is the hardest part, as dictionaries need to be connected to other
dictionaries, all while being somewhat easy to access and modify.

Structure
---------
						   head
						   neck
				lshoulder	 	rshoulder
			upperleftarm	     	upperrightarm
				lelbow	  chest		relbow
			lforearm				  rforearm
			lhand		   hip			 rhand
						  groin
					lthigh		rthigh
					lknee		 rknee
				llowerleg		 rlowerleg
				lfoot				 rfoot

Milestone 3-2 - The Material Things - Part 2
==============================================

Goal
----
Like in any game, items are extremely important and often introduce a lot of new,
interesting features. Regardless of what the item is (be it a weapon, food, or clothing,)
it's important to make them just as easy to modify as any other object in the game.

Right now every character is in the nude! We'll remedy that by creating clothes, which
despite sounding very simple, are actually one of the more complex objects we'll be adding.
This is because clothes aren't just attached to one part of the body, are are technically
attached to the arms, legs, whatever...

Clothes can also hold items themselves, so that also needs to be covered.

Example
-------

    jacket = add_item(player,'jacket')
    equip_item(player,jacket)

    #This function is then called...
    def equip_item(player,item):
        #TODO: Faster way to check this with sets
        for limb in item['attaches_to']:

Post-Mortem
----------
Milestone 3 was completed without much regard to this document. Fortunately, the issue
tracker was cleared without much trouble, although there were definitely a few problems
along the way that pushed back the completion date slightly.

As we move into Milestone 4, it's time to take into hard consideration how the core gameplay
mechanics will be conveyed to the user. This involves building the character's relationship
with items scattered throughout the world.

Milestone 4-1 - Interaction
=========================
Items currently have no individual behaviors, sans sneakers which provide the user with
increased speed. This is a good sign that player <-> item interactions are possible with
the current method of storing item data, and provides a ground for adding in more possibilities.

Stepping back, items need to exist in two contexts: The world and the player. In each, the item
should behave according to its in-game description, which should reflect the various effects it
has stored.

Items should also be able to interact with each other, maybe to combine and eventually form
a different item. The reverse should also be possible in some cases (tearing apart a shirt to
make bandages.)

A good example of this kind of interaction is between bullets and guns. Loading a gun is a 3-step
process that involves getting ammo, loading the bullets into the magazine, then inserting the
magazine into the gun. While some may argue that this is complexity for the sake of complexity,
I will point out that this type of process (loading your own gun) adds to the survival aspect
of the game, and also builds a deeper relationship with the player and the weapons he or she
chooses. It also encourages strict inventory management as a sort of metagame where the most
organized person succeeds, while the messy search through backpacks for the appropriate item.

This leads to inventory management: Items can be stored in several areas on the body. At first,
the player has a small backpack able to hold a handful of items, but can also store smaller items
in their pockets. In the above case, it would make more sense to stick a magazine in your pocket
rather than a backpack, which would require taking off in order to remove the item. Once again,
this adds to the inventory metagame discussed previously and puts the player in a position
to set themselves up for success or failure, depending on how accessible the item they require
is.

Example
------
A pistol may be holstered to someone's hip, allowing them easy access to it in dangerous
situations. Should the player predict a potentially deadly encounter from a distance, they have
the opportunity to shuffle their items as needed; holster the pistol, remove an SMG from their
backpack, and engage. Some weapons could also be outfitted with a strap, allowing them to simply
be swung around once the pistol is holstered.

Milestone 5-2 - ALife Revision 2
================================
The previous system for handling ALife functionalities like understanding and performing actions as a result will be replaced with the second iteration of ALife.
These changes will enforce a standard for all possible decisions, encouraging a common structure for current and future additions:

	brain-escape.py
		input:
			alife_seen
			alife_notseen
			targets

		qualifications (conditions):
			initial_state = 'vulnerable' #Previous needed ALife state
			attack <= 30%
			defense <= 30%

		actions:
			escape for targets
			state = 'panic' #State the ALife is now given

*Note*: These don't have to be required (like initial-state)

*Note*: Attack and defense are misleading (safety as just one variable)

Notice how this format puts a strict guideline on what variables are used and defined.
Previous implementations avoided this and as a result ended up with a variety of one-off terms and garbage variables.
This new structure defines when an action goes into effect and what conditions keep it active.
They are intended to work in certain cases and only be triggered when all conditions are met (in a descending order.)
Simply put, each condition is checked starting from the top, and if the ALife meets this then the function crawls down the list. If everything checks out OK then the function is run.

Milestone 5-3 - Traversing the Map
==================================
This sub-goal establishes the methods used by ALife to traverse the map in the most efficient way possible. Since pathfinding is a relatively intense operation, abstracted map data (chunks and reference maps) will be used instead of interpreting raw data.

Discovering the Map
-------------------
Currently, the biggest flaw in the ALife is its inability to discover the map by itself. As a general test, I've instructed the ALife to automatically go to and (roughly) path along the nearest road, but this isn't intended to be final in any sense.
For the sake of documentation, the offending fuction is `alife.survival.explore_unknown_chunks()`. The majority of the changes needed will be done in this file along with any files containing chunk functions.
We must also consider how often the ALife will be performing these tasks. With any luck, we should be able to have the ALife run any of these pathfinding operations once every 30 seconds or so, as the other ALife module for exploring interesting chunks will run automatically if needed then resume the discovery process when finished.

Since we are dealing with abstracted data, the amount of information to parse is much smaller than normal:

    Amount of tiles to parse in raw form: 22500
    Amount of tiles to parse in abstracted form: 900

This should give us access to just about every form of pathfinding that previous had to be avoided due to the sheer size of the current map. Granted, we'll still be using A* to find the actual paths, but these new functions will give us a vague idea of where the A* needs to be pointed at.

Finding a Place to Be Safe
------------------------
Next comes the issue of finding a proper place for the ALife to camp. This subgoal involves finding an appropriate way to score chunks with an appropriate safety score. Calculating this score should factor in the any friendly ALife occupying that area in addition to any other factors that ensure the chunk(s) provide adequate protection.

Requirements:
	* Easily fortified
	* Either remote or in a central location
		* When scoring for remote chunks we can check the distance to the nearest buidling

New Conversations
----------------
We need to track the following for all ALife:

	* Their thoughts on other ALife
	* Any current or previous conversations
		* The state of any current conversations
	* Any interrupts that should occur and how to judge what conversations are more important
	* Overhearing conversations and how to handle second-hand information.

Also implement a proper matching system so a message can be broadcasted to more than one ALife based on certain criteria (faction, location, etc.)
This system will be used for all conversations.

The structure for messages will be as follows:

	Match: Series of requirements an ALife must have to be considered the target of a conversation.
	Gist: Same as in the first revision: A summary of the message.

ALife will maintain the following arrays in their `know` dictionary:

	* Asked: Things we asked the ALife
	* Answered: Responses given to the ALife

ALife will store the following in their memory:

	* The end result of any notable conversation event:
		* First met
		* Initial impression
		* Who told them certain information

In addition, we can pass along memories directly through conversation.

Thoughts:
So we can create one entity (result  of `create_conversation`) and  pass it around to all ALife involved or go about it the old way, where each ALife has a view of the converation and that's it. Obviously there are several advantages to each one, with passing around the same entity getting into some messy memory access stuff possibly ending in a fractured packet of info being sent around... the best method after thinking about that would be having a unique view for each person and hoping that the ALife can ensure everyone involved in the conversation is on the same page.

We must also consider that if someone says "Hello!" to a group of people not everyone responds. Usually if one person responds the rest of the group is considered to have had that same response also.

Timing: Some questions need to be asked more than once, like requesting chunk info. There should be a delay or a way for topics to decay and leave the list eventually. This can *probably* be done in `alife.talk`, but there will need to be definite changes in `sound.listen()` for handling this behavior.

Milestone 6 - Growing Content
=============================

Goal
----
With all the systems in place, we must now generate content to build up the game's depth. The UI will also be reworked and extended to give the player a better understanding of the world. We'll also start creating personalities for ALife and extending their logic.

Roadmap
-------
When the player enters the world there should be some kind of conflict between the starter camp and the bandits. We want there to be some kind of established "safe zone" so the player feels like they have to be somewhat careful about where they are going.

Take note that the player won't be aligned to a faction unless:

1) They are wearing a faction-specific item
2) There are known to be in that faction

Both things will be false for new players regardless of how the first job goes. However, it should be noted that Bandits are automatically aligned against non-bandits, so you will encounter combat if you run into them anyway.

The following should be playable:

	The player spawns in the northwest and is instructed to follow the road until they see the nearest camp. The player should then be able to enter the camp, find out who the operator is, and get assigned their first job: Get the documents off the body of a deceased soldier.
	
	Upon arrival it is apparent that the target is not dead, but just has a bad leg injury preventing them from running. You will encounter this person and go through a dialog determining whether you are on good terms or not. If not, you will enter combat.
	
	After resolving the conflict you will take the documents back to camp. You will then be told to talk to those hanging around the camp to find what to do next, but the decision is ultimately up to you whether or not you actually do that.

Problem 1: The UI
----------------
We'll attempt to give the player a better understanding of the world and the people inhabiting it with these changes.

Acknowledging the following issues:
	* The player's lack of situational awareness
		* Information not CLEARLY displayed on the map needs to be re-represented on the right
			* EX: Target name - (Status)

Problem 2: The Combat
---------------------
The damage model makes no sense in a lot of applications. While damage is handled, the appropriate reaction is not, so the ALife is only affected in the long-lasting negative effects and not the reaction (stumbling, twirling, etc)

Problem 3: Group Tasks
----------------------
Like deciding how to flank a target, etc. Engage them.

Problem 4: Misc Stuff
---------------------
Message boxes on map screen for conversations.

New(er) Conversations
-------------------
Conversations have been revamped and the old system has been axed (for the most part.) While there are still bits and pieces of it scattered about, I don't think there is a use for it anymore. As a result, all the features of the old system need to be ported to the new one.

However, I am still unsure if these features can be recreated properly in the new code. The only real advantage of the old structure was that there wasn't any real structure at all- just a way for ALife to "hear" things and react accordingly. I'm hoping that what I have now can emulate that, because otherwise a lot of code is now obsolete (for the greater good.) To test, I've written the proper dialog for learning about camps and asking camp-related questions. This is still in its infancy, but it's interesting to see that it works rather well, so I'm inclined to believe that the old code should work too.

To explain, this new system is very centralized, so about 90% of all dialog-related code is contained in a single file. I guess that isn't much different than the previous code, but I think the big difference here is that the back-and-forth nature of certain conversations is a lot more organized and open to expansion than before. I really did feel like getting ALife to talk before was probably my least favorite thing to do, but if I am able to apply this to ALife vs. ALife situations instead of just Player vs. ALife, I think I might be on to something.

Another advantage is that I'll no longer need to write separate dialog menus for the player since this code generates these for us. I made a somewhat risky decision and wrote a new, less-complicated menu structure to use instead. There isn't anything wrong with the menus I use across the rest of the game, but I wanted to do some very specific things and knew I would just be bloating up a working system if decided to extend existing code to satisfy one case.

Questions
---------
Now there is a need for ALife to ask about certain topics. This could be done in one fell swoop when beginning dialog, but we specifically want the ALife to know they have questions to ask beforehand so they can pursue dialogs by themselves.

Example case: An ALife joins a camp but is unaware of who the founder is. After running out of people to ask, the ALife simply idles in the camp until someone can help them (during this time they are always broadcasting the request for founder info.) I won't say it's easier, but I'd like to get this behavior into the dialog tree instead, giving me an opportunity to implement dialogs started with the player by the ALife.

I think the main idea here is just attaching the ALife to the dialog tree and hoping they are able to figure it out. After all, it should solve the issue of having multiple conversations active (but not running) at once, in addition to giving me some amount of context to deal with instead of just having a random phrase in an array I have to parse to find its origin (and even then I can't be sure what the context is.)

Lies
----
In an effort to move the ALife's intelligence into the next level of complexity, it's time to start processing memories to find out what makes sense and what doesn't.

The obvious first thing to check will be looking at camp founders. The immediate issue is the fact that the ALife does nothing but reference the camp founder when doing some tasks; how could we possible interject this information into a phrase to get a response out of someone? In the case of the camp founder, should we just out-right ask everyone who the founder is?

I guess the real question is how to make the ALife discover lies without forcing it on them during dialog; i.e., it should occur naturally and through the `memory.detect_lies()` routine.

First order of business will be having the ALife walk around and get to know everyone.

Routines
---------
Each ALife has a selection of wants and needs. Needs include eating, sleeping, and general survival gear. Wants include non-essential items like radios (almost a need, but not quite) and high-end weapon attachments that aren't otherwise crucial.

Needs establish the base behavior for all ALife, while wants define their unique logic.

[x] Hunger
------
Operates on a simple timer that decreases each tick. Eating adds a variable amount to this timer. When this timer is half of its maximum a person is considered hungry. At a fourth they are starving.

Food can be found scattered about the Zone, usually in cans.

Thirst works on a similar timer but is a lot shorter, so you'll need to drink more frequently.

Squads Before Camps
------------------
Squads form when it is more convenient to fulfill these kinds of needs together, so ALife that need food might find themselves scavenging the same area, resulting in a confrontation that leads to a working relationship.

These groups will grow larger and larger as similar people are encountered while out adventuring.

Conflicts
----------
A difficult part of this is getting the ALife to disagree and begin conflicts. While it is easy to simulate what happens after a conflict starts, developing one that feels natural is many times harder. We simply cannot have "they're from a different squad" as a valid reason for starting fights. Whatever it is, it must be natural and make some amount of sense.

	* I would like to avoid "they're armed, so they must be dangerous."
		This isn't always true. After all, we'd have to ask them what their stance is, which involves coming up with a reason for being friendly or hostile.
			This is easy for the player to do because their reasoning is up to them.

Developing Friction
------------------
I want to avoid "good" and "bad" factions. I'll focus on camps right now since they will eventually develop into factions as relationships grow:

	Camps are most concerned with land ownership, i.e, they want to be in control of certain spots on the map.
		We will call these areas landmarks and they will have some kind of strategic importance or resource.
	
		Camps have certain needs. A need for weapons will result in a raid of an ammo depo.
	
[x] Advanced Life Flags
------------------
I'll start using flags in the race .XML to help better tweak how ALife behave. Examples include:
	
	CAN_TALK: ALife can speak and understand what is trying to be conveyed
	HUNGER/THIRSTY: Has requirement for food/water
	CAN_GROUP: Ability to develop squads/work in groups
	
New Judgement and Combat Scoring
------------------------------
One of the oldest parts of the codebase is `judgement.py`. It is a relic from a previous time in development where scoring was looked at from a very different point of view. It was intended to be all-encompassing, but as the game grew it remained the same.

Currently, the actual `judge` function returns a numerical value that indicates how much an ALife likes a target. Any value at or above zero indicates that the target is neutral. Anything less than that is considered hostile.

New system ideas:

	1) Like/dislike scoring can stay since it appears to be working so far.
		However, it should *not* be the deciding factor in whether combat is started
	2) Trust needs to play a clearer role in judgement (it also needs to be defined)
		Adding it on to `like` is incorrect since trust does not represent how much someone likes another
	3) Scoring must change once a target is identified as hostile
		Furthermore, this must be mutual if either ALife has made its hostile intentions clear

Variables:
	Fondness (-inf, +inf)
		Definition: Decides how well someone is liked based on neutral actions.
		Based on: friendly/unfriendly memories (first and second-hand)
	
	Danger (0, +inf):
		Definition: Represents how much of a threat someone poses.
		Based on: visible weapons WITH hostile memories (first and second-hand) to prove it.
			(invalid otherwise)
	
	Trust (-inf, +inf):
		Definition: Value used to define how believable someone's word is
		Based on: Dialog.
		Affects:
			This value comes into play during `determine_truth`, a memory seach function that simply picks the most "trusted" memory from the list.

New Pathing
------------
Structure: dict
Keys:
	Start		...
	End			...
	path_type	['']

Operation:
	First a "chunk path" is generated. The chunk map sees if it can path to the destination chunk.
		If it cannot, it gets as close as it can
	The ALife then follows that path chunk to chunk
	If we arrive at the end of the chunk path and can see the target, then stop.
	Otherwise use A* to find the destination.

Tech:
	The map is scanned and the following taken into account:
		1) Areas we can walk (can be unconnected.)
		2) Z-levels we can travel to

Other Concepts:
	Buildings, and other difficult terrain
	Zones
		Can references be Zones?
	Dead Zones
		Zones of the map not accessible from the current Zone

New Pathing v2
--------------
I'm going to call this method "zone pathing." This is a much more comprehensive way to ensure that paths are
correct the first time. We'll be slicing the map into vertical sections while keeping the same chunk size.

For each slice:
	
	* Set the zone and ramp maps to 0.
	* Increment the global zone counter.
	* Start flooding the zone map beginning in the top left of the slice (if the position is walkable) with the number held in the zone counter
	* If the position is walkable and is near to another z level, set the current position to RAMP on the neighboring ramp map and set RAMP on the position where this z-level decreases
	* After we are done flooding, save all of these positions to a dictionary so we can search for zones easily
	* Repeat for each zone level
	
Combat Fix #1 (Complete)
--------------
First in a series of fixes.
All of the logic that decides when combat is entered needs to be scrapped.

Proposing: `is_safe()`
	This function checks a variety of ALife memories and values to determine if they are safe.
	It would replace the majority (all?) of the calls to individual calculate_safety() functions.
	In addition, we can have this run once at the start of the tick.

Proposing: `calculate_safety()`
	Runs before ALife modules.
	Inspects all variables checked by `is_safe()` for changes.
		For example, when `combat_targets` become invalid.

Combat Fix #2 (Complete)
--------------
We need a way to determine who our targets are. Proposing the following categories:

Visible: In the ALife's LOS.
Non-visible: Inverse of previous.
Visible threats: In the ALife's LOS. Possibly dangerous.
Non-visible threats: Not in the ALife's LOS. Possibly Dangerous.

Combat Fix #3
--------------
Escaping is a huge issue. We are just instructing the ALife to run away, which is fine, but what about after that?

Proposing: Intelligent Hide. The ALife, once in the `hidden` state, generates a LOS from the last known position
of the target(s). The ALife then passes this to the pathing algor. as dangerous territory. We then choose a
destination, which can be a nearby camp or hiding spot (The ALife should also call for backup at this time to see
who is nearby.)

We only need to generate this once unless the target changes position

Combat Fix #4
--------------
When ALife are in trouble, they call for backup. If enough arrive and the situation is not dire (person who called
for help is in ok condition,) a surrender may be proposed.

Dialog Functions
------------------
The problem is that the dialog system is a little too good at working entirely by itself, leaving us with no idea of what the outcome was or even being able to extract basic data like what dialog is even running.

What is being proposed is a series of changes that expose the inner-workings of the dialog system.

Crafting
---------
Used for dismantling in this milestone.

The Big Fix
============
This is by no means the last major change to Reactor 3, but instead the first step in a series of moves towards fully-capable ALife. These ares the issues I am aiming to address:

Issue #1: State Overrides
------------------------
Each ALife module has rules for modules it will not take over for (i.g., 'camping' will not take over for 'combat' if it is in effect.) While this works, each module has to explictly list what modules it will ignore. This provides the following disadvantages:

	1) Adding new modules involves finding what modules will not be overridden and listing them.
		In addition, we must also modify modules if the new module needs to be ignored by any of them
	2) Won't work from a modders point of view since it involves modifying code outside of the modders' scope
		(Mods are designed to work alongside the codebase- not over it.)

We now need a general structure to handle this.

Issue #2: Jobs and Doing Stuff
-----------------------------
While the jobs system works, it is very unflexible and relies on functions for operation. In addition, it's hard to get the ALife to do anything without explictly writing a module. This is, of course, an issue when it comes down to actions like finding a camp leader.

How I would like it to work (finding a camp leader.):

	[ALife is aware of a camp and does not know the founder.]
	add_goal(life, 'learn about camp', camp=camp_id)
	add_criteria_memory(camp=camp_id, founder='*')
		with_criteria(can_trust, founder, required=True)
	add_criteria_memory(camp=camp_id, group='*')
		with_criteria(likes_group, group_id, required=True)
	
Group Battles
------------
The last big issue we have to approach is the lack of any conflict in the Zone between groups. The reason for the current lack of conflict has to do with there being nothing to fight over.
Proposing: Artifact fields. Areas of the map that generate a specifc kind of artifact, which change position after an established amount of time. Groups will be fighting for control of these areas.

Camps v2
--------
While the old camp structure is no longer valid in the wake of "shelters", there is now a need to manage larger sections of land. The proposed solution is a concept similar to the "control point" mode of Team Fortress 2, where pre-determined parts of the map can be owned by one team (in this case a group) at a time.

Needs v2 (v3?)
--------------
Lost track of how many times I've looked into the needs logic for ALife, but everything *should* be in working condition from the way I left it last time. iirc I was looking for a way to work needs into the external life structure, which was impossible at the time, but we have rawscript now to cover that. If anything, we should just give the ALife some vague info on when certain items are needed, and the `alife_needs` module should take over and satisfy it. The ALife can't really do all that much with items at the moment, so that should also be put on the list somewhere so it gets addressed in 0.6.

There's a potential issue with getting NPCs to manage inventory space correctly. This time around I'm probably just going to do a bare-bones version of what I want things to eventually look like so I don't end up spending more than a few days on this, so I'll just have them check storage capacity and work from there (at some point they need to consider access times and score storage options.)

The biggest problem is making groups aware of specific item needs - as a proof of concept we should being working towards moving groups around the map to loot things, which introduces a bunch of new code so we can bridge jobs with needs. At this stage we could just mask group item needs under the guise of jobs - I don't think it matters that each ALife maintain an understanding of what items the group needs as long as the leader is parsing that info and sending it out to everyone (as jobs.)

Version 0.6.5
=============
With 0.6 in the wild, it's time to take all existing frameworks/systems and begin using them to create content. We'll also be extending the ALife as much as possible, and implementing the last (?) round of behavioral changes.

What needs to be done
------------------
The laundry list of issues currently logged should be checked over for errors or missed fixes along the way that weren't marked as fixed. Most of these should be avoided and put off for bugfix days.

We will focus now on getting content working in a reasonable manner, and make any changes needed to support more early-game tasks (group formation, etc.) Before we do any of this, the content that exists currently should be examined and reconsidered.

Issue #1: It's Boring
------------------
First: Currently people enter the Zone one by one. Whle this is an accurate way to simulate a Zone where all ALife are interacting naturally, for the interest of time it is slow and boring for the player to watch and participate in. A better way to go about this is currently displayed by Wildlife, who sometimes enter the Zone with one or two additional "pack members" who have a natural bond. This bond is justified by the idea of Mother<->Father<->Child relationships. For the sake of time, we should implement this for people also.

Issue #1.1: Are we abandoning the "true" Zone?
----------------------------------------
By introducing pre-exisiting groups, there could potentially be issues with meshing "natural" ALife (i.e., those entering the Zone by themselves) with ALife who enter the Zone with a pre-existing bond.

Issue #2: The Trust Problem
------------------------
Trust is currently implemented in the worst way possible. The values that modify trust are random and unjustified, and are usually marked with "#TODO: Hardcoded". It would be in our best interest to cover this first, before we get into pre-existing bonds.

What is trust?

The criteria:
* We must be able to measure the ALife's exact trust in another ALife quickly
* Trust should not just consist of random values. There should be a certain amount of "obvious trust" and "earned trust", combined to calculate the total trust.
* A violation of a certain trust should not just be a negative value against the total, but instead something that can potentially swing the entirety of the trust variable into the negatives.

In addition, when do we "trust" someone? How can we measure how much trust is needed for a bond to form?

* Solution 1: Trust "tiers". Each ALife could maintain its own idea of who is a true friend vs. someone they know/work with.

Are there any issues with this solution? I can foresee a problem with the differing ideas of who is a friend/not friend introducing some behaviors where one person treats the other as a friend, while the "friend" sees the person differently. While this is the way it works in the world, it does not translate well to this format.

Solution for Solution 1: Issue 1: Rejections
--------------------------------------
If the above situation occurs, we can implement some form of "awareness", i.e., exposing the ALife to the idea that their level of trust is not mutual, limiting it as a result. There is also the possiblity for reactions to this - is the ALife opposed to the idea of not having mutual trust?

Where do we need to make changes in trust logic?
------------------------------------------
A heavy amount (all?) of the trust modifiers should be in `dialog.py`. We can begin by either disabling  the `modify_trust` function so we don't have to sort through each reference to `like` and `dislike` (misnomer for trust and distrust.)

What determines trust?
-------------------
Hard trust: Trust that is implied. Present in Parent<->child relationships and groups
Dynamic trust: Combination of dialog choices and other interactions

Using these two types of trust
--------------------------
Hard trust is all that should be needed for people to "get along," like in groups. Dynamic trust is used everywhere else.

Issue #2: Job Issue
-----------------
Starting on group jobs has made me realize just how much work is involved with getting the ALife to perform cycles. For example, I can give them the need to collect items for their group, but when it comes down to returning to the camp and storing the items it completely fails. It's the weird mix of needs and jobs that cause the issue, because iirc jobs have a higher priority than needs, so the ALife in question will become aware of the job to return the items regardless of whether they have them or not.

MapGen: Version 2
=================
Now that the current map generator is stable, it's time to write the second iteration of it. We'll work on it in 3 stages, but first, a few notes:

* We need larger maps - at least 2x/3x larger than the current ones
* Each map should have a number of unique landmarks in addition to areas that need to be on every map
* Generated maps should have a clear progression, i.e., going from peaceful to hostile

The following should be on every map, in order:

* Town(s)
* Factories
* Army Warehouses
* Labs
* Reactor

Cycle 1: Towns
------------
The current town size is fine, but the actual layout needs to be much more detailed. Buildings should not be constricted to tetris blocks and need to span multiple z-levels.

First, we need to generate a road leading into the Zone. It should NOT go deeper than factories and must cross through the main town.

Judgement 2.0
------------
Up until recently we've been tracking ALife world-views in a partially "all knowing" sense, i.e., everyone maintained their own views but often borrowed information from the world's memory rather than their own. There's a few reasons why this was done:

	* If a group is disbanded, ALife who are unaware of its removal will still think it exists, and thus pass (now invalid) group IDs to functions that throw Exceptions for doing so.
	* I stubbornly stood behind "memories" as being the go-to way to interpret the world, which involves iterating over a potentially massive dataset.
	
Our previous approach was slow and somewhat clunky - there was no real distinction between Memories and flags in `know_life` and why you would use the former at all. This is still unaddressed - I think the idea before was that memories provided enough context to go back and "rejudge" a situation, but this was never expanded upon outside of one case.

Now we're dealing with the aftermath of the old judgement logic being removed and a new ruleset implemented. It's working fine so far since it was just a modification of how Trust was calculated along with Danger. I don't see that area of the game changing unless these new developments end up uncovering a better way to do it.

THe following things bother me about judgement in its current form:

	* 1) Justification for certain actions are largely unexplained.
	* 2) Transitions between opposite states (discovering -> combat) are jarring. Besides occasional dialog after the fact, nothing but bullets are exchanged.
	* 3) Potential combat targets mix much too frequently.
	* 4) Groups are underdeveloped and play only a very small role in judgement - what about territory?
	* 5) Danger and Trust scores are idiotic and impossible to maintain - the numbers aren't based on anything and result in superficially high trust or distrust.

Issues #1 and #5: Justifying Actions
------------------------
Justification for an action shouldn't consist of just polar opposites ("They are an enemy" and "They are not an enemy"), but instead a wide range of interpretations, some of which is already modeled, just not utilized effectively (See: Dangerous but trusted targets.) ALife should be able to understand the weight of their actions and determined whether or not an action is worth going through with. It is also extremely important that this is not a hidden process - the player and other ALife should know about this in most cases and be able to react accordingly.

The current reaction to seeing members of an opposing faction is a simple fight or flight reponse- we tried to create "Okay, I'll just leave, then" responses, but due to issues in judgement scoring we can't exactly get that range- a target sees a hostile target and reacts immediately, regardless of recent changes in Trust or Danger that may reflect positive advancements in relationships.

Any replacement to this system needs to have hard math backing it and should tell us what type of relationship there is between two ALife.

Relationship types:
	Established hostile (high Danger, high Hostility): Target has either directly attacked you or someone else you trust.
		Reactions:
			Event causing this state happened recently:
				Event was witnessed: Combat
				Happened recently: Investigate
			
			else:
				Event was witnessed: Investigate
				Event was not witnessed (gained knowledge via conversation): Investigate and Interrogate

	Ordered hostile (mixed attributes): ALife made target by group order.
		Reactions:
			Target is marked as friendly: Refuse/Morality break
	
	Respected (high Respect): Authority figure, not always well-liked on a personal level
		Reactions: Mixed
	
	Friend (mixed Respect, high Trust):
		Reactions: Mixed
	
	Neutral (low attributes):
		Reactions: Mixed
	
	Potential threat (low Respect, >low Danger):
		Reactions:
			Target visible: Interrogate

Reactions:
	Interrogate:
		Begin dialog.
		Establish alignments.
			Hostile:
				Begin intimidation tactics.
				Surrender/attack
	Combat:
		If in group: Report attack.
		Begin combat
	
	Investigate:
		In group:
			Report start of investigation: Alert sent out to members of group.
				Offer chance to respond with pertinent information
			Begin search.
			On search complete:
				Target found:
					Interrogate
				Else:
					Create mystery

Respect:
	Factors:
		* Group leader
		* Positive combat actions
		* Superiority
			* Higher-end weapons

Hostility:
	Factors:
		* Unjustified violence
		* Standing ground


Situations (aka Events or Shared Memories)
--------------------
Events are shared memories.

Traits
-----
These define specific rules that affect the decision-making process.

	Aggressive: Prefers violence.
	Naive: Lower threshold for required trust when parsing events.
	Judgemental: First impressions define relationship alignment, harder to switch later on.
	Kleptomaniac: Doesn't care about claimed items.

Fixing
-----
[x] is_compatible_with

Combat flow
===========

'  ______          ,
' |Ranged| - - - |
'  ______


Phase 2
=======
We are at a point where the game works well enough to put down the hammer and nails and pick up a
writing utensil instead. That's a fancy way of saying, "Let's make this into a game."

First and foremost, we will focus on effective world generation. Our goal for this round of changes:

* Design and implement the first two areas of the game: The starting village and military outpost
* Begin implementing enemy types that aren't dynamic ALife: Soldiers and Mutants (maybe later?)

Our first real step is to create the tools we'll need to make this process easier.

Intelligent House Gen
-------------------
We start with a list of chunks (map positions) and a set of rules:

	* We must be able to travel to a room from any given room (all rooms must be connected.)
	* Allow doors connecting interior chunks.

This is only for house interiors. Exteriors are done on a slightly smaller scale later in mapgen.

.goap format
-----------

	[GOAL_DISCOVER]
	DESIRE: HAS_NON_RELAXED_GOAL
	TIER: TIER_RELAXED
	
	[GOAL_LOOT]
	DESIRE: !HAS_NEEDS
	TIER: TIER_SURVIVAL
	SET_FLAGS: {"wanted_items": GET_NEEDED_ITEMS}
	
	[ACTION_WANDER]
	SATISFIES: HAS_NON_RELAXED_GOAL
	LOOP: True
	EXECUTE: WANDER
	
	[ACTION_PICK_UP_ITEM]
	SATISFIES: HAS_NEEDS
	DESIRES: KNOWS_ABOUT_ITEM
	LOOP: False
	EXECUTE: PICK_UP_ITEM
	
	[ACTION_FIND_ITEM]
	SATISFIES: KNOWS_ABOUT_ITEM
	DESIRES: HAS_NON_RELAXED_GOAL
	LOOP_UNTIL: HAS_WANTED_ITEMS
