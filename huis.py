from generic import Color, Formula, Global


class EnergieVerbruik:
	def __init__(self, beschrijving, gas_verbruik_jaar, stroom_verbruik_jaar):
		self.beschrijving = beschrijving
		self.gas_verbruik_jaar = gas_verbruik_jaar
		self.stroom_verbruik_jaar = stroom_verbruik_jaar
		self.direct_verbruik_perc = Global.DIRECT_VERBRUIK_PERC
		
		self.gas_label = 'Gas'
		self.stroom_label = 'Stroom'
							
	def return_labels_list(self):
		return  [self.gas_label, 
				self.stroom_label
				]
	
	def return_values_list(self):
		return [self.gas_verbruik_jaar,
				self.stroom_verbruik_jaar]
			
	def print_tekst(self):
		
		spacer = Formula.max_len_label(self.return_labels_list())
		
		header = f"{Color.BOLD}{self.beschrijving}{Color.END}\n"
		tekst_str = header
		
		for label, value in zip(self.return_labels_list(), self.return_values_list()):
			tekst_str += f"{label:<{spacer}} {value:>6} \n"
			
		return tekst_str
	
	def print_html(self):

		header = f"<p><b>{self.beschrijving}</b>\n"
		table_start = f"<table>"
		html_str = header + table_start
		
		for label, value in zip(self.return_labels_list(), self.return_values_list()):
			html_str+= f"<tr><td>{label}</td><td align='right'>{value}</td></tr>"
		
		html_str += f"</table></p>"
		
		return html_str
		
	def __repr__(self):
	
		return self.print_tekst()
	
class EnergiePrijs:
	def __init__(self, gas_prijs_var, stroom_prijs_var, stroom_lever_prijs_var =0.2, stroom_prijs_vast= 0.2,gas_prijs_vast=0.2):
		self.gas_prijs_var= gas_prijs_var
		self.stroom_prijs_var = stroom_prijs_var
		self.stroom_lever_prijs_var = stroom_lever_prijs_var
		self.gas_prijs_vast_dag= gas_prijs_vast
		self.stroom_prijs_vast_dag = stroom_prijs_vast
		
		self.gas_prijs_afn_label = 'Gas afname var'
		self.stroom_prijs_afn_label = 'Stroom afname var'
		self.stroom_prijs_lev_label = 'Stroom levering var'
		self.gas_prijs_vast_label = 'Gas prijs vast'
		self.stroom_prijs_vast_label = 'Stroom prijs vast'
				
		
	def return_values_list(self):
		return [self.gas_prijs_var,
				self.stroom_prijs_var,
				self.stroom_lever_prijs_var,
				self.gas_prijs_vast_dag,
				self.stroom_prijs_vast_dag
				]
				
	def return_labels_list(self):
		return [self.gas_prijs_afn_label,
				self.stroom_prijs_afn_label,
				self.stroom_prijs_lev_label,
				self.gas_prijs_vast_label,
				self.stroom_prijs_vast_label
				]
			
	def print_tekst(self):
		
		spacer = Formula.max_len_label(self.return_labels_list())
		
		header = f"{Color.BOLD}Prijzen{Color.END}\n"
		tekst_str = header
		
		for label, value in zip(self.return_labels_list(), self.return_values_list()):
			tekst_str += f"{label:<{spacer}} {value:>6} €\n"
			
		return tekst_str
		
	def print_html(self):
		
		header = f"<p><b>Prijzen</b>\n"
		table_start = f"<table>"
		html_str = header + table_start
		
		for label, value in zip(self.return_labels_list(), self.return_values_list()):
			html_str+= f"<tr><td>{label}</td><td align='right'>{value} €</td></tr>"
		
		html_str += f"</table></p>"
		
		return html_str
		
	def __repr__(self):
	
		return self.print_tekst()
		
