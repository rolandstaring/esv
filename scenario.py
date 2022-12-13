from huis import EnergieVerbruik
from berekeningen import GasBesparingen, MeerverbruikStroom, StroomBesparingen
from kosten import EnergieKosten
from generic import Color, Formula

 
class VergelijkScenarios:
	def __init__(self, huidig, toekomst):
		self.huidig = huidig
		self.toekomst = toekomst
		self.roi_jaar = round(self.huidig.kosten.totaal_kosten_jaar() - self.toekomst.kosten.totaal_kosten_jaar())	
		
	
	def complement_apparaten(self):
		s_namen = set(self.huidig.maak_namen_lijst_van_investeringen())
		comp_namen = [x for x in self.toekomst.maak_namen_lijst_van_investeringen() if x not in s_namen]
		
		comp = []
		
		for c in comp_namen:
			for i in self.toekomst.inv_lijst:
				if i.naam == c:
					comp.append(i)
		
		return comp
	
	def bereken_investeringen_complement(self):
		p = 0
		for i in self.complement_apparaten():	
			p += i.prijs
		return p
	
	def print_complement_tekst(self):
		inv_str =''
		
		if len(self.complement_apparaten())>0:
			for i in self.complement_apparaten():
				spacer_tekst = 15
				spacer_prijs = 6
				tekst1 = f"{i.soort:<{spacer_tekst}}" 
				tekst2 = f"{i.naam:<{spacer_tekst}}"
				tekst3 = f"{str(i.prijs):>{spacer_prijs}} €"
				lijn = tekst1 + tekst2 + tekst3
				inv_str += lijn + '\n'
			
		
			len_spacers = (spacer_tekst)*2 + spacer_prijs
			lijn_str= (len_spacers+4)*'-'+'\n'
			som_str= f"{str(self.bereken_investeringen_complement()):>{len_spacers}} €\n"
			inv_str += lijn_str + som_str
		else:
			inv_str = 'Er zijn geen investeringen bijgekomen\n'
		return inv_str
		
	def print_complement_html(self):
		html = f"<p><b>Investeringen </b></p>"
		
		if len(self.complement_apparaten())>0:
			lab_list= []
			val_list = []
			for apparaat in self.complement_apparaten():
				lab_list.append(apparaat.naam)
				val_list.append(apparaat.prijs)	
			html+= Formula.print_html_formula(lab_list,val_list,'+')
		else:
			html += '<p>Er zijn geen investeringen</p>'
		
		return html	
			
	def print_html(self):
		html =''
		
		if len(self.complement_apparaten()) > 0:
			if self.roi_jaar <0:
				roi_jaar_abs = abs(self.roi_jaar)
				html = f"<p>Verlies {abs(self.roi_jaar):>6} € jaar</p>" 
			else:
				html =f"<p>Terugverdientijd {self.bereken_tvt()} jaar<br> Winst {self.roi_jaar} € jaar</p>"			
		else:	
			if self.roi_jaar <0:
				roi_jaar_abs = abs(self.roi_jaar)
				html = f"<p>Verlies {abs(self.roi_jaar)}</p>"
			elif self.roi_jaar ==0:
				html =f"<p>Geen verschil tussen scenarios</p>"
			else:
				html = f"<p>Winst {self.roi_jaar:>6} € jaar</p>"
				
		return html
	
	def print_tekst(self):
		verg_str =''
		if len(self.complement_apparaten()) > 0:
			if self.roi_jaar <0:
				roi_jaar_abs = abs(self.roi_jaar)
				verg_str = f"Verlies {abs(self.roi_jaar):>6} € jaar\n" 
			else:
				verg_str =f"Terugverdientijd {self.bereken_tvt()} jaar\n\nWinst {self.roi_jaar:>6} € jaar\n"			
		else:	
			if self.roi_jaar <0:
				roi_jaar_abs = abs(self.roi_jaar)
				verg_str = f"Verlies {abs(self.roi_jaar):>6}"
			elif self.roi_jaar ==0:
				verg_str =f"Geen verschil tussen scenarios"
			else:
				verg_str = f"Winst {self.roi_jaar:>6} € jaar"
				
		return verg_str
	
	def bereken_tvt(self):
		self.tvt = round(self.bereken_investeringen_complement()/ self.roi_jaar)
		return self.tvt
		
	def __repr__(self):
		return self.print_tekst()

