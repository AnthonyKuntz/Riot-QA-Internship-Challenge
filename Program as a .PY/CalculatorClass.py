class Calculator(object):

	@staticmethod
	def notADamagingSpell(leveltip):
		return ( u('Damage')       not in leveltip[u('label')] and
				 u('Bonus Damage') not in leveltip[u('label')] and 
				 u('Base Damage')  not in leveltip[u('label')] )

	@staticmethod
	def fixIncorrectCooldowns(name, finalCooldown):
		if   name == u('Riposte'): 				finalCooldown = 15	 	# Incorrectly recorded as a 0 second cooldown
		elif name == u('Rend'): 				finalCooldown = 8 		# Incorrectly recorded as a 0 second cooldown
		elif name == u('Force of Will'): 		finalCooldown = 8 		# Incorrectly recorded as a 0 second cooldown
		elif name == u('Leap Strike'): 			finalCooldown = 6 		# Incorrectly recorded as a 0 second cooldown
		elif name == u('Sweeping Blade'): 		finalCooldown = 6 		# Incorrectly recorded as a 0 second cooldown
		elif name == u('Last Breath'): 			finalCooldown = 30 		# Incorrectly recorded as a 0 second cooldown
		elif name == u('Eye of Destruction'): 	finalCooldown = 10
		elif name == u('Poison Trail'): 		finalCooldown = 1 	# Since Singed does x dmg per second, set CD to 1
		elif name == u('Bola Strike'): 			finalCooldown = 10 	# Incorrectly recorded as a 0.5 second cooldown
		elif name == u('Battle Roar'): 			finalCooldown = 12 	# Incorrectly recorded as a 0.5 second cooldown
		elif name == u('Dance of Arrows'): 		finalCooldown = 2
		elif name == u('Electro Harpoon'): 		finalCooldown = 10 / 2 	# Incorrectly recorded as a 0.5 second cooldown
																  		# Two casts in 10 seconds --> 10 / 2 seconds
		elif name == u('Savagery'): 			finalCooldown = 4 		# Incorrectly recorded as a 0.5 second cooldown
		elif name == u('Shadow Dance'): 		finalCooldown = 15 		# Use recharge time rather than cooldown
		elif name == u('Excessive Force'): 		finalCooldown = 8 	  	# Use recharge time rather than cooldown
		elif name == u('Missile Barrage'): 		finalCooldown = 8 		# Use recharge time rather than cooldown

		elif name == u('Blood Thirst / Blood Price'): 
			attacksPerSecond = 1.2 # Reasonable Estimate for an Aatrox
			timeForThreeAttacks = 3 / attacksPerSecond
			finalCooldown = timeForThreeAttacks

		elif name == u('Vorpal Spikes'):
			attacksPerSecond = .779 # Reasonable Estimate for a Cho'gath
			timeForOneAttack = 1 / attacksPerSecond
			finalCooldown = timeForOneAttack

		return finalCooldown

	@staticmethod
	def noActualDamage(string):
		return ( "true" not in string and "True" not in string and 
				 "magic" not in string and "Magic" not in string and
				 "physical" not in string and "Physical" not in string )

	@staticmethod
	def removeGarbage(tooltip):
		while "seconds" in tooltip:
			secondsIndex = tooltip.find("seconds")
			tooltip = tooltip[:secondsIndex - 10] + tooltip[secondsIndex + 2:]
		while "%" in tooltip:
			modIndex = tooltip.find("%")
			tooltip = tooltip[:modIndex - 15] + tooltip[modIndex + 5:] 

		return tooltip

def u(string):
	return unicode(string)