class Plafond():
	def __init__ (self, energie_prijzen, gas_plafond, stroom_plafond):
		self.energie_prijzen = energie_prijzen
		self.gas_plafond = gas_plafond
		self.stroom_plafond = stroom_plafond
		
		self.gas_plafond_label = 'Gas Plafond'
		self.stroom_plafond_label = 'Stroom Plafond'
	
	def gas_kosten_tot_plafond(self):
		return round(self.energie_prijzen.gas_prijs_var * self.gas_plafond)
		
	def stroom_kosten_tot_plafond(self):
		return round(self.energie_prijzen.stroom_prijs_var *self.stroom_plafond)			
	
	def return_labels_list(self):
		return  [self.energie_prijzen.gas_prijs_afn_label,
				 self.energie_prijzen.stroom_prijs_afn_label,
				 self.gas_plafond_label,
				 self.stroom_plafond_label
							]
	
	def return_values_list(self):
		return [self.energie_prijzen.gas_prijs_var,
				self.energie_prijzen.stroom_prijs_var,
				self.gas_plafond,
				self.stroom_plafond
							]
	def print_tekst(self):
	
		spacer = Formula.max_len_label(self.return_labels_list())
		
		header = f"{Color.BOLD}Plafond{Color.END}\n"
		tekst_str = header
		
		for label, value in zip(self.return_labels_list(), self.return_values_list()):
			tekst_str += f"{label:<{spacer}} {value:>6} \n"
			
		return tekst_str
		
	def print_html(self):
		self.vars_list = [self.energie_prijzen.gas_prijs_var,
							self.energie_prijzen.stroom_prijs_var,
							self.gas_plafond,
							self.stroom_plafond
							]
		
		header = f"<p><b>Plafond</b>\n"
		table_start = f"<table>"
		html_str = header + table_start
		
		for label, value in zip(self.return_labels_list(), self.return_values_list()):
			html_str+= f"<tr><td>{label}</td><td align='right'>{value}</td></tr>"
		
		html_str += f"</table></p>"
		
		return html_str
	
	def __repr__(self):
		return self.print_tekst()
		
class Huishouden:
	def __init__(self, naam,  soort_woning, energie_verbruik, energie_prijzen, saldering = 1 ):
		self.naam = naam
		self.soort = soort_woning
		self.energie_verbruik = energie_verbruik
		self.energie_prijzen = energie_prijzen
		self.saldering = saldering
		self.Kwh_voor_1m3_Gas = Global.KWH_1M3_GAS
	
	def reassign_values_from_list(self, values_list):
		self.energie_verbruik.gas_verbruik_jaar = int(values_list[0].text())	
		self.energie_verbruik.stroom_verbruik_jaar = int(values_list[1].text())
		self.energie_prijzen.gas_prijs_var  = float(values_list[2].text())	
		self.energie_prijzen.stroom_prijs_var  = float(values_list[3].text())		
		self.energie_prijzen.stroom_lever_prijs_var  = float(values_list[4].text())	
		self.energie_prijzen.gas_prijs_vast_dag  = float(values_list[5].text())	
		self.energie_prijzen.stroom_prijs_vast_dag  = float(values_list[6].text())
		self.saldering  = float(values_list[7].text())
	
	def return_values_list(self):
		id_list = [self.naam, self.soort]
		values_list = id_list + self.energie_verbruik.return_values_list() + self.energie_prijzen.return_values_list()
		values_list.append(self.saldering)
		return values_list
		
	def return_labels_list(self):
		id_list = ['Naam','Soort']
		labels_list = id_list + self.energie_verbruik.return_labels_list() + self.energie_prijzen.return_labels_list()
		labels_list.append('Saldering')
		return labels_list
	
	def print_tekst(self):
	
		tekst_str = f"{Color.BOLD}Huishouden{Color.END}\n"
		
		return tekst_str
		
	def print_html(self):
		html_str = f"\n<p>{self.naam}</p>"
		html_str += f"\n<p>{self.soort}</p>"
	
		return html_str
				
	def make_dict(self):
		keys_list = ['naam',  'soort', 'gas', 'stroom', 'prijs_gas','prijs_stroom', 'prijs_stroom_lev', 'prijs_gas_vast_dag','prijs_stroom_vast_dag', 'saldering']
		return dict(zip(keys_list, self.return_values_list()))
		
	def __repr__(self):
		return self.print_tekst()
