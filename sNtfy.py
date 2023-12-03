from phBot import *
import QtBind
from threading import Timer
import urllib.request
import urllib.parse
import struct
import json
import os
import re

pName = 'sNtfy'
pVersion = '0.0.3'
pUrl = 'https://raw.githubusercontent.com/sn4dy/phbot-plugins/master/sNtfy.py'

NTFY_DEFAULT_SERVER = 'https://ntfy.sh/'

character_data = None
party_data = None
chat_data = {}
isConnected = False
hasStall = False

ntfyServer = ""
ntfyTopic = ""

gui = QtBind.init(__name__, pName + " Page 1")

QtBind.createLabel(gui, "ntfy Server Address:", 6, 10)
leNtfyServer = QtBind.createLineEdit(gui, "", 6, 30, 145, 19)
QtBind.createLabel(gui, "ntfy Topic Name:", 6, 50)
leNtfyTopic = QtBind.createLineEdit(gui, "", 6, 70, 145, 19)
btnSaveConfig = QtBind.createButton(gui, "saveConfigs", "Save Changes", 6, 90)

QtBind.createLineEdit(gui, "", 169, 10, 1, 262) # Separator

_x = 180
_y = 10

eventCharacterConnected = QtBind.createCheckBox(gui, "doNothing", "Connected to the game", _x, _y)
_y += 20
eventCharacterDisconnected = QtBind.createCheckBox(gui, "doNothing", "Disconnected from game", _x, _y)
_y += 20

eventMessageUniqueSpawned = QtBind.createCheckBox(gui, "doNothing", "Unique spawned", _x, _y)
_y += 20
eventMessageUniqueKilled = QtBind.createCheckBox(gui, "doNothing", "Unique killed", _x, _y)
_y += 20

eventMessageCTF = QtBind.createCheckBox(gui, "doNothing", "Capture the Flag", _x, _y)
_y += 20
eventMessageBA = QtBind.createCheckBox(gui, "doNothing", "Battle Arena", _x, _y)
_y += 20
eventMessageFortress = QtBind.createCheckBox(gui, "doNothing", "Fortress War", _x, _y)
_y += 20
eventMessageCHunter = QtBind.createCheckBox(gui, "doNothing", "Consignment Hunter", _x, _y)
_y += 20
eventMessageCThief = QtBind.createCheckBox(gui, "doNothing", "Consignment Thief", _x, _y)
_y += 20

_x += 275

eventNearGM = QtBind.createCheckBox(gui, "doNothing", "GM near to you", _x, _y)
_y += 20
eventNearUnique = QtBind.createCheckBox(gui, "doNothing", "Unique near to you", _x, _y)
_y += 20
eventNearHunter = QtBind.createCheckBox(gui, "doNothing", "Hunter/Trader near to you", _x, _y)
_y += 20
eventNearThief = QtBind.createCheckBox(gui, "doNothing", "Thief near to you", _x, _y)
_y += 20
eventCharacterAttacked = QtBind.createCheckBox(gui, "doNothing", "Character attacked", _x, _y)
_y += 20
eventCharacterDied = QtBind.createCheckBox(gui, "doNothing", "Character died", _x, _y)
_y += 20
eventMountDied = QtBind.createCheckBox(gui, "doNothing", "Transport/Horse died", _x, _y)
_y += 20

eventMessageQuest = QtBind.createCheckBox(gui, "doNothing", "Quest Completed", _x, _y)
_y += 20
eventBotAlchemy = QtBind.createCheckBox(gui, "doNothing", "Alchemy Completed", _x, _y)
_y += 20
eventMessageItemSold = QtBind.createCheckBox(gui, "doNothing", "Alchemy Completed", _x, _y)
_y += 20

configPage1={'eventCharacterConnected':eventCharacterConnected,'eventCharacterDisconnected':eventCharacterDisconnected,'eventMessageUniqueSpawned':eventMessageUniqueSpawned,'eventMessageUniqueKilled':eventMessageUniqueKilled,'eventMessageCTF':eventMessageCTF,'eventMessageBA':eventMessageBA,'eventMessageFortress':eventMessageFortress,'eventMessageCHunter':eventMessageCHunter,'eventMessageCThief':eventMessageCThief,'eventNearGM':eventNearGM,'eventNearUnique':eventNearUnique,'eventNearHunter':eventNearHunter,'eventNearThief':eventNearThief,'eventCharacterAttacked':eventCharacterAttacked,'eventCharacterDied':eventCharacterDied,'eventMountDied':eventMountDied,'eventMessageQuest':eventMessageQuest,'eventBotAlchemy':eventBotAlchemy,'eventMessageItemSold':eventMessageItemSold}

gui_ = QtBind.init(__name__, pName + " Page 2")

_x = 6
_y = 10

