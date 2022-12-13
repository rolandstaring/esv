from datetime import date, datetime
import numpy as np

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

###############
## Apparaten ##
###############

class Apparaat:
	def __init__ (self, naam, prijs):
		self.naam = naam
		self.prijs = prijs		
		
				
	def __repr__(self):
		return '%s van %s voor € %s ' % (self.soort, self.naam, self.prijs)

class Zonnepanelen(Apparaat):
	soort = 'zonnepanelen'
	def __init__ (self, naam, prijs, watt_pp, aantal, jaar_van_aanschaf, schaduw_factor):
		Apparaat.__init__(self, naam,prijs ) 
		
		self.watt_pp = watt_pp	# Hoeveelheid Watt per paneel
		self.aantal = aantal
		self.jaar_van_aanschaf = jaar_van_aanschaf
		self.schaduw_factor = schaduw_factor
	
	def reassign_values_from_list(self, values_list):
		#self.naam = str(values_list[0].text()) 	
		self.prijs= int(values_list[0].text())	
		self.watt_pp = int(values_list[1].text())	
		self.aantal = int(values_list[2].text())	
		self.jaar_van_aanschaf = int(values_list[3].text())	
		self.schaduw_factor = float(values_list[4].text())	
	
	def bereken_leeftijd_panelen(self):
		return date.today().year-self.jaar_van_aanschaf	
	
	def return_values_list(self):
		return [self.naam, self.prijs, self.watt_pp, self.aantal, self.jaar_van_aanschaf, self.schaduw_factor]
	
	def return_labels_list(self):
		return ['Naam', 'Prijs', 'Watt per paneel', 'Aantal', 'Jaar van Aanschaf', 'Schaduw factor']	
	
	def return_keys_list(self):
		return ['naam', 'prijs', 'watt_pp', 'aantal', 'jaar_van_aanschaf', 'schaduw_factor']	

	def bereken_gas_besparing(self,huis):
		return 0 # met zonnepanelen bespaar je geen gas

	def bereken_stroom_verbruik(self, huis):
		return 0 # zonnepanelen verbruiken geen stroom

	def bereken_start_cap(self):
		return round(self.schaduw_factor * self.watt_pp * self.aantal)
	
	def bereken_effectiviteit_panelen(self):
		degradatie_zonnepanelen_pjaar = 0.7 # % degradatie van panalen per jaar
		return (100-(degradatie_zonnepanelen_pjaar*self.bereken_leeftijd_panelen()))/100
	
	def bereken_huidige_cap(self):
		return round(self.bereken_effectiviteit_panelen() * self.bereken_start_cap())

	
	def make_dict(self):
	
		return dict(zip(self.return_keys_list(), self.return_values_list()))

		

	def __repr__(self):
		return '%s %s '	 % (self.aantal , Apparaat.__repr__(self))

class Zonneboiler(Apparaat):
	soort = 'zonneboiler'
	def __init__ (self, naam, prijs, cap_kwh, watt):
		Apparaat.__init__(self,naam,prijs)
		self.cap_kwh = cap_kwh
		self.watt = watt  
	
	def reassign_values_from_list(self, values_list):
		#self.naam = values_list[0].text()	
		self.prijs = int(values_list[0].text())	
		self.cap_kwh =int(values_list[1].text())	
		self.watt = int(values_list[2].text())	
	
	def return_values_list(self):
		return [self.naam, self.prijs, self.cap_kwh, self.watt]
	
	def return_labels_list(self):
		return ['Naam', 'Prijs', 'Capaciteit', 'Watt']
	
	def return_keys_list(self):
		return ['naam', 'prijs', 'cap_kwh','watt']
	
	def bereken_stroom_verbruik(self,huis):
		aantal_uren_jaar = 2000
		return round((aantal_uren_jaar*self.watt)/1000) # in kwh
	
	def bereken_gas_besparing(self,huis):
		return round(self.cap_kwh / huis.Kwh_voor_1m3_Gas)
	
	def make_dict(self):
		return dict(zip(return_keys_list, return_values_list))
			
	def __repr__(self):
		return ' %s '  % (Apparaat.__repr__(self))

class Warmtepomp(Apparaat):
	soort = 'warmtepomp'
	def __init__ (self, naam, prijs, cop, gbc):
		Apparaat.__init__(self,naam,prijs )
		self.cop = cop # efficiency factor
		self.gbc = gbc # gas besparings percentage
	
	def reassign_values_from_list(self, values_list):
		#self.naam = values_list[0].text()	
		self.prijs = int(values_list[0].text())	
		self.cop = float(values_list[1].text())	
		self.gbc = float(values_list[2].text())	
	
	def return_labels_list(self):
		return ['Naam', 'Prijs', 'CoP', 'Aantal', 'Gas besparing %']
		
	def return_values_list(self):
		return [self.naam, self.prijs, self.cop, self.gbc]	
	
	def return_keys_list(self):
		return [ 'naam', 'prijs', 'cop', 'gbc']
	
	def bereken_gas_besparing(self, huis):
		return round(self.gbc * huis.energie_verbruik.gas_verbruik_jaar)

	
	def bereken_stroom_verbruik(self,huis):
		return round((self.bereken_gas_besparing(huis) * huis.Kwh_voor_1m3_Gas)/self.cop)
		
	def make_dict(self):
		return dict(zip(keys_list, values_list))	
		
	def __repr__(self):
		return ' %s '	 % (Apparaat.__repr__(self))
		
class Thuisbatterij(Apparaat):
	soort = 'thuisbatterij'
	def __init__ (self, naam, prijs, cap ):
		Apparaat.__init__(self,naam,prijs)
		self.cap = cap
	
	def reassign_values_from_list(self, values_list):
		#self.naam = values_list[0].text()	
		self.prijs = int(values_list[0].text())	
		self.cap =int(values_list[1].text())	
	
	
	def return_labels_list(self):
		return ['Naam', 'Prijs', 'Capaciteit']
		
	def return_values_list(self):
		return [self.naam, self.prijs, self.cap]	
	
	def return_keys_list(self):
		return [ 'naam', 'prijs', 'cap']
	
	def bereken_gas_besparing(self,huis):
		return 0 # met een batterij bespaar je geen gas
	
	def bereken_stroom_verbruik(self,huis):
		return 0 # zonnepanelen verbruiken geen stroom

	def make_dict(self):
	
		return dict(zip(self.return_keys_list, self.return_values_list))
	
	def bereken_verhoging_direct_verbruik(self, KWp_zps, verbruik_factor):
		return verbruik_factor + np.log10(KWp_zps)*0.3 + (self.cap*0.001)/40 # inschatting/benadering


