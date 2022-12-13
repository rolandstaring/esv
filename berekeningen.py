from generic import Color, Formula

class InvesteringsBerekening:
	def __init__(self, inv_lijst,huis):
		self.inv_lijst =inv_lijst
		self.huis = huis
			
class GasBesparingen(InvesteringsBerekening):
	
	def print_besparingen_gas_html(self):
		html = f"<p><b>Gas besparingen</b></p>"
			
		if len(self.inv_lijst)>0:
			lab_list= []
			val_list = []
			for inv in self.inv_lijst:
				if inv.bereken_gas_besparing(self.huis) >0:
					lab_list.append(inv.naam)
					val_list.append(inv.bereken_gas_besparing(self.huis))
			if len(lab_list)>0:		
				html+= Formula.print_html_formula(lab_list,val_list,'+')
		else:
			html += '<p>Er zijn geen besparingen in gas</p>'
		
		return html	
		
	
	def print_besparingen_gas_tekst(self):
		gb_str = Color.BOLD + 'Gas besparingen \n'+ Color.END
		
		spacer_str1 = 15
		spacer_str2 = 15
		spacer_str3 = 6
		
		if len(self.inv_lijst)>0:
			for i in self.inv_lijst:
				if i.bereken_gas_besparing(self.huis) >0:
					gb_str += f"{i.soort:<{spacer_str1}}{i.naam:<{spacer_str2}}{str(i.bereken_gas_besparing(self.huis)):>{spacer_str3}} m3\n"
				
			len_spacers = spacer_str1 + spacer_str2 +spacer_str3 
			lijn_str= (len_spacers+4)*'-'+'\n'
			som_str	= f"{self.bereken_besparingen_gas():>{len_spacers}} m3"
			gb_str += lijn_str + som_str
		else:
			gb_str += 'Er zijn geen besparingen in gas/n'
		
		return gb_str
		
	def bereken_besparingen_gas(self):
		gb = 0
		
		for i in self.inv_lijst:
			gb += i.bereken_gas_besparing(self.huis)
			
		return gb	
		 
	def __repr__ (self):
		return self.print_besparingen_gas_tekst()

class MeerverbruikStroom(InvesteringsBerekening):
	def __init__(self,app_lijst, inv_lijst, huis):
		InvesteringsBerekening.__init__(self, inv_lijst, huis)
		self.app_lijst = app_lijst
			
	def print_meerverbruik_stroom_html(self):
		
		html = f"<p><b>Meerverbruik Stroom</b></p>"
			
		if len(self.app_lijst)>0:
			lab_list= []
			val_list = []
			for apparaat in self.app_lijst:
				if apparaat.bereken_stroom_verbruik(self.huis) >0:
					lab_list.append(apparaat.naam)
					val_list.append(apparaat.bereken_stroom_verbruik(self.huis))
			if len(lab_list)>0:	
				html+= Formula.print_html_formula(lab_list,val_list,'+')
		else:
			html += '<p>Er is geen meerverbruik stroom</p>'
		
		return html	
		
	

	def print_meerverbruik_stroom_tekst(self):
		mv_str = Color.BOLD + 'Meerverbruik stroom \n' + Color.END
		
		spacer_str1 = 15
		spacer_str2 = 15
		spacer_str3 = 6
		
		if len(self.app_lijst)>0:
			for i in self.app_lijst:
				if i.bereken_stroom_verbruik(self.huis) >0:
					mv_str += f"{i.soort:<{spacer_str1}}{i.naam:<{spacer_str2}}{(i.bereken_stroom_verbruik(self.huis)):>{spacer_str3}} kwh\n"
		
			len_spacers = spacer_str1 + spacer_str2 +spacer_str3 
			lijn_str= (len_spacers+4)*'-'+'\n'
			som_str	= f"{self.bereken_meerverbruik_stroom():>{len_spacers}} kwh"
			mv_str += lijn_str + som_str
		else:
			mv_str += 'Er is geen meerverbruik stroom/n'
			
		return mv_str
	
		
	def bereken_meerverbruik_stroom(self):
		mv = 0
		
		for i in self.app_lijst:
			mv += i.bereken_stroom_verbruik(self.huis)
			
		return mv
		
	def __repr__(self):
		return self.print_meerverbruik_stroom_tekst()
	
class StroomBesparingen(InvesteringsBerekening):
	def __init__(self,app_lijst, inv_lijst, huis):
		InvesteringsBerekening.__init__(self, inv_lijst, huis)
		self.app_lijst = app_lijst
		
	def print_besparingen_stroom_zp_html(self):
		
		lab_list = [ 'Direct verbruik',
						'Saldering',
						'Niet saldeerbaar'
						]
		var_list = [self.bereken_direct_verbruik_stroom_zonnepanelen(),
					self.bereken_salderingsdeel_stroom_zonnepanelen(),
					self.bereken_teruglevering_stroom_zonnepanelen()
					]
		
		
		if self.bereken_capaciteit_zonnepanelen()== 0:
			html = ' U heeft (nog) geen zonnepanelen </p>'
		
		else:
			html = f"<p><b>Zonnepanelen besparingen</b></p>"
			html+= Formula.print_html_formula(lab_list,var_list,'+')
	
		return html
	
	def print_besparingen_stroom_zp_tekst(self):
		if self.bereken_capaciteit_zonnepanelen()== 0:
			return 'U heeft (nog) geen zonnepanelen'
		else:
			str1 = 'Direct verbruik'
			str2 = 'Saldering'
			str3 = 'Niet saldeerbaar'
			str4 = 'Capaciteit zonnepanelen'
			spacer = max(len(str1),len(str2),len(str3), len(str4))
			lijn_str= (spacer+10)*'-'+'\n'
			
			lijn1 = f"{Color.BOLD}Stroom van zonnepanelen\n{Color.END}"
			lijn2 = f"{str1:<{spacer}}{self.bereken_direct_verbruik_stroom_zonnepanelen():>6} kwh\n"
			lijn3 = f"{str2:<{spacer}}{self.bereken_salderingsdeel_stroom_zonnepanelen():>6} kwh\n"
			lijn4 = f"{str3:<{spacer}}{self.bereken_teruglevering_stroom_zonnepanelen():>6} kwh\n"
			lijn5 = f"{str4:<{spacer}}{self.bereken_capaciteit_zonnepanelen():>6} kwh\n"
			return lijn1 + lijn2 + lijn3 + lijn4 + lijn_str + lijn5
	
	def bereken_capaciteit_zonnepanelen(self):
		
		cap_zonnepanelen = 0
		
		for i in self.app_lijst:
			if i.soort == 'zonnepanelen':
				cap_zonnepanelen += i.bereken_huidige_cap()
				
		return cap_zonnepanelen
	
	def bereken_direct_verbruik_stroom_zonnepanelen(self):
		
		return round(self.huis.energie_verbruik.direct_verbruik_perc*self.bereken_capaciteit_zonnepanelen()) # KWH direct verbruikt		
	
	def bereken_salderingsdeel_stroom_zonnepanelen(self):

		return round(self.huis.saldering*(self.bereken_capaciteit_zonnepanelen()-self.bereken_direct_verbruik_stroom_zonnepanelen()))  # KWH saldering tegen kostprijs
	
	def bereken_teruglevering_stroom_zonnepanelen(self):
	
		return round((1-self.huis.saldering)*(self.bereken_capaciteit_zonnepanelen()-self.bereken_direct_verbruik_stroom_zonnepanelen()))

	def __repr__(self):
		return self.print_besparingen_stroom_zp_tekst()
	