eventMessageAll = QtBind.createCheckBox(gui_, "doNothing", "General", _x, _y)
_y += 20
eventMessagePrivate = QtBind.createCheckBox(gui_, "doNothing", "Private", _x, _y)
_y += 20
eventMessageStall = QtBind.createCheckBox(gui_, "doNothing", "Stall", _x, _y)
_y += 20
eventMessageParty = QtBind.createCheckBox(gui_, "doNothing", "Party", _x, _y)
_y += 20
eventMessageAcademy = QtBind.createCheckBox(gui_, "doNothing", "Academy", _x, _y)
_y += 20
eventMessageGuild = QtBind.createCheckBox(gui_, "doNothing", "Guild", _x, _y)
_y += 20
eventMessageUnion = QtBind.createCheckBox(gui_, "doNothing", "Union", _x, _y)
_y += 20
eventMessageGlobal = QtBind.createCheckBox(gui_, "doNothing", "Global", _x, _y)
_y += 20
eventMessageNotice = QtBind.createCheckBox(gui_, "doNothing", "Notice", _x, _y)
_y += 20
eventMessageGM = QtBind.createCheckBox(gui_, "doNothing", "GM Talk", _x, _y)
_y += 20

_x += 195

eventPartyJoined = QtBind.createCheckBox(gui_, "doNothing", "Party joined", _x, _y)
_y += 20
eventPartyLeft = QtBind.createCheckBox(gui_, "doNothing", "Party left", _x, _y)
_y += 20
eventPartyMemberJoin = QtBind.createCheckBox(gui_, "doNothing", "Party member joined", _x, _y)
_y += 20
eventPartyMemberLeft = QtBind.createCheckBox(gui_, "doNothing", "Party member left", _x, _y)
_y += 20
eventPartyMemberLevelUp = QtBind.createCheckBox(gui_, "doNothing", "Party member level up", _x, _y)
_y += 20

eventGuildNoticeChanged = QtBind.createCheckBox(gui_, "doNothing", "Guild notice changed", _x, _y)
_y += 20
eventGuildMemberLogin = QtBind.createCheckBox(gui_, "doNothing", "Guild member login", _x, _y)
_y += 20
eventGuildMemberLogout = QtBind.createCheckBox(gui_, "doNothing", "Guild member logout", _x, _y)
_y += 20

eventPickItem = QtBind.createCheckBox(gui_, "doNothing", "Item picked up (vSRO)", _x, _y)
_y += 20
eventPickRare = QtBind.createCheckBox(gui_, "doNothing", "Item (Rare) picked up", _x, _y)
_y += 20
eventPickEquipable = QtBind.createCheckBox(gui_, "doNothing", "Item (Equipable) picked up", _x, _y)
_y += 20

configPage2={'eventMessageAll':eventMessageAll,'eventMessagePrivate':eventMessagePrivate,'eventMessageStall':eventMessageStall,'eventMessageParty':eventMessageParty,'eventMessageAcademy':eventMessageAcademy,'eventMessageGuild':eventMessageGuild,'eventMessageUnion':eventMessageUnion,'eventMessageGlobal':eventMessageGlobal,'eventMessageNotice':eventMessageNotice,'eventMessageGM':eventMessageGM,'eventPartyJoined':eventPartyJoined,'eventPartyLeft':eventPartyLeft,'eventPartyMemberJoin':eventPartyMemberJoin,'eventPartyMemberLeft':eventPartyMemberLeft,'eventPartyMemberLevelUp':eventPartyMemberLevelUp,'eventGuildNoticeChanged':eventGuildNoticeChanged,'eventGuildMemberLogin':eventGuildMemberLogin,'eventGuildMemberLogout':eventGuildMemberLogout,'eventPickItem':eventPickItem,'eventPickRare':eventPickRare,'eventPickEquipable':eventPickEquipable}

def getPath():
	return get_config_dir() + pName + "\\"

def getConfig():
	return getPath() + character_data['server'] + "_" + character_data['name'] + ".json"

def loadDefaultConfig():
	QtBind.setText(gui, leNtfyServer, NTFY_DEFAULT_SERVER)
	QtBind.setText(gui, leNtfyTopic, "")
	
	for name, item in configPage1.items():
		QtBind.setChecked(gui, item, False)

	for name, item in configPage2.items():
		QtBind.setChecked(gui, item, False)

def saveConfigs():
	global ntfyServer, ntfyTopic
	ntfyServer = QtBind.text(gui, leNtfyServer)
	ntfyTopic = QtBind.text(gui, leNtfyTopic)

	data = {}
	data["ntfyServer"] = ntfyServer
	data["ntfyTopic"] = ntfyTopic

	if checkConnection():
		configItems = {}
		data["ConfigItems"] = configItems

		for name, item in configPage1.items():
			configItems[name] = QtBind.isChecked(gui, item)

		for name, item in configPage2.items():
			configItems[name] = QtBind.isChecked(gui_, item)

		with open(getConfig(),"w") as f:
			f.write(json.dumps(data, indent=4, sort_keys=True))
			
		log("Plugin: "+pName+" configs has been saved")

