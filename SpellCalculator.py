import json
import urllib2
from CalculatorClass import Calculator

def u(string):
	return unicode(string)

class RiotAPIandCalculator(Calculator):

	def __init__(self, amountRequested):
		self.myAPIKey = "ed127769-3732-4fd9-84b2-4729e013089c"
		self.championID = None

		self.url = "https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion/?champData=spells&api_key=" + self.myAPIKey

		self.data = json.load(urllib2.urlopen(self.url))

		self.attackDamageColor = "colorFF8C00"
		self.abilityPowerColor = "color99FF99"
		self.timeColor 		   = "colorFFFFFF"

		self.bestSpell = None
		self.bestDPS = 0
		self.amountRequested = amountRequested

		self.dictionaryOfDPS = dict()

		self.wrongKeySpells = [u('Dance of Arrows')]
		self.skipSpells = [ u('Light Binding'), u('Lucent Singularity'), u('Final Spark'), 
							u('Consume'), u('Silver Bolts'), u('Twisted Advance')]
							  # Skip due to omissions in Riot API,
							  # percent health based damage,
							  # or lack of damage to champion.


	def calculate(self, abilityPower, attackDamage, cooldownReduction):

		for champion in self.data[u('data')]:
			spellsList = self.data[u('data')][champion][u('spells')]
			# Dictionaries of each ability of the champion
			for spellDict in spellsList: 
				name = str(spellDict[u('name')])
				if name in self.skipSpells: continue

				leveltip = spellDict[u('leveltip')]

				if self.notADamagingSpell(leveltip): continue # Ignore non-Damaging Spells

				cooldownList = spellDict[u('cooldown')]
				finalCooldown = cooldownList[-1] # Assume spell is fully leveled
				finalCooldown = self.fixIncorrectCooldowns(name, finalCooldown)

				tooltip = spellDict[u('tooltip')]
				tooltip = self.removeGarbage(tooltip)

				adCoeffs = []
				apCoeffs = []
				baseDamages = []

				string = tooltip.split("amage")[0] 			# Splitting on "damage" doesn't work since the
												   			# word is sometimes capitalized in the API
				if self.noActualDamage(string): continue

				if self.attackDamageColor in string:
					# Find the AD Scaling
					colorIndex = tooltip.find(self.attackDamageColor)
					coeffIndex = tooltip[colorIndex:].find("{{") + colorIndex
					coeffIndex += len("{{ ")
					key = tooltip[coeffIndex: coeffIndex + len("e1")]
					if name in self.wrongKeySpells: key = u("e2") # Fix the improper key in Kindred's data
					adCoeffs.append( key )

				if self.abilityPowerColor in string:
					# Find the AP Scaling
					colorIndex = tooltip.find(self.abilityPowerColor)
					coeffIndex = tooltip[colorIndex:].find("{{") + colorIndex
					coeffIndex += len("{{ ")
					apCoeffs.append( tooltip[coeffIndex: coeffIndex + len("e1")] )

				a = tooltip.find( " }} <span class=")	# Look for any of the three CSS implementations
				b = tooltip.find( " }}<span class=")
				c = tooltip.find( " }} (<span class=")
				if a == -1: a = float("infinity")		# Disregard if not found
				if b == -1: b = float("infinity")		
				if c == -1: c = float("infinity")		

				baseDamageIndex = min( a, b, c) - len("e1")
				if baseDamageIndex == float("infinity"):
					baseDamageIndex = tooltip.find("e1 }}")
					if baseDamageIndex == -1: baseDamageIndex = None

				baseDamages.append( baseDamageIndex )

				adCoeffNums = []
				apCoeffNums = []
				baseDamage = 0

				found = False
				try: 
					found = False
					varsList = spellDict[u('vars')]
					for dictionary in varsList:
						for key in adCoeffs:
							if "key" in dictionary and dictionary["key"] == key:
								coeff = float(dictionary["coeff"][0])
								adCoeffNums.append( coeff )
								found = True
						for key in apCoeffs:
							if "key" in dictionary and dictionary["key"] == key:
								coeff = float(dictionary["coeff"][0])
								apCoeffNums.append( coeff )
								found = True

				except: 
					found = False

				if not found:
					# Some champions store the vars data in effect instead
					# This condition will search here if vars did not exist
					# or if the vars data was simply not found in vars
					for key in adCoeffs:
						numericalIndex = int(key[1:])
						adCoeffNums.append( spellDict[u('effect')][numericalIndex][-1] )
						if name == u('Rolling Thunder'): print 3457734583475
					for key in apCoeffs:
						numericalIndex = int(key[1:])
						apCoeffNums.append( spellDict[u('effect')][numericalIndex][-1] )	

				adCoeff = sum(adCoeffNums)
				apCoeff = sum(apCoeffNums)

				for index in baseDamages:
					if index == None: continue
					numericalIndex = int(tooltip[index+1:index+2])
					baseDamage += spellDict[u('effect')][numericalIndex][-1]
					# Assume fully leveled ability


				totalDamage = baseDamage + abilityPower * apCoeff + attackDamage * adCoeff

				effectiveCooldown = finalCooldown - finalCooldown * ( cooldownReduction / 100 ) if cooldownReduction != 100 else 1

				damagePerSecond = totalDamage / effectiveCooldown
			
				if damagePerSecond > self.bestDPS:
					self.bestDPS = damagePerSecond
					self.bestSpell = name

				pictureName = str(spellDict[u('image')][u('full')])

				self.dictionaryOfDPS[str(name)] = (round(damagePerSecond, 2), pictureName, str(champion), str(name))


		listOfSpells = sorted(self.dictionaryOfDPS, lambda x, y: int(self.dictionaryOfDPS[y][0] - self.dictionaryOfDPS[x][0]))

		listOfPictures = [ ( self.dictionaryOfDPS[info][1], 
						     self.dictionaryOfDPS[info][2], 
						     self.dictionaryOfDPS[info][3]  ) for info in listOfSpells]

		return listOfPictures[:self.amountRequested]
