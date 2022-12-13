from generic import Color, Formula


#########################	

class EnergieKosten:
	def __init__(self, gas_jaar_var, stroom_jaar_var, gas_jaar_vast, stroom_jaar_vast):
		self.gas_jaar_var = gas_jaar_var
		self.gas_jaar_vast = gas_jaar_vast
		self.stroom_jaar_var = stroom_jaar_var
		self.stroom_jaar_vast = stroom_jaar_vast
		
		self.gas_kosten_jaar_label = "Gas Kosten Jaar "
		self.stroom_kosten_jaar_label = "Stroom Kosten Jaar "
		self.kosten_jaar_totaal_label = "Energie kosten Jaar"
		self.kosten_maand_totaal_label = "Energie kosten Maand"
				


	def return_labels_list(self):
				return 	[self.gas_kosten_jaar_label,
							self.stroom_kosten_jaar_label,
							self.kosten_jaar_totaal_label,
							self.kosten_maand_totaal_label ]
	
	def return_values_list(self):
				return 	[self.gas_kosten_jaar(),
							self.stroom_kosten_jaar(),
							self.totaal_kosten_jaar(),
							self.totaal_kosten_maand()	]

	def print_tekst(self):
		
		
		spacer = Formula.max_len_label(self.return_labels_list())
		header = f"{Color.BOLD}Kosten{Color.END}\n"
		tekst_str = header
		lijn_str = (spacer+6)*'-'+'\n'
		
		i = 0
		for label, value in zip(self.return_labels_list(), self.return_values_list()):
			i+= 1
			if i == 3:
				tekst_str += lijn_str
			tekst_str += f"{label:<{spacer}} {value:>6} €\n"
			
		return tekst_str
	
	def print_html(self):
		
		spacer = Formula.max_len_label(self.return_labels_list())
		header = f"<b>Kosten</b>\n"
		table_start = f"<table>"
		html_str = header + table_start
		streep = spacer*'-'
		lijn_str = f"<tr><td></td><td>{streep}</td></tr>"
		
		i = 0
		for label, value in zip(self.return_labels_list(), self.return_values_list()):
			i+= 1
			if i == 3:
				html_str += lijn_str
			html_str+= f"<tr><td>{label}</td><td align='right'>{value} €</td></tr>"
		
		html_str += f"</table>"
		
		return html_str
			
		
	def gas_kosten_jaar(self):
		return round(self.gas_jaar_var + self.gas_jaar_vast)
	
	def gas_kosten_jaar_html(self):
		html = f"<p><b>Totaal kosten gas</b>"
		lab_list = ['Gas jaar var €', 'Gas jaar vast €']
		val_list = [self.gas_jaar_var, round(self.gas_jaar_vast)]	
		html += Formula.print_html_formula(lab_list, val_list, '+')
		return html
		
	def stroom_kosten_jaar_html(self):
		html = f"<p><b>Totaal kosten stroom</b>"
		lab_list = ['Stroom jaar var €', 'Stroom jaar vast €']
		val_list = [self.stroom_jaar_var, round(self.stroom_jaar_vast)]	
		html += Formula.print_html_formula(lab_list, val_list, '+')
		return html
	
	def stroom_kosten_jaar(self):
		return round(self.stroom_jaar_var + self.stroom_jaar_vast)
	
	def totaal_kosten_jaar(self):
		return round(self.gas_kosten_jaar()+ self.stroom_kosten_jaar())
	
	def totaal_kosten_maand(self):
		return round(self.totaal_kosten_jaar()/12)
	
	def __repr__(self):
		return self.print_tekst()