def loadConfigs():
	loadDefaultConfig()
	if checkConnection():
		global isConnected, ntfyServer, ntfyTopic
		isConnected = True

		if os.path.exists(getConfig()):
			data = {}
			with open(getConfig(),"r") as f:
				data = json.load(f)

			if "ntfyServer" in data and data["ntfyServer"]:
				ntfyServer = data["ntfyServer"]
				QtBind.setText(gui, leNtfyServer, data["ntfyServer"])
			if "ntfyTopic" in data and data["ntfyTopic"]:
				ntfyTopic = data["ntfyTopic"]
				QtBind.setText(gui, leNtfyTopic, data["ntfyTopic"])

			if "ConfigItems" in data:
				triggers = data["ConfigItems"]

				if "eventCharacterConnected" in triggers:
					QtBind.setChecked(gui, eventCharacterConnected, triggers["eventCharacterConnected"])
				if "eventCharacterDisconnected" in triggers:
					QtBind.setChecked(gui, eventCharacterDisconnected, triggers["eventCharacterDisconnected"])

				if "eventMessageUniqueSpawned" in triggers:
					QtBind.setChecked(gui, eventMessageUniqueSpawned, triggers["eventMessageUniqueSpawned"])
				if "eventMessageUniqueKilled" in triggers:
					QtBind.setChecked(gui, eventMessageUniqueKilled, triggers["eventMessageUniqueKilled"])

				if "eventMessageCTF" in triggers:
					QtBind.setChecked(gui, eventMessageCTF, triggers["eventMessageCTF"])
				if "eventMessageBA" in triggers:
					QtBind.setChecked(gui, eventMessageBA, triggers["eventMessageBA"])
				if "eventMessageFortress" in triggers:
					QtBind.setChecked(gui, eventMessageFortress, triggers["eventMessageFortress"])
				if "eventMessageCHunter" in triggers:
					QtBind.setChecked(gui, eventMessageCHunter, triggers["eventMessageCHunter"])
				if "eventMessageCThief" in triggers:
					QtBind.setChecked(gui, eventMessageCThief, triggers["eventMessageCThief"])

				if "eventNearGM" in triggers:
					QtBind.setChecked(gui, eventNearGM, triggers["eventNearGM"])
				if "eventNearUnique" in triggers:
					QtBind.setChecked(gui, eventNearUnique, triggers["eventNearUnique"])
				if "eventNearHunter" in triggers:
					QtBind.setChecked(gui, eventNearHunter, triggers["eventNearHunter"])
				if "eventNearThief" in triggers:
					QtBind.setChecked(gui, eventNearThief, triggers["eventNearThief"])
				if "eventCharacterAttacked" in triggers:
					QtBind.setChecked(gui, eventCharacterAttacked, triggers["eventCharacterAttacked"])
				if "eventCharacterDied" in triggers:
					QtBind.setChecked(gui, eventCharacterDied, triggers["eventCharacterDied"])
				if "eventMountDied" in triggers:
					QtBind.setChecked(gui, eventMountDied, triggers["eventMountDied"])

				if "eventMessageQuest" in triggers:
					QtBind.setChecked(gui, eventMessageQuest, triggers["eventMessageQuest"])
				if "eventBotAlchemy" in triggers:
					QtBind.setChecked(gui, eventBotAlchemy, triggers["eventBotAlchemy"])
				if "eventMessageItemSold" in triggers:
					QtBind.setChecked(gui, eventMessageItemSold, triggers["eventMessageItemSold"])

				if "eventMessageAll" in triggers:
					QtBind.setChecked(gui_, eventMessageAll, triggers["eventMessageAll"])
				if "eventMessagePrivate" in triggers:
					QtBind.setChecked(gui_, eventMessagePrivate, triggers["eventMessagePrivate"])
				if "eventMessageStall" in triggers:
					QtBind.setChecked(gui_, eventMessageStall, triggers["eventMessageStall"])
				if "eventMessageParty" in triggers:
					QtBind.setChecked(gui_, eventMessageParty, triggers["eventMessageParty"])
				if "eventMessageAcademy" in triggers:
					QtBind.setChecked(gui_, eventMessageAcademy, triggers["eventMessageAcademy"])
				if "eventMessageGuild" in triggers:
					QtBind.setChecked(gui_, eventMessageGuild, triggers["eventMessageGuild"])
				if "eventMessageUnion" in triggers:
					QtBind.setChecked(gui_, eventMessageUnion, triggers["eventMessageUnion"])
				if "eventMessageGlobal" in triggers:
					QtBind.setChecked(gui_, eventMessageGlobal, triggers["eventMessageGlobal"])
				if "eventMessageNotice" in triggers:
					QtBind.setChecked(gui_, eventMessageNotice, triggers["eventMessageNotice"])
				if "eventMessageGM" in triggers:
					QtBind.setChecked(gui_, eventMessageGM, triggers["eventMessageGM"])

				if "eventPartyJoined" in triggers:
					QtBind.setChecked(gui_, eventPartyJoined, triggers["eventPartyJoined"])
				if "eventPartyLeft" in triggers:
					QtBind.setChecked(gui_, eventPartyLeft, triggers["eventPartyLeft"])
				if "eventPartyMemberJoin" in triggers:
					QtBind.setChecked(gui_, eventPartyMemberJoin, triggers["eventPartyMemberJoin"])
				if "eventPartyMemberLeft" in triggers:
					QtBind.setChecked(gui_, eventPartyMemberLeft, triggers["eventPartyMemberLeft"])
				if "eventPartyMemberLevelUp" in triggers:
					QtBind.setChecked(gui_, eventPartyMemberLevelUp, triggers["eventPartyMemberLevelUp"])

				if "eventGuildNoticeChanged" in triggers:
					QtBind.setChecked(gui_, eventGuildNoticeChanged, triggers["eventGuildNoticeChanged"])
				if "eventGuildMemberLogin" in triggers:
					QtBind.setChecked(gui_, eventGuildMemberLogin, triggers["eventGuildMemberLogin"])
				if "eventGuildMemberLogout" in triggers:
					QtBind.setChecked(gui_, eventGuildMemberLogout, triggers["eventGuildMemberLogout"])

				if "eventPickItem" in triggers:
					QtBind.setChecked(gui_, eventPickItem, triggers["eventPickItem"])
				if "eventPickRare" in triggers:
					QtBind.setChecked(gui_, eventPickRare, triggers["eventPickRare"])
				if "eventPickEquipable" in triggers:
					QtBind.setChecked(gui_, eventPickEquipable, triggers["eventPickEquipable"])

