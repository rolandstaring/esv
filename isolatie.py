###############
## Isolatie	 ##
###############


class Isolatie:
	def __init__ (self, naam,  prijs, rd , m2):
		self.naam= naam
		self.prijs = prijs
		self.rd = rd
		self.m2 = m2
	
	def reassign_values_from_list(self, values_list):	
		self.prijs = int(values_list[0].text())	
		self.rd = float(values_list[1].text())	
		self.m2 = float(values_list[2].text())	
	
	def return_labels_list(self):
		return [ 'naam',  'prijs', 'rd' , 'm2']
	
	def return_values_list(self):
		return [ self.naam,  self.prijs, self.rd, self.m2]
	 
	def make_dict(self):
		return dict(zip(self.return_labels_list, self.return_values_list))
	
	def __repr__(self):
		return '%sisolatie van %s voor € %s ' % (self.soort, self.naam, self.prijs)

class Vloerisolatie(Isolatie):
	soort = 'vloerisolatie'
	def __init__ (self,naam,  prijs, rd, m2):
		Isolatie.__init__(self, naam, prijs,rd, m2 )
		self.besp_tabel = {
			'tussenwoning':'80',
			'hoekwoning':130,
			'2onder1kap':'170',
			'vrijstaand':'250' }
	
	def bereken_gas_besparing(self, huishouden):
		return int(self.besp_tabel[huishouden.soort])
		
	def __repr__(self):
		return '%s '	 % ( Isolatie.__repr__(self))
	
class Dakisolatie(Isolatie):
	soort = 'dakisolatie'
	def __init__ (self,naam,  prijs, rd, m2):
		Isolatie.__init__(self, naam, prijs,rd, m2 )
	
		self.besp_tabel = {
			'tussenwoning':'400',
			'hoekwoning':'420',
			'2onder1kap':'440',
			'vrijstaand':'700' }
		
	def bereken_gas_besparing(self, huishouden):
		return int(self.besp_tabel[huishouden.soort])
	
	def __repr__(self):
		return '%s '	 % ( Isolatie.__repr__(self))

class Spouwisolatie(Isolatie):
	soort = 'spouwisolatie'
	def __init__ (self, naam, prijs, rd, m2):
		Isolatie.__init__(self, naam, prijs, rd, m2)
		self.besp_tabel = {
			'tussenwoning':'180',
			'hoekwoning':'400',
			'2onder1kap':'410',
			'vrijstaand':'600' }
		
	def bereken_gas_besparing(self,huishouden):
		return int(self.besp_tabel[huishouden.soort])
	
	def __repr__(self):
		return '%s '	 % ( Isolatie.__repr__(self))
		
class Glasisolatie(Isolatie):
	soort = 'glasisolatie'
	def __init__ (self, naam, prijs, rd, m2):
		Isolatie.__init__(self, naam, prijs,rd , m2)
	
	
	def bereken_gas_besparing(self,huishouden):
		return 0  # nader te berekenen
	
	def __repr__(self):
		return '%s '	 % ( Isolatie.__repr__(self))