class Scenario:
	def __init__ (self, naam, iso_lijst, app_lijst, huis):
		self.naam = naam
		self.iso_lijst = iso_lijst
		self.app_lijst = app_lijst
		self.inv_lijst = iso_lijst + app_lijst
		self.huis = huis
		self.kosten = EnergieKosten(0,0,0,0)
		self.verbruik_na = EnergieVerbruik('Verbruik na investeringen',0,0)
		self.gasbesparing = GasBesparingen(self.inv_lijst, huis)
		self.stroombesparing = StroomBesparingen(app_lijst, self.inv_lijst, huis)
		self.stroomtoename	= MeerverbruikStroom(app_lijst, self.inv_lijst, huis) 

	
	def bereken_investering(self):
		inv = 0
		
		for i in self.inv_lijst:
			inv += i.prijs
			
		return inv
		
	def maak_namen_lijst_van_investeringen(self):
		namen_lijst = []
		for i in self.inv_lijst:
			namen_lijst.append(i.naam)
		
		return namen_lijst
	
	def print_investeringen_html(self):
		html = f"<p><b>Investeringen </b></p>"
		
		if len(self.inv_lijst)>0:
			lab_list= []
			val_list = []
			for inv in self.inv_lijst:
				lab_list.append(inv.naam)
				val_list.append(inv.prijs)	
			html+= Formula.print_html_formula(lab_list,val_list,'+')
		else:
			html += '<p>Er zijn geen investeringen</p>'
		
		return html		
	
	def print_investeringen_tekst(self):
		inv_str = f"{Color.BOLD}Investeringen {Color.END}\n"
		
		if len(self.inv_lijst)>0:
	
			for i in self.inv_lijst:	
				spacer_tekst = 15
				spacer_prijs = 6
				tekst1 = f"{i.soort:<{spacer_tekst}}" 
				tekst2 = f"{i.naam:<{spacer_tekst}}"
				tekst3 = f"{str(i.prijs):>{spacer_prijs}} €"
				lijn = tekst1 + tekst2 + tekst3
				inv_str += lijn + '\n'
			
			len_spacers = (spacer_tekst)*2 + spacer_prijs
			lijn_str= (len_spacers+4)*'-'+'\n'
			som_str= f"{str(self.bereken_investering()):>{len_spacers}} €\n"
		
			inv_str += lijn_str + som_str
		else:
			inv_str = 'Er zijn geen investeringen'
		
		return inv_str
	
	def __repr__(self):
		blok1 = print(self.huis) 
		blok2 = print(self.verbruik_na)
		blok3 = print(self.print_investeringen_tekst())
		blok4 = print(self.gasbesparing)
		blok5 = print(self.stroomtoename)
		blok6 = print(self.stroombesparing)
		blok7 = print(self.kosten)
		return blok7
	