def checkConnection():
	global character_data
	character_data = get_character_data()
	if not (character_data and "name" in character_data and character_data["name"]):
		character_data = None
	return character_data

def getBattleArenaText(t):
	if t == 0:
		return 'Random'
	if t == 1:
		return 'Party'
	if t == 2:
		return 'Guild'
	if t == 3:
		return 'Job'
	return 'Unknown['+str(t)+']'

def getFortressText(code):
	if code == 1:
		return "Jangan"
	if code == 3:
		return "Hotan"
	if code == 6:
		return "Bandit"
	return 'Fortress #'+str(code)

def getPartyTextList(party):
	if not party:
		return ''
	txt = '```\n'
	for joinId, member in party.items():
		txt += member['name'].ljust(13)
		txt += (' (Lvl.'+str(member['level'])+')').ljust(10)
		if member['guild']:
			txt += ' ['+member['guild']+']'
		txt += '\n'
	txt += '```'
	return txt

def getGuildTextList(guild):
	if not guild:
		return ''
	txt = '```\n'
	for memberID, member in guild.items():
		txt += member['name'].ljust(13)
		txt += (' (Lvl.'+str(member['level'])+')').ljust(10)
		if member['online']:
			txt += ' - [On]'
		else:
			txt += ' - [Off]'
		txt += '\n'
	txt += '```'
	return txt

def getGoldText():
	global character_data
	character_data = get_character_data()
	return "{:,}".format(character_data['gold'])

def getRaceText(servername):
	if '_CH_' in servername:
		return '(CH)'
	if '_EU_' in servername:
		return '(EU)'
	return ''

def getGenreText(servername):
	if '_M_' in servername:
		return '[M]'
	if '_W_' in servername:
		return '[F]'
	return ''

def getSoXText(servername,level):
	if level < 101:
		if servername.endswith('A_RARE'):
			return '^Star'
		elif servername.endswith('B_RARE'):
			return '^Moon'
		elif servername.endswith('C_RARE'):
			return '^Sun'
	else:
		if servername.endswith('A_RARE'):
			return '^Nova'
		elif servername.endswith('B_RARE'):
			return '^Rare'
		elif servername.endswith('C_RARE'):
			return '^Legend'
		elif servername.endswith('SET_A'):
			return '^Egy A'
		elif servername.endswith('SET_B'):
			return '^Egy B'
	return ''

def getConsignmentTownText(code):
	if code == 0:
		return 'Jangan'
	if code == 1:
		return 'Donwhang'
	return 'Town #'+str(code)

