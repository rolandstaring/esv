from datetime import datetime

class Report:
	def __init__(self, scenario):
		self.scenario = scenario
		self.input_berekeningen_lijst =[
				self.scenario.huis.print_html(),
				self.scenario.huis.energie_verbruik.print_html(),
				self.scenario.huis.energie_prijzen.print_html(),
				self.scenario.print_investeringen_html()
				]
		self.stroom_berekeningen_lijst = [ 
				 self.scenario.stroomtoename.print_meerverbruik_stroom_html(),
				 self.scenario.stroombesparing.print_besparingen_stroom_zp_html(),
				 self.scenario.print_bereken_kosten_stroom_var_html(),
				 self.scenario.print_bereken_kosten_stroom_vast_html(),
				 self.scenario.kosten.stroom_kosten_jaar_html() 
				 ]
		self.gas_berekeningen_lijst = [
				self.scenario.gasbesparing.print_besparingen_gas_html(),
				self.scenario.print_bereken_kosten_gas_var_html(),
				self.scenario.print_bereken_kosten_gas_vast_html(),
				self.scenario.kosten.gas_kosten_jaar_html()
				]
		self.output_berekeningen_lijst = [
				self.scenario.kosten.print_html()
				]
				
		self.verwerk_plafond()
		
	def verwerk_plafond(self):
		if self.scenario.soort == 'Scenario met plafond':
			self.input_berekeningen_lijst.append(self.scenario.plafond.print_html())	
		
	def input_berekeningen(self):
		html = ''
		for html_code in self.input_berekeningen_lijst:
			html += html_code
		return html
	
	def output_berekeningen(self):
		html = ''
		for html_code in self.output_berekeningen_lijst:
			html += html_code
		return html
	
	def stroom_berekeningen(self):
		html = ''
		for html_code in self.stroom_berekeningen_lijst:
			html += html_code
		return html	
	
	def gas_berekeningen(self):
		html = ''
		for html_code in self.gas_berekeningen_lijst:
			html += html_code
		return html
	
	def make_pdf(self):
		report_list = [self.input_berekeningen(),
					 self.output_berekeningen(),
					 self.gas_berekeningen(),
					 self.stroom_berekeningen() ]
		
				
		filename_date = datetime.now().strftime("%Y%m%d-%H%M%S")
		filename = self.scenario.naam + '_' + filename_date + '.html'
		
	
		f = open(filename, "x")
		
		for html_code in report_list:
			f.write(html_code)
			
		f.close()
		
	