class ScenarioMetPlafond(Scenario):
	soort = 'Scenario met plafond'
	def __init__ (self, naam, iso_lijst,app_lijst, huis, plafond):
		Scenario.__init__(self, naam, iso_lijst, app_lijst, huis)
		self.plafond = plafond	
		
		self.bereken_kosten_gas_var()
		self.bereken_kosten_gas_vast()
		self.bereken_kosten_stroom_var()
		self.bereken_kosten_stroom_vast()
	
	def print_bereken_kosten_stroom_vast_html(self):
		html = f"<p><b>Kosten stroom vast</b>"
		lab_list = ['Gas prijs vast per dag €', 'Dagen in een jaar']
		val_list = [self.huis.energie_prijzen.stroom_prijs_vast_dag, 365]	
		html += Formula.print_html_formula(lab_list, val_list, '*')	
		return html

		
	def print_bereken_kosten_gas_vast_html(self):
		html = f"<p><b>Kosten gas vast</b>"
		lab_list = ['Gas prijs vast per dag €', 'Dagen in een jaar']
		val_list = [self.huis.energie_prijzen.gas_prijs_vast_dag, 365]	
		html += Formula.print_html_formula(lab_list, val_list, '*')	
		return html
	
	
	def print_bereken_kosten_gas_var_html(self):
		html = ''
		
		if self.huis.energie_verbruik.gas_verbruik_jaar >= self.gasbesparing.bereken_besparingen_gas():
			html += f"<p><b>Gas na besparingen</b></p>"
			lab_list = ['Gas verbruik jaar m3','Gas besparingen jaar m3']
			val_list = [self.huis.energie_verbruik.gas_verbruik_jaar,self.gasbesparing.bereken_besparingen_gas()]
			html+= Formula.print_html_formula(lab_list, val_list,'-')
			gas_verbruik_na_besparing = round(self.huis.energie_verbruik.gas_verbruik_jaar -self.gasbesparing.bereken_besparingen_gas())
		else:
			gas_verbruik_na_besparing = 0
			html+= f"<p> Gefeliciteerd je hebt nu 0 op de gas meter </p> <p>Je gasbesparing is {str(self.gasbesparing.bereken_besparingen_gas())}</p>"
		
		lab_list = ['Gas verbruik na besparing m3', 'Gas prijs var €']
		val_list = [gas_verbruik_na_besparing, self.huis.energie_prijzen.gas_prijs_var]
		html += Formula.print_html_formula(lab_list, val_list, '*')
		
		boven_prijsplafond_kosten_gas = round((gas_verbruik_na_besparing - self.plafond.gas_plafond)* self.huis.energie_prijzen.gas_prijs_var)
		onder_prijsplafond_kosten_gas = round(gas_verbruik_na_besparing * self.plafond.energie_prijzen.gas_prijs_var)
		html += f"<p><b>Boven prijsplafond gas</b></p>"
		lab_list = ['Netto verbruik gas m3', 'Gas plafond m3']
		val_list = [gas_verbruik_na_besparing, self.plafond.gas_plafond]
		html += Formula.print_html_formula(lab_list, val_list, '-')
		html += f"<p><b>Kosten gas boven plafond</b></p>"
		lab_list = ['Boven prijsplafond m3', 'Gas prijs var €']
		val_list = [gas_verbruik_na_besparing - self.plafond.gas_plafond, self.plafond.gas_plafond]
		html += Formula.print_html_formula(lab_list, val_list, '*')
		
		
		
	
		if	gas_verbruik_na_besparing > self.plafond.gas_plafond:
			self.kosten.gas_jaar_var = self.plafond.gas_kosten_tot_plafond() + boven_prijsplafond_kosten_gas
			html += f"<p><b>Gaskosten boven plafond </b></p>"
			lab_list = ['Tot gasplafond kosten €', 'Boven gasplafond kosten €']
			val_list = [self.plafond.gas_kosten_tot_plafond(), boven_prijsplafond_kosten_gas]
			html += Formula.print_html_formula(lab_list, val_list, '+')
		else:
			self.kosten.gas_jaar_var = onder_prijsplafond_kosten_gas
			html += f"<p><b>Gaskosten onder plafond </b></p>"
			lab_list = ['Netto verbruik m3', 'Gas prijs var €']
			val_list = [gas_verbruik_na_besparing, self.plafond.energie_prijzen.gas_prijs_var]
			html += Formula.print_html_formula(lab_list, val_list, '*')
		
		return html
	
	def bereken_kosten_gas_var(self):
		
		# het besparen van gas kan nooit groter worden dan 0
		if self.huis.energie_verbruik.gas_verbruik_jaar >= self.gasbesparing.bereken_besparingen_gas():
			gas_verbruik_na_besparing = round(self.huis.energie_verbruik.gas_verbruik_jaar -self.gasbesparing.bereken_besparingen_gas())
		else:
			gas_verbruik_na_besparing = 0
		
		
		self.verbruik_na.gas_verbruik_jaar = gas_verbruik_na_besparing
		
	
		
		boven_prijsplafond_kosten_gas = round((gas_verbruik_na_besparing - self.plafond.gas_plafond)* self.huis.energie_prijzen.gas_prijs_var)
		onder_prijsplafond_kosten_gas = round(gas_verbruik_na_besparing * self.plafond.energie_prijzen.gas_prijs_var)
		
		if	gas_verbruik_na_besparing > self.plafond.gas_plafond:
			self.kosten.gas_jaar_var = self.plafond.gas_kosten_tot_plafond() + boven_prijsplafond_kosten_gas
			
		else:
			self.kosten.gas_jaar_var = onder_prijsplafond_kosten_gas
		
		return self.kosten.gas_jaar_var
			
	
	def bereken_kosten_gas_vast(self):
		self.kosten.gas_jaar_vast = self.huis.energie_prijzen.gas_prijs_vast_dag * 365 
		return round(self.kosten.gas_jaar_vast)
	
	
	def print_bereken_kosten_stroom_var_html(self):
		html=''
		stroom_na_investeringen = round((self.huis.energie_verbruik.stroom_verbruik_jaar + self.stroomtoename.bereken_meerverbruik_stroom()) - 
										(self.stroombesparing.bereken_direct_verbruik_stroom_zonnepanelen() + self.stroombesparing.bereken_salderingsdeel_stroom_zonnepanelen()) )
		
		
		html += f"<p><b>Extra verbruik stroom</b>"
		lab_list = ['Jaarverbruik stroom', ' Meerverbruik stroom ']
		val_list = [self.huis.energie_verbruik.stroom_verbruik_jaar,  self.stroomtoename.bereken_meerverbruik_stroom() ]	
		html += Formula.print_html_formula(lab_list, val_list, '+')	
		
		html += f"<p><b>Directe besparingen stroom</b>"
		lab_list = ['Direct verbruik zonnepanelen', 'Salderingsdeel zonnepanelen']
		val_list = [self.stroombesparing.bereken_direct_verbruik_stroom_zonnepanelen(), self.stroombesparing.bereken_salderingsdeel_stroom_zonnepanelen()]	
		html += Formula.print_html_formula(lab_list, val_list, '+')	
		
		html += f"<p><b>Verbruik na besparing stroom</b>"
		lab_list = ['Verbruik stroom totaal', 'Besparing stroom totaal']
		val_list = [self.huis.energie_verbruik.stroom_verbruik_jaar + self.stroomtoename.bereken_meerverbruik_stroom(), self.stroombesparing.bereken_direct_verbruik_stroom_zonnepanelen() + self.stroombesparing.bereken_salderingsdeel_stroom_zonnepanelen()]	
		html += Formula.print_html_formula(lab_list, val_list, '-')	
		
		prijsplafond_kosten_stroom = self.plafond.stroom_kosten_tot_plafond()
		boven_prijsplafond_kosten_stroom = round((stroom_na_investeringen - self.plafond.stroom_plafond)*self.huis.energie_prijzen.stroom_prijs_var)
		onder_prijsplafond_kosten_stroom = round(self.plafond.stroom_plafond* self.plafond.energie_prijzen.stroom_prijs_var)
		teruglever_inkomsten_stroom = round(self.stroombesparing.bereken_teruglevering_stroom_zonnepanelen()*self.huis.energie_prijzen.stroom_lever_prijs_var)
		
		html += f"<p><b>Boven prijsplafond kwh stroom</b></p>"
		lab_list = ['Netto stroom kwh', ' Prijsplafond stroom kwh']
		val_list = [stroom_na_investeringen,  self.plafond.stroom_plafond ]	
		html += Formula.print_html_formula(lab_list, val_list, '-')	
		
		html += f"<p><b>Boven prijsplafond kosten stroom</b></p>"
		lab_list = ['Deel boven prijsplafond kwh', 'Stroom prijs var']
		val_list = [stroom_na_investeringen - self.plafond.stroom_plafond, self.huis.energie_prijzen.stroom_prijs_var]	
		html += Formula.print_html_formula(lab_list, val_list, '*')	
		
		html += f"<p><b>Onder prijsplafond kosten stroom</b></p>"
		lab_list = ['Deel boven prijsplafond', 'Stroom prijs var']
		val_list = [self.plafond.stroom_plafond, self.plafond.energie_prijzen.stroom_prijs_var]	
		html += Formula.print_html_formula(lab_list, val_list, '*')
		
		html += f"<p><b>Teruglever inkomsten stroom</b></p>"
		lab_list = ['Deel niet saldeerbaar', 'Stroom prijs teruglever var']
		val_list = [self.stroombesparing.bereken_teruglevering_stroom_zonnepanelen(), self.huis.energie_prijzen.stroom_lever_prijs_var]	
		html += Formula.print_html_formula(lab_list, val_list, '*')
		
		
		if	stroom_na_investeringen > self.plafond.stroom_plafond: # stroomverbruik is boven het prijsplafond
			html += f"<p><b>Kosten stroom voor teruglevering</b>"
			lab_list = ['Stroomkosten tot prijsplafond €',' Stroomkosten boven prijsplafond €']
			val_list = [prijsplafond_kosten_stroom,  boven_prijsplafond_kosten_stroom ]	
			html += Formula.print_html_formula(lab_list, val_list, '+')	
			
			html += f"<p><b>Kosten stroom na teruglevering</b>"
			lab_list = ['Netto stroomkosten met plafond €', 'Inkomsten uit teruglevering €']
			val_list = [prijsplafond_kosten_stroom + boven_prijsplafond_kosten_stroom, teruglever_inkomsten_stroom]	
			html += Formula.print_html_formula(lab_list, val_list, '-')
			
		else:										# stroomverbruik is onder het prijsplafond
			if stroom_na_investeringen < 0:					# stroomverbruik is negatief 
				html += f"<p><b>Stroomverbruik is negatief </b>"
				lab_list = ['Stroomkosten tot prijsplafond kwh',' Stroom prijs voor terugleveren €']
				val_list = [stroom_na_investeringen,  self.huis.energie_prijzen.stroom_lever_prijs_var ]	
				html += Formula.print_html_formula(lab_list, val_list, '*')	
				lab_list = ['Netto stroomkosten met prijsplafond', 'Inkomsten uit teruglevering']
				val_list = [stroom_na_investeringen*self.huis.energie_prijzen.stroom_lever_prijs_var, teruglever_inkomsten_stroom]	
				html += Formula.print_html_formula(lab_list, val_list, '-')
			
			else:	
				html += f"<p><b>Stroom onder prijsplafond </b>"		
				lab_list = ['Netto stroomkosten onder prijsplafond', 'Inkomsten uit teruglevering']
				val_list = [onder_prijsplafond_kosten_stroom, teruglever_inkomsten_stroom]	
				html += Formula.print_html_formula(lab_list, val_list, '-')
		
		return html
				
	def bereken_kosten_stroom_var(self):
	
		stroom_na_investeringen = round((self.huis.energie_verbruik.stroom_verbruik_jaar + self.stroomtoename.bereken_meerverbruik_stroom()) - 
										(self.stroombesparing.bereken_direct_verbruik_stroom_zonnepanelen() + self.stroombesparing.bereken_salderingsdeel_stroom_zonnepanelen()) )
		
		self.verbruik_na.stroom_verbruik_jaar = stroom_na_investeringen
		
		
		prijsplafond_kosten_stroom = self.plafond.stroom_kosten_tot_plafond()
		boven_prijsplafond_kosten_stroom = round((stroom_na_investeringen - self.plafond.stroom_plafond)*self.huis.energie_prijzen.stroom_prijs_var)
		onder_prijsplafond_kosten_stroom = round(stroom_na_investeringen* self.plafond.energie_prijzen.stroom_prijs_var)
		
		teruglever_inkomsten_stroom = round(self.stroombesparing.bereken_teruglevering_stroom_zonnepanelen()*self.huis.energie_prijzen.stroom_lever_prijs_var)
		
				
		if	stroom_na_investeringen > self.plafond.stroom_plafond: # stroomverbruik is boven het prijsplafond
			self.kosten.stroom_jaar_var = round(prijsplafond_kosten_stroom + boven_prijsplafond_kosten_stroom - teruglever_inkomsten_stroom)
			
		else:										# stroomverbruik is onder het prijsplafond
			if stroom_na_investeringen < 0:					# stroomverbruik is negatief 
				self.kosten.stroom_jaar_var = round(stroom_na_investeringen*self.huis.energie_prijzen.stroom_lever_prijs_var - teruglever_inkomsten_stroom) # je krijgt geld terug omdat je meer levert dan je zelf gebruikt of weg kan strepen met saldering
			else:									
				self.kosten.stroom_jaar_var = round(onder_prijsplafond_kosten_stroom - teruglever_inkomsten_stroom)
				
		return self.kosten.stroom_jaar_var 
	
	def bereken_kosten_stroom_vast(self):
		self.kosten.stroom_jaar_vast = self.huis.energie_prijzen.stroom_prijs_vast_dag * 365 
		return round(self.kosten.stroom_jaar_vast)
	
	def __repr__(self):
		return f"{Color.BOLD}{self.soort}{Color.END}\n{Scenario.__repr__(self)}\n\n{self.plafond} "
	