def ParseItem(data,index):
	rentID = struct.unpack_from('<I', data, index)[0]
	index += 4 # Rent id
	# TO DO: Parse rentability stuffs
	index += 4 # UnkUInt01
	itemID = struct.unpack_from('<I', data, index)[0]
	index += 4 # Item ID
	itemData = get_item(itemID)
	# IsEquipable
	if itemData['tid1'] == 1:
		index += 1 # plus
		index += 8 # stats
		index += 4 # durability
		count = data[index]
		index += 1 # magic options
		for i in range(count):
			index += 4 # id
			index += 4 # value
		index += 1 # (1)
		count = data[index]
		index += 1 # sockets
		for i in range(count):
			index += 1 # slot
			index += 4 # id
			index += 4 # value
		index += 1 # (2)
		count = data[index]
		index += 1 # adv
		for i in range(count):
			index += 1 # slot
			index += 4 # id
			index += 4 # value
		index += 4 # UnkUint02
	# IsCOS
	elif itemData['tid1'] == 2:
		# IsPet
		if itemData['tid2'] == 1:
			state = data[index]
			index += 1 # state
			if state != 1:
				index += 4 # model
				index += 2 + struct.unpack_from('<H', data, index)[0] # name
				# NeedsTime
				if data['tid3'] == 2:
					index += 4 # endtime
				index += 1 # UnkByte01
		# IsTransform
		elif itemData['tid2'] == 2:
			index += 4 # model
		# IsCube?
		elif itemData['tid2'] == 3:
			index += 4 # quantity
	# IsETC
	elif itemData['tid1'] == 3:
		index += 2 # quantity
		# IsAlchemy
		if itemData['tid2'] == 11:
			# IsStone
			if itemData['tid3'] == 1 or itemData['tid3'] == 2:
				index += 1 # assimilation
		# IsCard
		elif itemData['tid2'] == 14 and itemData['tid3'] == 2:
			count = data[index]
			index += 1 # params
			for i in range(count):
				index += 4 # id
				index += 4 # value
	return index,itemData

def joined_game():
	loadConfigs()
	if QtBind.isChecked(gui, eventCharacterConnected):
	    ntfy("Connected to the game", character_data['name'], ["green_circle"])

def disconnected():
	global isConnected
	if isConnected:
		isConnected = False
		if QtBind.isChecked(gui, eventCharacterDisconnected):
			ntfy("You has been disconnected", character_data['name'], ["red_circle"])

def handle_chat(t,player,msg):
	itemLink = re.search('([0-9]*)',msg) # Check if contains item linking
	if itemLink:
		global chat_data
		links = itemLink.groups()
		for i in range(len(links)):
			uid = int(links[i])
			if uid in chat_data:
				item = chat_data[uid]
				race = getRaceText(item['servername'])
				genre = getGenreText(item['servername'])
				sox = getSoXText(item['servername'],item['level'])
				msg = msg.replace(''+links[i]+'','`< '+item['name']+(' '+race if race else '')+(' '+genre if genre else '')+(' '+sox if sox else '')+' >`')
			else:
				msg = msg.replace(''+links[i]+'','`< '+links[i]+' >`')

    # Check message type
	if t == 1:
		if QtBind.isChecked(gui_, eventMessageAll):
			ntfy("[General] " + player + ": " + msg, character_data['name'], ["speech_balloon"])
	elif t == 2:
		if QtBind.isChecked(gui_, eventMessagePrivate):
			ntfy("[Private] " + player + ": " + msg, character_data['name'], ["speech_balloon"])
	elif t == 9:
		if QtBind.isChecked(gui_, eventMessageStall):
			ntfy("[Stall] " + player + ": " + msg, character_data['name'], ["speech_balloon"])
	elif t == 4:
		if QtBind.isChecked(gui_, eventMessageParty):
			ntfy("[Party] " + player + ": " + msg, character_data['name'], ["speech_balloon"])
	elif t == 16:
		if QtBind.isChecked(gui_, eventMessageAcademy):
			ntfy("[Academy] " + player + ": " + msg, character_data['name'], ["speech_balloon"])
	elif t == 5:
		if QtBind.isChecked(gui_, eventMessageGuild):
			ntfy("[Guild] " + player + ": " + msg, character_data['name'], ["speech_balloon"])
	elif t == 11:
		if QtBind.isChecked(gui_, eventMessageUnion):
			ntfy("[Union] " + player + ": " + msg, character_data['name'], ["speech_balloon"])
	elif t == 6:
		if QtBind.isChecked(gui_, eventMessageGlobal):
			ntfy("[Global] " + player + ": " + msg, character_data['name'], ["speech_balloon"])
	elif t == 7:
		if QtBind.isChecked(gui_, eventMessageNotice):
			ntfy("[Notice] " + msg, character_data['name'], ["loudspeaker"])
	elif t == 3:
		if QtBind.isChecked(gui_, eventMessageGM):
			ntfy("[GM] " + player + ": " + msg, character_data['name'], ["speech_balloon"])

def handle_event(t, data):
	# Filter events
	if t == 9:
		if QtBind.isChecked(gui, eventNearGM):
			ntfy("GM " + data + " is near to you!", character_data['name'], ["warning"])
	elif t == 0:
		if QtBind.isChecked(gui, eventNearUnique):
			ntfy(data + " unique is near to you!", character_data['name'], ["purple_circle"])
	elif t == 1:
		if QtBind.isChecked(gui, eventNearHunter):
			ntfy("Hunter/Trader " + data + " is near to you!", character_data['name'], ["warning"])
	elif t == 2:
		if QtBind.isChecked(gui, eventNearThief):
			ntfy("Thief " + data + " is near to you!", character_data['name'], ["warning"])
	elif t == 4:
		if QtBind.isChecked(gui, eventCharacterAttacked):
			ntfy(data + " is attacking you!", character_data['name'], ["warning"])
	elif t == 7:
		if QtBind.isChecked(gui, eventCharacterDied):
			ntfy("You died", character_data['name'], ["warning"])
	elif t == 3:
		if QtBind.isChecked(gui, eventMountDied):
			pet = get_pets()[data]
			ntfy("Your pet " + (pet['type'].title()) + " died", character_data['name'], ["warning"])
	elif t == 5:
		if QtBind.isChecked(gui_, eventPickRare):
			item = get_item(int(data))
			race = getRaceText(item['servername'])
			genre = getGenreText(item['servername'])
			sox = getSoXText(item['servername'],item['level'])
			ntfy("Rare Item picked up " + item['name'] + (' ' + race if race else '') + (' ' + genre if genre else '') + (' ' + sox if sox else ''), character_data['name'], ["tada"])
	elif t == 6:
		if QtBind.isChecked(gui_, eventPickEquipable):
			item = get_item(int(data))
			race = getRaceText(item['servername'])
			genre = getGenreText(item['servername'])
			sox = getSoXText(item['servername'],item['level'])
			ntfy("Equipable Item picked up " + item['name'] + (' ' + race if race else '') + (' ' + genre if genre else '') + (' ' + sox if sox else ''), character_data['name'], ["tada"])
	elif t == 8:
		if QtBind.isChecked(gui, eventBotAlchemy):
			ntfy("Auto alchemy has been completed", character_data['name'], ["tada"])