class ScenarioZonderPlafond(Scenario):	
	def __init__ (self, naam, inv_lijst, huis):
		Scenario_.__init__(self, naam, inv_lijst, huis)
	soort = 'Scenario zonder plafond'
	def __init__ (self, naam, iso_lijst,app_lijst, huis):
		Scenario.__init__(self, naam, iso_lijst, app_lijst, huis)
		self.bereken_kosten_gas_var()
		self.bereken_kosten_gas_vast()
		self.bereken_kosten_stroom_var()
		self.bereken_kosten_stroom_vast()

	
	def print_bereken_kosten_gas_var_html(self):
		html = ''
		
		if self.huis.energie_verbruik.gas_verbruik_jaar >= self.gasbesparing.bereken_besparingen_gas():
			html += f"<p><b>Netto verbruik gas</b></p>"
			lab_list = ['Gas verbruik jaar m3','Gas besparingen jaar m3']
			val_list = [self.huis.energie_verbruik.gas_verbruik_jaar,self.gasbesparing.bereken_besparingen_gas()]
			html+= Formula.print_html_formula(lab_list, val_list,'-')
			gas_verbruik_na_besparing = round(self.huis.energie_verbruik.gas_verbruik_jaar -self.gasbesparing.bereken_besparingen_gas())
		else:
			
			gas_verbruik_na_besparing = 0
			html+= f"<p> Gefeliciteerd je hebt nu 0 op de gas meter </p> <p>Je gasbesparing is {str(self.gasbesparing.bereken_besparingen_gas())}</p>"
		
		html += f"<p><b>Kosten gas variabel </b></p>"
		lab_list = ['Gas verbruik na besparing m3', 'Gas prijs var €']
		val_list = [gas_verbruik_na_besparing, self.huis.energie_prijzen.gas_prijs_var]
		html += Formula.print_html_formula(lab_list, val_list, '*')
		
		return html
		
	def bereken_kosten_gas_var(self):
		
		if self.huis.energie_verbruik.gas_verbruik_jaar >= self.gasbesparing.bereken_besparingen_gas():
			gas_verbruik_na_besparing = round(self.huis.energie_verbruik.gas_verbruik_jaar -self.gasbesparing.bereken_besparingen_gas())
		else:
			gas_verbruik_na_besparing = 0
		
		self.verbruik_na.gas_verbruik_jaar = gas_verbruik_na_besparing
		
		self.kosten.gas_jaar_var = round(gas_verbruik_na_besparing * self.huis.energie_prijzen.gas_prijs_var)
		
		return self.kosten.gas_jaar_var
	
	
	def bereken_kosten_gas_vast(self):
		self.kosten.gas_jaar_vast = self.huis.energie_prijzen.gas_prijs_vast_dag * 365 
		return round(self.kosten.gas_jaar_vast)
	
	def print_bereken_kosten_stroom_vast_html(self):
		html = f"<p><b>Kosten stroom vast</b></p>"
		lab_list = ['Stroom prijs vast per dag €', 'Dagen in een jaar']
		val_list = [self.huis.energie_prijzen.stroom_prijs_vast_dag, 365]	
		html += Formula.print_html_formula(lab_list, val_list, '*')	
		return html
	
	def print_bereken_kosten_gas_vast_html(self):
		html = f"<p><b>Kosten gas vast</b></p>"
		lab_list = ['Gas prijs vast per dag €', 'Dagen in een jaar']
		val_list = [self.huis.energie_prijzen.gas_prijs_vast_dag, 365]	
		html += Formula.print_html_formula(lab_list, val_list, '*')	
		return html
	
	
	def print_bereken_kosten_stroom_var_html(self):
		html = ''
		stroom_na_investeringen = round((self.huis.energie_verbruik.stroom_verbruik_jaar + self.stroomtoename.bereken_meerverbruik_stroom() )- 
										(self.stroombesparing.bereken_direct_verbruik_stroom_zonnepanelen() + self.stroombesparing.bereken_salderingsdeel_stroom_zonnepanelen()) )
		
		html = f"<p><b>Extra verbruik stroom</b>"
		lab_list = ['Jaarverbruik stroom', ' Meerverbruik stroom ']
		val_list = [self.huis.energie_verbruik.stroom_verbruik_jaar,  self.stroomtoename.bereken_meerverbruik_stroom() ]	
		html += Formula.print_html_formula(lab_list, val_list, '+')	
		html = f"<p><b>Directe besparing stroom</b>"
		lab_list = ['Direct verbruik zonnepanelen', 'Salderingsdeel zonnepanelen']
		val_list = [self.stroombesparing.bereken_direct_verbruik_stroom_zonnepanelen(), self.stroombesparing.bereken_salderingsdeel_stroom_zonnepanelen()]	
		html += Formula.print_html_formula(lab_list, val_list, '+')	
		html = f"<p><b>Verbruik na besparing stroom</b>"
		lab_list = ['Verbruik stroom totaal', 'Besparing stroom totaal']
		val_list = [self.huis.energie_verbruik.stroom_verbruik_jaar + self.stroomtoename.bereken_meerverbruik_stroom(), self.stroombesparing.bereken_direct_verbruik_stroom_zonnepanelen() + self.stroombesparing.bereken_salderingsdeel_stroom_zonnepanelen()]	
		html += Formula.print_html_formula(lab_list, val_list, '-')	
		
		
		kosten_stroom_var = round(stroom_na_investeringen * self.huis.energie_prijzen.stroom_prijs_var)
		teruglever_inkomsten_stroom_var = round(self.stroombesparing.bereken_teruglevering_stroom_zonnepanelen()*self.huis.energie_prijzen.stroom_lever_prijs_var)
		
		if stroom_na_investeringen < 0 : # je krijgt geld terug omdat je meer levert dan je zelf gebruikt of weg kan strepen met saldering
			html += f"<p><b>Geen kosten maar inkomsten voor stroom</b></p>"
			html += f"<p><b>Stroomkosten na direct verbruik</b>"
			lab_list = ['Netto verbruik stroom', ' Teruglever prijs var ']
			val_list = [stroom_na_investeringen,  self.huis.energie_prijzen.stroom_prijs_var ]	
			html += Formula.print_html_formula(lab_list, val_list, '*')
			
			html += f"<p><b>Inkomsten teruglevering</b>"
			lab_list = ['Teruglever deel zonnepanelen', ' Teruglever prijs var ']
			val_list = [self.stroombesparing.bereken_teruglevering_stroom_zonnepanelen(),  self.huis.energie_prijzen.stroom_lever_prijs_var]	
			html += Formula.print_html_formula(lab_list, val_list, '*')
			
			html += f"<p><b>Netto verbruik stroom</b>"
			lab_list = ['Inkomsten stroom', ' Teruglever inkomsten']
			val_list = [stroom_na_investeringen*self.huis.energie_prijzen.stroom_lever_prijs_var,  teruglever_inkomsten_stroom_var]	
			html += Formula.print_html_formula(lab_list, val_list, '-')
			
		else:
			html += f"<p><b>Stroomkosten na direct verbruik</b>"
			lab_list = ['Netto verbruik stroom', ' Prijs stroom var ']
			val_list = [stroom_na_investeringen,  self.huis.energie_prijzen.stroom_prijs_var ]	
			html += Formula.print_html_formula(lab_list, val_list, '*')
			
			html += f"<p><b>Inkomsten teruglevering</b>"
			lab_list = ['Teruglever deel zonnepanelen', ' Teruglever prijs var ']
			val_list = [self.stroombesparing.bereken_teruglevering_stroom_zonnepanelen(),  self.huis.energie_prijzen.stroom_lever_prijs_var]	
			html += Formula.print_html_formula(lab_list, val_list, '*')
			
			html += f"<p><b>Netto verbruik stroom</b>"
			lab_list = ['Kosten stroom var', ' Teruglever inkomsten ']
			val_list = [kosten_stroom_var,  teruglever_inkomsten_stroom_var ]	
			html += Formula.print_html_formula(lab_list, val_list, '-')
		
		return html
		
		
	def bereken_kosten_stroom_var(self):		
		stroom_na_investeringen = round((self.huis.energie_verbruik.stroom_verbruik_jaar + self.stroomtoename.bereken_meerverbruik_stroom() )- 
										(self.stroombesparing.bereken_direct_verbruik_stroom_zonnepanelen() + self.stroombesparing.bereken_salderingsdeel_stroom_zonnepanelen()) )
		
		
		self.verbruik_na.stroom_verbruik_jaar = stroom_na_investeringen
		
		kosten_stroom_var = round(stroom_na_investeringen * self.huis.energie_prijzen.stroom_prijs_var)
		teruglever_inkomsten_stroom_var = round(self.stroombesparing.bereken_teruglevering_stroom_zonnepanelen()*self.huis.energie_prijzen.stroom_lever_prijs_var)
		
		if stroom_na_investeringen < 0 : # je krijgt geld terug omdat je meer levert dan je zelf gebruikt of weg kan strepen met saldering
			self.kosten.stroom_jaar_var = round(stroom_na_investeringen*self.huis.energie_prijzen.stroom_lever_prijs_var - teruglever_inkomsten_stroom_var) # je krijgt geld terug omdat je meer levert dan je zelf gebruikt of weg kan strepen met saldering
			
		else:
			self.kosten.stroom_jaar_var = round(kosten_stroom_var - teruglever_inkomsten_stroom_var)
		
		return self.kosten.stroom_jaar_var
		
	
	def bereken_kosten_stroom_vast(self):
		self.kosten.stroom_jaar_vast = self.huis.energie_prijzen.stroom_prijs_vast_dag * 365 
		return round(self.kosten.stroom_jaar_vast)	
		
	def __repr__(self):
		return f"{Color.BOLD}{self.soort}{Color.END}\n{Scenario.__repr__(self)}"	
		
		
		