def handle_joymax(opcode, data):
	# globals used in more than one IF statement
	global party_data, hasStall

	# SERVER_NOTICE_UPDATE
	if opcode == 0x300C:
		updateType = data[0]
		if updateType == 5:
			if QtBind.isChecked(gui, eventMessageUniqueSpawned):
				modelID = struct.unpack_from("<I",data,2)[0]
				uniqueName = get_monster(int(modelID))['name']
				ntfy(uniqueName+" has appeared", character_data['name'], ["purple_circle"])
		elif updateType == 6:
			if QtBind.isChecked(gui, eventMessageUniqueKilled):
				modelID = struct.unpack_from("<I",data,2)[0]
				killerNameLength = struct.unpack_from('<H', data, 6)[0]
				killerName = struct.unpack_from('<' + str(killerNameLength) + 's', data, 8)[0].decode('cp1252')
				uniqueName = get_monster(int(modelID))['name']
				ntfy(uniqueName+" killed by " + killerName, character_data['name'], ["purple_circle"])
		elif updateType == 29:
			jobType = data[2]
			if jobType == 1:
				if QtBind.isChecked(gui, eventMessageCHunter):
					progressType = data[3]
					if progressType == 0:
						ntfy("Hunter Consignment trade will start at 10 minutes", character_data['name'], ["dromedary_camel"])
					elif progressType == 1:
						ntfy("Hunter Consignment trade started at " + getConsignmentTownText(data[4]), character_data['name'], ["dromedary_camel"])
					elif progressType == 2:
						ntfy("Hunter Consignment trade has ended", character_data['name'], ["dromedary_camel"])
			elif jobType == 2:
				if QtBind.isChecked(gui, eventMessageCThief):
					progressType = data[3]
					if progressType == 0:
						ntfy("Thief Consignment trade will start at 10 minutes", character_data['name'], ["dromedary_camel"])
					elif progressType == 1:
						ntfy("Thief Consignment trade started at " + getConsignmentTownText(data[4]), character_data['name'], ["dromedary_camel"])
					elif progressType == 2:
						ntfy("Thief Consignment trade has ended", character_data['name'], ["dromedary_camel"])
	# SERVER_BA_NOTICE
	elif opcode == 0x34D2:
		if QtBind.isChecked(gui, eventMessageBA):
			updateType = data[0]
			if updateType == 2:
				ntfy("Battle Arena " + getBattleArenaText(data[1]) + " will start at 10 minutes", character_data['name'], ["coin"])
			elif updateType == 13:
				ntfy("Battle Arena " + getBattleArenaText(data[1]) + " will start at 5 minutes", character_data['name'], ["coin"])
			elif updateType == 14:
				ntfy("Battle Arena " + getBattleArenaText(data[1]) + " will start at 1 minutes", character_data['name'], ["coin"])
			elif updateType == 3:
				ntfy("Battle Arena registration period has ended", character_data['name'], ["coin"])
			elif updateType == 4:
				ntfy("Battle Arena started", character_data['name'], ["coin"])
			elif updateType == 5:
				ntfy("Battle Arena has ended", character_data['name'], ["coin"])
	# SERVER_CTF_NOTICE
	elif opcode == 0x34B1:
		if QtBind.isChecked(gui, eventMessageCTF):
			updateType = data[0]
			if updateType == 2:
				ntfy("Capture the Flag will start at 10 minutes", character_data['name'], ["triangular_flag_on_post"])
			elif updateType == 13:
				ntfy("Capture the Flag will start at 5 minutes", character_data['name'], ["triangular_flag_on_post"])
			elif updateType == 14:
				ntfy("Capture the Flag will start at 1 minute", character_data['name'], ["triangular_flag_on_post"])
			elif updateType == 3:
				ntfy("Capture the Flag started", character_data['name'], ["triangular_flag_on_post"])
			elif updateType == 9:
				ntfy("Capture the Flag has ended", character_data['name'], ["triangular_flag_on_post"])
	# SERVER_QUEST_UPDATE
	elif opcode == 0x30D5:
		if QtBind.isChecked(gui, eventMessageQuest):
			if data[0] == 2 and data[10] == 2: # Quest update & Quest completed
				questID = struct.unpack_from("<I",data,1)[0]
				quest = get_quests()[questID]
				ntfy(quest['name'] + " Quest has been completed", character_data['name'], ["scroll"])
	# SERVER_INVENTORY_ITEM_MOVEMENT
	elif opcode == 0xB034:
		# vSRO filter
		locale = get_locale()
		if locale == 22:
			# Check success
			if data[0] == 1:
				if QtBind.isChecked(gui_, eventPickItem):
					# parse
					updateType = data[1]
					if updateType == 6: # Ground
						notify_pickup(struct.unpack_from("<I",data,7)[0])
					elif updateType == 17: # Pet
						notify_pickup(struct.unpack_from("<I",data,11)[0])
					elif updateType == 28: # Pet (Full/Quest)
						slotInventory = data[6]
						if slotInventory != 254:
							notify_pickup(struct.unpack_from("<I",data,11)[0])
	# SERVER_FW_NOTICE
	elif opcode == 0x385F:
		if QtBind.isChecked(gui, eventMessageFortress):
			updateType = data[0]
			if updateType == 1:
				ntfy("Fortress War will start in 30 minutes", character_data['name'], ["fleur_de_lis"])
			elif updateType == 2:
				ntfy("Fortress War started", character_data['name'], ["fleur_de_lis"])
			elif updateType == 3:
				ntfy("Fortress War has 30 minutes before the end", character_data['name'], ["fleur_de_lis"])
			elif updateType == 4:
				ntfy("Fortress War has 20 minutes before the end", character_data['name'], ["fleur_de_lis"])
			elif updateType == 5:
				ntfy("Fortress War has 10 minutes before the end", character_data['name'], ["fleur_de_lis"])
			elif updateType == 8:
				fortressID = struct.unpack_from("<I",data,1)[0]
				guildNameLength = struct.unpack_from("<H",data,5)[0]
				guildName = data[7:7+guildNameLength].decode('cp1252')
				ntfy("Fortress War " + getFortressText(fortressID) + " has been taken by " + guildName, character_data['name'], ["fleur_de_lis"])
			elif updateType == 9:
				ntfy("Fortress War has 1 minute before the end", character_data['name'], ["fleur_de_lis"])
			elif updateType == 6:
				ntfy("Fortress War has ended", character_data['name'], ["fleur_de_lis"])
	# SERVER_PARTY_DATA
	elif opcode == 0x3065:
		if QtBind.isChecked(gui_, eventPartyJoined):
			party_data = get_party()
			ntfy("You has been joined to the party\n"+getPartyTextList(party_data), character_data['name'], ["blue_square"])
	# SERVER_PARTY_UPDATE
	elif opcode == 0x3864:
		updateType = data[0]
		if updateType == 1:
			if QtBind.isChecked(gui_, eventPartyLeft):
				ntfy("You left the party", character_data['name'], ["blue_square"])
		elif updateType == 2:
			if QtBind.isChecked(gui_, eventPartyMemberJoin):
				party_data = get_party()
				memberNameLength = struct.unpack_from('<H',data,6)[0]
				memberName = struct.unpack_from('<'+str(memberNameLength)+'s',data,8)[0].decode('cp1252')
				ntfy(memberName+" joined to the party\n"+getPartyTextList(party_data), character_data['name'], ["blue_square"])
		elif updateType == 3:
			joinID = struct.unpack_from("<I",data,1)[0]
			memberName = party_data[joinID]['name']
			party_data = get_party()
			if memberName == character_data['name']:
				if QtBind.isChecked(gui_, eventPartyLeft):
					ntfy("You left the party", character_data['name'], ["blue_square"])
			else:
				if QtBind.isChecked(gui_, eventPartyMemberLeft):
					ntfy(memberName+" left the party\n"+getPartyTextList(party_data), character_data['name'], ["blue_square"])
		elif updateType == 6: # update member
			if data[5] == 2: # level
				if QtBind.isChecked(gui_, eventPartyMemberLevelUp):
					joinID = struct.unpack_from("<I",data,1)[0]
					newLevel = data[6]
					oldLevel = party_data[joinID]['level']
					party_data[joinID]['level'] = newLevel
					if oldLevel < newLevel:
						ntfy(party_data[joinID]['name']+"` level up!\n"+getPartyTextList(party_data), character_data['name'], ["blue_square"])
	# SERVER_STALL_CREATE_RESPONSE
	elif opcode == 0xB0B1:
		if data[0] == 1:
			hasStall = True
	# SERVER_STALL_DESTROY_RESPONSE
	elif opcode == 0xB0B2:
		if data[0] == 1:
			hasStall = False
	# SERVER_STALL_ENTITY_ACTION
	elif opcode == 0x30B7:
		if data[0] == 3 and hasStall:
			if QtBind.isChecked(gui, eventMessageItemSold):
				playerNameLength = struct.unpack_from('<H', data, 2)[0]
				playerName = struct.unpack_from('<' + str(playerNameLength) + 's', data, 4)[0].decode('cp1252')
				ntfy(playerName+" bought an item from your stall\nYour gold now: "+getGoldText(), character_data['name'], ["moneybag"])
	# SERVER_CHAT_ITEM_DATA
	elif opcode == 0xB504:
		global chat_data
		index = 2
		for i in range(data[1]):
			uid = struct.unpack_from('<I', data, index)[0]
			index += 4 # Unique ID
			try:
				index, item = ParseItem(data,index)
				chat_data[uid] = item
			except Exception as ex:
				log('Plugin: Saving error parsing item (JellyDix)...')
				# Make easy log file for user
				with open(getPath()+"error.log","a") as f:
					f.write("["+str(ex)+"] Server: (Opcode) 0x" + '{:02X}'.format(opcode) + " (Data) "+ ("None" if not data else ' '.join('{:02X}'.format(x) for x in data))+'\r\n')
				break
	# GUILD_INFO_UPDATE
	elif opcode == 0x38F5:
		updateType = data[0]
		if updateType == 6: # member update
			memberID = struct.unpack_from("<I",data,1)[0]
			infoType = data[5]
			if infoType == 2: # session
				if data[6]:
					if QtBind.isChecked(gui_, eventGuildMemberLogout):
						member = get_guild()[memberID]
						ntfy("Guild member " + member['name'] + " has logged off", character_data['name'], ["red_circle"])
				else:
					if QtBind.isChecked(gui_, eventGuildMemberLogin):
						member = get_guild()[memberID]
						# Avoid myself
						if member['name'] != character_data['name']:
							ntfy("Guild member " + member['name'] + " has logged on", character_data['name'], ["green_circle"])
		elif updateType == 5: # general info
			infoType = data[1]
			if infoType == 16: # notice changed
				if QtBind.isChecked(gui_, eventGuildNoticeChanged):
					index = 2
					titleLength = struct.unpack_from('<H', data, index)[0]
					title = struct.unpack_from('<' + str(titleLength) + 's', data,index+2)[0].decode('cp1252')
					index+=2+titleLength
					textLength = struct.unpack_from('<H', data,index)[0]
					text = struct.unpack_from('<' + str(textLength) + 's', data, index+2)[0].decode('cp1252')
					ntfy("Guild notice updated\nTitle: " + title + "\nMessage: " + text, character_data['name'], ["loudspeaker"])
	return True

def notify_pickup(itemID): # for vSRO
	if QtBind.isChecked(gui_, eventPickItem):
		item = get_item(itemID)
		race = getRaceText(item['servername'])
		genre = getGenreText(item['servername'])
		sox = getSoXText(item['servername'],item['level'])
		ntfy("Item picked up "+item['name']+(' '+race if race else '')+(' '+genre if genre else '')+(' '+sox if sox else ''), character_data['name'], ["gift"])

def ntfy(message, title="", tags=[], priority=3):
    if not ntfyServer or not ntfyTopic:
        return
    Timer(0.001, ntfyPush,(message,title, tags, priority)).start()

def ntfyPush(message, title="", tags=[], priority=3):
    ntfyAddr = ntfyServer
    if ntfyAddr[-1] != '/':
        ntfyAddr += '/'
    data = {"message": message, "priority": priority}
    if title:
        data["title"] = title
    if tags:
        data["tags"] = tags
    headers = {
        'Content-Type': 'application/json',
    }
    _ = urllib.request.urlopen(ntfyAddr, headers=headers, data = json.dumps(data).encode())


# Plugin loaded
log('Plugin: '+pName+' v'+pVersion+' successfully loaded')

if not os.path.exists(getPath()):
	# Creating configs folder
	os.makedirs(getPath())
	log('Plugin: '+pName+' folder has been created')
# Adding RELOAD plugin support
loadConfigs()
