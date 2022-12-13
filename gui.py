
import sys
import random
import pickle
import json
from report import Report 

import apparaat as apr   
import isolatie as iso
import huis as hs
import scenario as sc
#import report as rp

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
#from PyQt5 import QtNetwork as qtn
from PyQt5 import QtCore as qtc
#from PyQt5 import QtMultimedia as qtm


class SelecteerScenariosWidget(qtw.QWidget):

	
	def __init__(self, scenarios):
		super().__init__()
		self.title = 'Plafond gegevens '
		self.left = 500
		self.top = 200
		self.width = 200
		self.height = 250
		self.scenarios = scenarios
		
		self.InitUI()
		
	def InitUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left,self.top,self.width,self.height)
		
		self.vlayout = qtw.QVBoxLayout()
		self.button_layout = qtw.QHBoxLayout()
		
		self.huidig_label = qtw.QLabel('Kies een <i>Referentie<i> scenario ')
		self.toekomst_label = qtw.QLabel('Kies een <i>Wat als?</i> scenario')
		self.dropdown_huidig = qtw.QComboBox()
		self.dropdown_toekomst = qtw.QComboBox()
		
		items_list = []
		for s in self.scenarios:
			items_list.append(s.naam)
		
		self.dropdown_huidig.addItems(items_list)
		self.dropdown_toekomst.addItems(items_list)
		
		
		self.vergelijk_button = qtw.QPushButton(
			"Vergelijk",
			clicked= self.vergelijk)
	
		
		self.vlayout.addWidget(self.dropdown_huidig)
		self.vlayout.addWidget(self.dropdown_toekomst)
		self.vlayout.addWidget(self.vergelijk_button)

		self.setLayout(self.vlayout)
		
	def vergelijk(self):
		huidig_text = self.dropdown_huidig.currentText()
		toekomst_text = self.dropdown_toekomst.currentText()
		
		if huidig_text != toekomst_text:
			for s in self.scenarios:
				if huidig_text == s.naam:
					huidig = s
				elif toekomst_text == s.naam:
					toekomst = s
			
			verg_scenarios = sc.VergelijkScenarios(huidig,toekomst)
			self.scenario_verg_widget = ScenarioVergelijkWidget(verg_scenarios)
			self.scenario_verg_widget.show()
		
		self.close()
				

class VoegPlafondToeWidget(qtw.QWidget):
	submitted = qtc.pyqtSignal(object)
	
	def __init__(self, plafond,scenario):
		super().__init__()
		self.title = 'Plafond gegevens '
		self.left = 500
		self.top = 200
		self.width = 500
		self.height = 350

		self.plafond = plafond
		self.scenario = scenario
		
		self.InitUI()
		#naam,  soort, gas, stroom, prijs_gas,prijs_stroom, prijs_stroom_lev, prijs_vast
		
	def InitUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left,self.top,self.width,self.height)
		self.vlayout = qtw.QVBoxLayout()
		self.hlayout = qtw.QHBoxLayout()
		self.vlayout_left = qtw.QVBoxLayout()
		self.vlayout_right = qtw.QVBoxLayout()
		
		self.gui_edit_l = []
		
		self.vlayout.addLayout(self.hlayout)
		self.hlayout.addLayout(self.vlayout_left)
		self.hlayout.addLayout(self.vlayout_right)
		self.PlaceholderLabel = qtw.QLabel('	')
		
		self.save_button = qtw.QPushButton(
			"Save",
			clicked= self.save)
		
		
		for label, value in zip(self.plafond.return_labels_list(), self.plafond.return_values_list()):
			qlab = qtw.QLabel(label)
			qedit = qtw.QLineEdit()
			qedit.setText(str(value))
			
			self.gui_edit_l.append(qedit)
			self.vlayout_left.addWidget(qlab)
			self.vlayout_right.addWidget(qedit)
		
		
		self.vlayout_left.addWidget(self.PlaceholderLabel)
		self.vlayout_right.addWidget(self.save_button)
	
		self.setLayout(self.vlayout)
	
	def save(self):
	
		if self.gui_edit_l[0].isModified() == True or self.gui_edit_l[1].isModified() == True or self.gui_edit_l[2].isModified() == True or self.gui_edit_l[3].isModified() == True:
			self.plafond.energie_prijzen.gas_prijs_var  = float(self.gui_edit_l[0].text())	
			self.plafond.energie_prijzen.stroom_prijs_var  = float(self.gui_edit_l[1].text())
			self.plafond.gas_plafond = int(self.gui_edit_l[2].text())	
			self.plafond.stroom_plafond = int(self.gui_edit_l[3].text())		

		pscenario_naam = self.scenario.naam + '_plaf'
		pscenario = sc.ScenarioMetPlafond(pscenario_naam,self.scenario.iso_lijst,self.scenario.app_lijst, self.scenario.huis,self.plafond)
		self.submitted.emit(pscenario)
		self.close()

class EditWidget(qtw.QWidget):
	def __init__(self, investering):
		super().__init__()
		self.title = 'Edit ' + investering.naam 
		self.left = 500
		self.top = 200
		self.width = 500
		self.height = 350
		self.investering = investering
		
		self.InitUI()
		#naam,  soort, gas, stroom, prijs_gas,prijs_stroom, prijs_stroom_lev, prijs_vast
		
	def InitUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left,self.top,self.width,self.height)

		self.vlayout = qtw.QVBoxLayout()
		self.hlayout = qtw.QHBoxLayout()
		self.vlayout_left = qtw.QVBoxLayout()
		self.vlayout_right = qtw.QVBoxLayout()
		self.button_layout = qtw.QHBoxLayout()
		
		title_name = f"<b>{self.investering.naam},{self.investering.soort}</b>"
		
		self.TitelLabel = qtw.QLabel(title_name)
		self.PlaceholderLabel = qtw.QLabel('	')
		
		self.gui_edit_l = []
		
		self.vlayout.addWidget(self.TitelLabel)
		self.vlayout.addLayout(self.hlayout)
		self.hlayout.addLayout(self.vlayout_left)
		self.hlayout.addLayout(self.vlayout_right)
		
		
		self.save_button = qtw.QPushButton(
			"Save",
			clicked= self.save)
		
		self.exit_button = qtw.QPushButton(
			"Close",
			clicked= self.exit)
		
		self.labels_list = self.investering.return_labels_list()
		self.values_list = self.investering.return_values_list()
		self.labels_list.pop(0)
		self.values_list.pop(0)
		
		for label, value in zip(self.labels_list, self.values_list):
			qlab = qtw.QLabel(label)
			qedit = qtw.QLineEdit()
			qedit.setText(str(value))
			
			self.gui_edit_l.append(qedit)
			self.vlayout_left.addWidget(qlab)
			self.vlayout_right.addWidget(qedit)
		
		self.vlayout_left.addWidget(self.PlaceholderLabel)
		self.vlayout_right.addLayout(self.button_layout)
		
		self.button_layout.addWidget(self.save_button)
		self.button_layout.addWidget(self.exit_button)
	
		self.setLayout(self.vlayout)
		
	
	def save(self):
		for edit_l in self.gui_edit_l:
			if edit_l.isModified() == True:
				self.investering.reassign_values_from_list(self.gui_edit_l)
				break
		
	
	def exit(self):
		self.close()
			
class EditHuisWidget(qtw.QWidget):
	def __init__(self, huis):
		super().__init__()
		self.title = 'Edit ' + huis.naam
		self.huis = huis
		self.left = 500
		self.top = 200
		self.width = 500
		self.height = 350
		
		self.InitUI()
		
	def InitUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left,self.top,self.width,self.height)

		self.vlayout = qtw.QVBoxLayout()
		self.hlayout = qtw.QHBoxLayout()
		self.vlayout_left = qtw.QVBoxLayout()
		self.vlayout_right = qtw.QVBoxLayout()
		self.button_layout = qtw.QHBoxLayout()
		
		title_name = f"<b>{self.huis.naam},{self.huis.soort}</b>"
		
		self.TitelLabel = qtw.QLabel(title_name)
		self.PlaceholderLabel = qtw.QLabel('	')
		
		self.gui_edit_l = []
		
		self.vlayout.addWidget(self.TitelLabel)
	
		self.vlayout.addLayout(self.hlayout)
		self.hlayout.addLayout(self.vlayout_left)
		self.hlayout.addLayout(self.vlayout_right)
		
		self.save_button = qtw.QPushButton(
			"Save",
			clicked= self.save)
		
		self.exit_button = qtw.QPushButton(
			"Close",
			clicked= self.exit)
		
		self.labels_list = self.huis.return_labels_list()
		self.values_list = self.huis.return_values_list()
		self.labels_list.pop(0)
		self.values_list.pop(0)
		self.labels_list.pop(0)
		self.values_list.pop(0)
		
		for label, value in zip(self.labels_list, self.values_list):
			qlab = qtw.QLabel(label)
			qedit = qtw.QLineEdit()
			qedit.setText(str(value))
			
			self.gui_edit_l.append(qedit)
			self.vlayout_left.addWidget(qlab)
			self.vlayout_right.addWidget(qedit)
		
		self.vlayout_left.addWidget(self.PlaceholderLabel)
		self.vlayout_right.addLayout(self.button_layout)
		
		self.button_layout.addWidget(self.save_button)
		self.button_layout.addWidget(self.exit_button)
	
		self.setLayout(self.vlayout)
		
	
	def save(self):
		for edit_l in self.gui_edit_l:
			if edit_l.isModified() == True:
				self.huis.reassign_values_from_list(self.gui_edit_l)
				break
			
	def exit(self):
		self.close()

class ScenarioVergelijkWidget(qtw.QWidget):
	def __init__(self, scenario_verg):
		super().__init__()
		self.title = 'Vergelijken van scenarios'
		self.scenario_verg = scenario_verg
		self.left = 700
		self.top = 0
		self.width = 700
		self.height = 1000
		self.InitUI()
		# Main UI code goes here
	
	def InitUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left,self.top,self.width,self.height)
		
		self.vlayout = qtw.QVBoxLayout()
		self.hlayout = qtw.QHBoxLayout()
		self.vlayout_left = qtw.QVBoxLayout()
		self.vlayout_right = qtw.QVBoxLayout()
		
		self.vlayout.addLayout(self.hlayout)
		self.hlayout.addLayout(self.vlayout_left)
		self.hlayout.addLayout(self.vlayout_right)
		
		naam_huidig =  'Details ' + self.scenario_verg.huidig.naam
		naam_toekomst =  'Details ' + self.scenario_verg.toekomst.naam
		
		self.scenarioHuidigButton = qtw.QPushButton(
			naam_huidig,
			clicked= self.toon_details_huidig)
		
		self.scenarioToekomstButton = qtw.QPushButton(
			naam_toekomst,
			clicked= self.toon_details_toekomst)
		
		
		self.scenarioHuidigLabel = qtw.QLabel('Scenario huidig '+ self.scenario_verg.huidig.naam )
		self.scenarioToekomstLabel = qtw.QLabel('Scenario toekomst '+ self.scenario_verg.toekomst.naam )
		self.scenarioVergLabel = qtw.QLabel('Vergelijking')
		
		self.scenarioHuidigEdit = qtw.QTextEdit()
		self.scenarioToekomstEdit = qtw.QTextEdit()
		self.scenarioVergEdit = qtw.QTextEdit()
		
		self.scenario_verg.huidig
		
		kosten_huidig = self.scenario_verg.huidig.kosten.print_html()
		investeringen_huidig = self.scenario_verg.huidig.print_investeringen_html()
		huidig_text = kosten_huidig + investeringen_huidig
		
		kosten_toekomst = self.scenario_verg.toekomst.kosten.print_html()
		investeringen_toekomst = self.scenario_verg.toekomst.print_investeringen_html()
		toekomst_text =kosten_toekomst + investeringen_toekomst
		
		complement_investeringen = self.scenario_verg.print_complement_html()
		roi_vergelijking =  self.scenario_verg.print_html()
		vergelijking_text = complement_investeringen + roi_vergelijking
		
		self.scenarioHuidigEdit.setHtml(huidig_text)
		self.scenarioToekomstEdit.setHtml(toekomst_text)
		self.scenarioVergEdit.setHtml(vergelijking_text)
		
		self.vlayout_left.addWidget(self.scenarioHuidigLabel)
		self.vlayout_left.addWidget(self.scenarioHuidigEdit)
		self.vlayout_left.addWidget(self.scenarioHuidigButton)
		
		self.vlayout_left.addWidget(self.scenarioToekomstLabel)
		self.vlayout_left.addWidget(self.scenarioToekomstEdit)
		self.vlayout_left.addWidget(self.scenarioToekomstButton)
		
		self.vlayout_right.addWidget(self.scenarioVergLabel)
		self.vlayout_right.addWidget(self.scenarioVergEdit)
		
		
		self.setLayout(self.vlayout)
	
	def toon_details_huidig(self):
		
		self.scenario_widget = ScenarioWidget(self.scenario_verg.huidig)
		self.scenario_widget.show()
	
	def toon_details_toekomst(self):
		
		self.scenario_widget = ScenarioWidget(self.scenario_verg.toekomst)
		self.scenario_widget.show()
					
class ScenarioWidget(qtw.QWidget):
	submitted = qtc.pyqtSignal(object)
	def __init__(self, scenario):
		super().__init__()
		self.title = 'Scenario ' + scenario.naam
		self.scenario = scenario
		self.left = 0
		self.top = 0
		self.width = 700
		self.height = 1000
		self.InitUI()
		# Main UI code goes here
		
	def InitUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left,self.top,self.width,self.height)
		
		myFont=qtg.QFont()
		myFont.setBold(True)
		
		self.vlayout = qtw.QVBoxLayout()
		self.hlayout = qtw.QHBoxLayout()
		self.vlayout_left = qtw.QVBoxLayout()
		#self.vlayout_mid = qtw.QVBoxLayout()
		self.vlayout_right = qtw.QVBoxLayout()
		
		self.vlayout.addLayout(self.hlayout)
		self.hlayout.addLayout(self.vlayout_left)
		#self.hlayout.addLayout(self.vlayout_mid)
		self.hlayout.addLayout(self.vlayout_right)
		
		
		self.add_plafond_button = qtw.QPushButton(
			"Voeg plafond toe",
			clicked= self.add_plafond)
		
		self.report_button = qtw.QPushButton(
			"Maak rapport",
			clicked= self.make_report)
		
		self.scenarioInLabel = qtw.QLabel('Scenario Input')
		self.scenarioUitLabel = qtw.QLabel('Scenario Output')
		self.scenarioBerekeningGasLabel = qtw.QLabel('Scenario Berekening Gas')
		self.scenarioBerekeningStroomLabel = qtw.QLabel('Scenario Berekening Stroom')
		self.scenarioInEdit = qtw.QTextEdit()
		self.scenarioOutEdit = qtw.QTextEdit()
		self.scenarioBerekeningGasEdit = qtw.QTextEdit()
		self.scenarioBerekeningStroomEdit = qtw.QTextEdit()
		
		self.report = Report(self.scenario)
				
		self.scenarioInEdit.setHtml(self.report.input_berekeningen())
		self.scenarioOutEdit.setHtml(self.report.output_berekeningen())
		self.scenarioBerekeningGasEdit.setHtml(self.report.gas_berekeningen())
		self.scenarioBerekeningStroomEdit.setHtml(self.report.stroom_berekeningen())
		
		if self.scenario.soort == 'Scenario zonder plafond':
			self.vlayout_left.addWidget(self.add_plafond_button)
		self.vlayout_left.addWidget(self.report_button)
		
		self.vlayout_left.addWidget(self.scenarioUitLabel)
		self.vlayout_left.addWidget(self.scenarioOutEdit)
		
		self.vlayout_left.addWidget(self.scenarioInLabel)
		self.vlayout_left.addWidget(self.scenarioInEdit)
	
		self.vlayout_right.addWidget(self.scenarioBerekeningGasLabel)
		self.vlayout_right.addWidget(self.scenarioBerekeningGasEdit)
		
		self.vlayout_right.addWidget(self.scenarioBerekeningStroomLabel)
		self.vlayout_right.addWidget(self.scenarioBerekeningStroomEdit)
		
		
		self.setLayout(self.vlayout)
		
	def	add_plafond(self):
		energie_prijzen= hs.EnergiePrijs(0,0)
		plafond = hs.Plafond(energie_prijzen,0,0)
		self.plafond_widget = VoegPlafondToeWidget(plafond,self.scenario)
		self.plafond_widget.submitted.connect(self.voeg_plafond_scenario_aan_lijst)
		self.plafond_widget.show()
	
	
	def make_report(self):
		self.report.make_pdf()
		
	def voeg_plafond_scenario_aan_lijst(self,pscenario):
		self.submitted.emit(pscenario)
			
#########
## Wizard voor huizen
#########

class AdresPage(qtw.QWizardPage):
	def __init__(self):
		super().__init__()
		
		self.InitUI()
		
	def InitUI(self):
		myFont=qtg.QFont()
		myFont.setBold(True)
		
		self.q_label = qtw.QLabel('Wat is je adres?')
		self.q_label.setFont(myFont)
		
		self.straat_label = qtw.QLabel('Straatnaam')
		self.straat_le = qtw.QLineEdit()
		self.straat_le.setFixedWidth(200)
		
		self.nr_label = qtw.QLabel('Nummer')
		self.nr_le = qtw.QLineEdit()
		self.nr_le.setFixedWidth(200)
		
		self.vlayout = qtw.QVBoxLayout()
		self.hlayout1 = qtw.QHBoxLayout()
		self.hlayout2 = qtw.QHBoxLayout()
		
		
		self.vlayout.addWidget(self.q_label)
		
		self.vlayout.addLayout(self.hlayout1)
		self.hlayout1.addWidget(self.straat_label)
		self.hlayout1.addWidget(self.straat_le)
		
		self.vlayout.addLayout(self.hlayout2)
		self.hlayout2.addWidget(self.nr_label)
		self.hlayout2.addWidget(self.nr_le)
		
		self.registerField('straatnaam',self.straat_le)
		self.registerField('straatnr',self.nr_le)
		
		self.setLayout(self.vlayout)

class HouseTypePage(qtw.QWizardPage):
	def __init__(self):
		super().__init__()
		
		
		self.InitUI()
		
	def InitUI(self):
		
		self.vlayout = qtw.QVBoxLayout()
		self.q_label = qtw.QLabel('In wat voor huis woon je?')
	
		self.hh = qtw.QCheckBox("hoekwoning")
		self.tw = qtw.QCheckBox("tussenwoning")
		self.tk = qtw.QCheckBox("2Onder1Kap")
		self.vs = qtw.QCheckBox("vrijstaand")
		
		#self.tw.setChecked(True)
		
		self.bg = qtw.QButtonGroup()
		self.bg.addButton(self.hh,1)
		self.bg.addButton(self.tw,2)
		self.bg.addButton(self.tk,3)
		self.bg.addButton(self.vs,4)
		
		
		self.vlayout.addWidget(self.q_label)
		self.vlayout.addWidget(self.hh)
		self.vlayout.addWidget(self.tw)
		self.vlayout.addWidget(self.tk)
		self.vlayout.addWidget(self.vs)
		
		self.setLayout(self.vlayout)
		
		self.bg.buttonClicked.connect(self.onButtonClick)
		
	
	def onButtonClick(self):
		checkbox = self.bg.checkedButton()
		self.registerField('house_type',checkbox,"text")
		
class EnergyPricePage(qtw.QWizardPage):
	def __init__(self):
		super().__init__()
		self.InitUI()
		
	def InitUI(self):
	
		self.vlayout = qtw.QVBoxLayout()
		
		myFont=qtg.QFont()
		myFont.setBold(True)
		
		self.t2_label = qtw.QLabel('Prijzen voor energie')
		self.t2_label.setFont(myFont)
		
		self.hlayout1 = qtw.QHBoxLayout()
		self.hlayout2 = qtw.QHBoxLayout()
		self.hlayout3 = qtw.QHBoxLayout()
		self.hlayout4 = qtw.QHBoxLayout()
		self.hlayout5 = qtw.QHBoxLayout()
		
		# Gas kosten variabel
		self.prijs_gas_var_label = qtw.QLabel('Prijs Gas verbruik')
		self.prijs_gas_var = qtw.QLineEdit()
		self.prijs_gas_var.setFixedWidth(60)
		self.eurom3_label = qtw.QLabel('€ per m3')
		
		# Stroom kosten variabel
		self.prijs_stroom_var_label = qtw.QLabel('Prijs Stroom verbruik ')
		self.prijs_stroom_var = qtw.QLineEdit()
		self.prijs_stroom_var.setFixedWidth(60)
		self.eurokwh_label = qtw.QLabel('€ per kwh')
		
		# Stroom kosten variabel
		self.prijs_stroom_var_lev_label = qtw.QLabel('Prijs Stroom levering')
		self.prijs_stroom_var_lev = qtw.QLineEdit()
		self.prijs_stroom_var_lev.setFixedWidth(60)
		self.eurokwh2_label = qtw.QLabel('€ per kwh')
		
		# Stroom kosten vast
		self.prijs_stroom_vast_label = qtw.QLabel('Stroom prijs vast')
		self.prijs_stroom_vast = qtw.QLineEdit()
		self.prijs_stroom_vast.setFixedWidth(60)
		self.euro1_label = qtw.QLabel('€ per dag')
		
		# Gas kosten vast
		self.prijs_gas_vast_label = qtw.QLabel('Gas prijs vast')
		self.prijs_gas_vast = qtw.QLineEdit()
		self.prijs_gas_vast.setFixedWidth(60)
		self.euro2_label = qtw.QLabel('€ per dag')
		
		self.vlayout.addWidget(self.t2_label)
	
		self.vlayout.addLayout(self.hlayout1)
		self.hlayout1.addWidget(self.prijs_gas_var_label)
		self.hlayout1.addWidget(self.prijs_gas_var)
		self.hlayout1.addWidget(self.eurom3_label)
		
		self.vlayout.addLayout(self.hlayout2)
		self.hlayout2.addWidget(self.prijs_stroom_var_label)
		self.hlayout2.addWidget(self.prijs_stroom_var)
		self.hlayout2.addWidget(self.eurokwh_label)
		
		self.vlayout.addLayout(self.hlayout3)
		self.hlayout3.addWidget(self.prijs_stroom_var_lev_label)
		self.hlayout3.addWidget(self.prijs_stroom_var_lev)
		self.hlayout3.addWidget(self.eurokwh2_label)
		
		self.vlayout.addLayout(self.hlayout4)
		self.hlayout4.addWidget(self.prijs_stroom_vast_label)
		self.hlayout4.addWidget(self.prijs_stroom_vast)
		self.hlayout4.addWidget(self.euro1_label)
		
		self.vlayout.addLayout(self.hlayout5)
		self.hlayout5.addWidget(self.prijs_gas_vast_label)
		self.hlayout5.addWidget(self.prijs_gas_vast)
		self.hlayout5.addWidget(self.euro2_label)
		
		self.setLayout(self.vlayout)
		
		self.registerField('prijsgasvar',self.prijs_gas_var)
		self.registerField('prijsstroomvar',self.prijs_stroom_var)
		self.registerField('prijsstroomlev',self.prijs_stroom_var_lev)
		self.registerField('prijsstroomvast',self.prijs_stroom_vast)
		self.registerField('prijsgasvast',self.prijs_gas_vast)

class EnergyUsagePage(qtw.QWizardPage):
	def __init__(self):
		super().__init__()
		self.InitUI()
		
	def InitUI(self):
	
		self.vlayout = qtw.QVBoxLayout()
		
		myFont=qtg.QFont()
		myFont.setBold(True)
		
		self.t_label = qtw.QLabel('Energie verbruik per jaar')
		self.t_label.setFont(myFont)
	
		
		self.hlayout1 = qtw.QHBoxLayout()
		self.hlayout2 = qtw.QHBoxLayout()

		
		# Gas verbruik jaar
		self.gas_label = qtw.QLabel('Gas')
		self.gasm3 = qtw.QLineEdit()
		self.gasm3.setFixedWidth(60)
		self.eenheid_gas_label = qtw.QLabel('m3/jaar')
		
		
		#Stroom verbruik jaar
		self.stroom_label = qtw.QLabel('Stroom')
		self.stroomkwh = qtw.QLineEdit()
		self.stroomkwh.setFixedWidth(60)
		self.eenheid_stroom_label = qtw.QLabel('kwh/jaar')
		
	
		self.vlayout.addWidget(self.t_label)
		
		self.vlayout.addLayout(self.hlayout1)
		self.hlayout1.addWidget(self.gas_label)
		self.hlayout1.addWidget(self.gasm3)
		self.hlayout1.addWidget(self.eenheid_gas_label)
		
		self.vlayout.addLayout(self.hlayout2)
		self.hlayout2.addWidget(self.stroom_label)
		self.hlayout2.addWidget(self.stroomkwh)
		self.hlayout2.addWidget(self.eenheid_stroom_label)
		
		self.setLayout(self.vlayout)
		
		self.registerField('gasm3',self.gasm3)
		self.registerField('stroomkwh',self.stroomkwh)	

class MijnHuisWizard(qtw.QWizard):
	submitted = qtc.pyqtSignal(object)
	 
	def __init__(self):
		super().__init__()
		self.addPage(AdresPage())
		self.addPage(HouseTypePage())
		self.addPage(EnergyUsagePage())
		self.addPage(EnergyPricePage())
		
		self.button(qtw.QWizard.FinishButton).clicked.connect(self.onFinish)
		
		self.InitUI()
	
	def InitUI(self):
		self.setWindowTitle("Details van huishouden")
	
	def onFinish(self):
		huis_soort = self.field('house_type')
		gasm3 = self.field('gasm3')
		stroomkwh = self.field('stroomkwh')
		prijs_gas_var = self.field('prijsgasvar')
		prijs_stroom_var = self.field('prijsstroomvar')
		prijs_stroom_var_lev = self.field('prijsstroomlev')
		prijs_stroom_vast = self.field('prijsstroomvast')
		prijs_gas_vast = self.field('prijsgasvast')
		
		adres = self.field('straatnaam')+ ' ' + self.field('straatnr')
		
		energie_prijzen = hs.EnergiePrijs(float(prijs_gas_var), float(prijs_stroom_var), float(prijs_stroom_var_lev),float(prijs_stroom_vast),float(prijs_gas_vast))
		energie_verbruik = hs.EnergieVerbruik('Verbruik voor Investering',int(gasm3), int(stroomkwh))
		
		huis = hs.Huishouden(adres,huis_soort,energie_verbruik, energie_prijzen)
		self.submitted.emit(huis)
		
	
#########
## Wizard voor zonnepanelen 
#########	
	
class LeverancierPrijsPage(qtw.QWizardPage):
	def __init__(self):
		super().__init__()
		
		myFont=qtg.QFont()
		myFont.setBold(True)
		
		self.q_label = qtw.QLabel('Leverancier en prijs')
		self.q_label.setFont(myFont)
		
		self.merk_label = qtw.QLabel('Merk of Naam')
		self.merk_le = qtw.QLineEdit()
		self.merk_le.setFixedWidth(200)
		
		self.prijs_label = qtw.QLabel('Prijs')
		self.prijs_le = qtw.QLineEdit()
		self.prijs_le.setFixedWidth(200)
		
		self.vlayout = qtw.QVBoxLayout()
		self.hlayout1 = qtw.QHBoxLayout()
		self.hlayout2 = qtw.QHBoxLayout()
		
		self.vlayout.addWidget(self.q_label)
		
		self.vlayout.addLayout(self.hlayout1)
		self.hlayout1.addWidget(self.merk_label)
		self.hlayout1.addWidget(self.merk_le)
		
		self.vlayout.addLayout(self.hlayout2)
		self.hlayout2.addWidget(self.prijs_label)
		self.hlayout2.addWidget(self.prijs_le)
		
		self.registerField('merk',self.merk_le)
		self.registerField('prijs',self.prijs_le)
		
		self.setLayout(self.vlayout)
		
class AantalWattJaarSchaduwPage(qtw.QWizardPage):
	def __init__(self):
		super().__init__()
		
		myFont=qtg.QFont()
		myFont.setBold(True)
		
		self.q_label = qtw.QLabel('Zonnepanelen info')
		self.q_label.setFont(myFont)
		
		self.aantal_label = qtw.QLabel('Aantal')
		self.aantal_le = qtw.QLineEdit()
		self.aantal_le.setFixedWidth(120)
		
		self.watt_label = qtw.QLabel('Watt')
		self.watt_le = qtw.QLineEdit()
		self.watt_le.setFixedWidth(120)
		
		self.jaar_label = qtw.QLabel('Jaar aanschaf')
		self.jaar_le = qtw.QLineEdit()
		self.jaar_le.setFixedWidth(120)
		
		self.schaduw_label = qtw.QLabel('Schaduw factor')
		self.schaduw_le = qtw.QLineEdit()
		self.schaduw_le.setFixedWidth(120)
		
		self.vlayout = qtw.QVBoxLayout()
		self.hlayout1 = qtw.QHBoxLayout()
		self.hlayout2 = qtw.QHBoxLayout()
		self.hlayout3 = qtw.QHBoxLayout()
		self.hlayout4 = qtw.QHBoxLayout()
		
		self.vlayout.addWidget(self.q_label)
		
		self.vlayout.addLayout(self.hlayout1)
		self.hlayout1.addWidget(self.aantal_label)
		self.hlayout1.addWidget(self.aantal_le)
		
		self.vlayout.addLayout(self.hlayout2)
		self.hlayout2.addWidget(self.watt_label)
		self.hlayout2.addWidget(self.watt_le)
		
		self.vlayout.addLayout(self.hlayout3)
		self.hlayout3.addWidget(self.jaar_label)
		self.hlayout3.addWidget(self.jaar_le)
		
		self.vlayout.addLayout(self.hlayout4)
		self.hlayout4.addWidget(self.schaduw_label)
		self.hlayout4.addWidget(self.schaduw_le)
		
		self.registerField('aantal',self.aantal_le)
		self.registerField('watt',self.watt_le)
		self.registerField('jaar',self.jaar_le)
		self.registerField('schaduw',self.schaduw_le)
		
		self.setLayout(self.vlayout)

class MijnZonnepanelenWizard(qtw.QWizard):
	submitted = qtc.pyqtSignal(object)
	 
	def __init__(self):
		super().__init__()
		self.addPage(LeverancierPrijsPage())
		self.addPage(AantalWattJaarSchaduwPage())
		
		
		self.button(qtw.QWizard.FinishButton).clicked.connect(self.onFinish)
		
		self.InitUI()
	
	def InitUI(self):
		self.setWindowTitle("Details van zonnepanelen")
	
	def onFinish(self):
		merk = self.field('merk')
		prijs = self.field('prijs')
		aantal = self.field('aantal')
		watt = self.field('watt')
		jaar = self.field('jaar')
		schaduw= self.field('schaduw')
	
		
		zp = apr.Zonnepanelen(merk,int(prijs),int(watt),int(aantal), int(jaar), float(schaduw))
		self.submitted.emit(zp)
		
		
#########
## Wizard voor zonneboiler
#########	
	
class LeverancierPrijsCapPage(qtw.QWizardPage):
	def __init__(self):
		super().__init__()
		
		myFont=qtg.QFont()
		myFont.setBold(True)
		
		self.q_label = qtw.QLabel('Leverancier en prijs')
		self.q_label.setFont(myFont)
		
		self.merk_label = qtw.QLabel('Merk of Naam')
		self.merk_le = qtw.QLineEdit()
		self.merk_le.setFixedWidth(200)
		
		self.prijs_label = qtw.QLabel('Prijs')
		self.prijs_le = qtw.QLineEdit()
		self.prijs_le.setFixedWidth(200)
		
		self.cap_label = qtw.QLabel('Capaciteit')
		self.cap_le = qtw.QLineEdit()
		self.cap_le.setFixedWidth(200)
		
		
		self.watt_label = qtw.QLabel('Watt')
		self.watt_le = qtw.QLineEdit()
		self.watt_le.setFixedWidth(200)

		
		
		self.vlayout = qtw.QVBoxLayout()
		self.hlayout1 = qtw.QHBoxLayout()
		self.hlayout2 = qtw.QHBoxLayout()
		self.hlayout3 = qtw.QHBoxLayout()
		self.hlayout4 = qtw.QHBoxLayout()
		
		self.vlayout.addWidget(self.q_label)
		
		self.vlayout.addLayout(self.hlayout1)
		self.hlayout1.addWidget(self.merk_label)
		self.hlayout1.addWidget(self.merk_le)
		
		self.vlayout.addLayout(self.hlayout2)
		self.hlayout2.addWidget(self.prijs_label)
		self.hlayout2.addWidget(self.prijs_le)
		
		self.vlayout.addLayout(self.hlayout3)
		self.hlayout3.addWidget(self.cap_label)
		self.hlayout3.addWidget(self.cap_le)
		
		
		self.vlayout.addLayout(self.hlayout3)
		self.hlayout3.addWidget(self.watt_label)
		self.hlayout3.addWidget(self.watt_le)

		
		
		self.registerField('merk',self.merk_le)
		self.registerField('prijs',self.prijs_le)
		self.registerField('capaciteit',self.cap_le)
		self.registerField('watt',self.watt_le)
		
		self.setLayout(self.vlayout)
		
class MijnZonneboilerWizard(qtw.QWizard):
	submitted = qtc.pyqtSignal(object)
	 
	def __init__(self):
		super().__init__()
		self.addPage(LeverancierPrijsCapPage())
				
		self.button(qtw.QWizard.FinishButton).clicked.connect(self.onFinish)
		
		self.InitUI()
	
	def InitUI(self):
		self.setWindowTitle("Details van zonnepanelen")
	
	def onFinish(self):
		merk = self.field('merk')
		prijs = self.field('prijs')
		cap = self.field('capaciteit')
		watt = self.field('watt')
		

		zb = apr.Zonneboiler(merk,int(prijs),int(cap),watt)
		self.submitted.emit(zb)

#########
## Wizard voor warmtepomp
#########	
	
class LeverancierPrijsCopGasPage(qtw.QWizardPage):
	def __init__(self):
		super().__init__()
		
		myFont=qtg.QFont()
		myFont.setBold(True)
		
		self.q_label = qtw.QLabel('Leverancier en prijs')
		self.q_label.setFont(myFont)
		
		self.merk_label = qtw.QLabel('Merk of Naam')
		self.merk_le = qtw.QLineEdit()
		self.merk_le.setFixedWidth(200)
		
		self.prijs_label = qtw.QLabel('Prijs')
		self.prijs_le = qtw.QLineEdit()
		self.prijs_le.setFixedWidth(200)
		
		self.cop_label = qtw.QLabel('COP')
		self.cop_le = qtw.QLineEdit()
		self.cop_le.setFixedWidth(120)
		
		self.gbc_label = qtw.QLabel('GBC')
		self.gbc_le = qtw.QLineEdit()
		self.gbc_le.setFixedWidth(120)
		
		self.vlayout = qtw.QVBoxLayout()
		self.hlayout1 = qtw.QHBoxLayout()
		self.hlayout2 = qtw.QHBoxLayout()
		self.hlayout3 = qtw.QHBoxLayout()
		self.hlayout4 = qtw.QHBoxLayout()
		
		self.vlayout.addWidget(self.q_label)
		
		self.vlayout.addLayout(self.hlayout1)
		self.hlayout1.addWidget(self.merk_label)
		self.hlayout1.addWidget(self.merk_le)
		
		self.vlayout.addLayout(self.hlayout2)
		self.hlayout2.addWidget(self.prijs_label)
		self.hlayout2.addWidget(self.prijs_le)
		
		self.vlayout.addLayout(self.hlayout3)
		self.hlayout3.addWidget(self.cop_label)
		self.hlayout3.addWidget(self.cop_le)
		
		self.vlayout.addLayout(self.hlayout4)
		self.hlayout4.addWidget(self.gbc_label)
		self.hlayout4.addWidget(self.gbc_le)
		
		self.registerField('merk',self.merk_le)
		self.registerField('prijs',self.prijs_le)
		self.registerField('cop',self.cop_le)
		self.registerField('gbc',self.gbc_le)
		
		self.setLayout(self.vlayout)
		
class MijnWarmtepompWizard(qtw.QWizard):
	submitted = qtc.pyqtSignal(object)
	 
	def __init__(self):
		super().__init__()
		self.addPage(LeverancierPrijsCopGasPage())
				
		self.button(qtw.QWizard.FinishButton).clicked.connect(self.onFinish)
		
		self.InitUI()
	
	def InitUI(self):
		self.setWindowTitle("Details van warmtepomp")
	
	def onFinish(self):
		merk = self.field('merk')
		prijs = self.field('prijs')
		cop = self.field('cop')
		gbc = self.field('gbc')

		wp = apr.Warmtepomp(merk,int(prijs),float(cop),float(gbc))
		self.submitted.emit(wp)

#########
## Wizardpagina generiek voor isolatie
#########

class IsolatieInputPage(qtw.QWizardPage):
	def __init__(self, isolatie_soort):
		super().__init__()
		
		myFont=qtg.QFont()
		myFont.setBold(True)
		
		beschrijving = 'Gegevens ' + isolatie_soort
		
		self.q_label = qtw.QLabel(beschrijving)
		self.q_label.setFont(myFont)
		
		self.merk_label = qtw.QLabel('Merk of Naam')
		self.merk_le = qtw.QLineEdit()
		self.merk_le.setFixedWidth(200)
		
		self.prijs_label = qtw.QLabel('Prijs')
		self.prijs_le = qtw.QLineEdit()
		self.prijs_le.setFixedWidth(200)
		
		self.rd_label = qtw.QLabel('Rd')
		self.rd_le = qtw.QLineEdit()
		self.rd_le.setFixedWidth(200)
		
		self.m2_label = qtw.QLabel('m2')
		self.m2_le = qtw.QLineEdit()
		self.m2_le.setFixedWidth(200)
		
		self.vlayout = qtw.QVBoxLayout()
		self.hlayout1 = qtw.QHBoxLayout()
		self.hlayout2 = qtw.QHBoxLayout()
		self.hlayout3 = qtw.QHBoxLayout()
		self.hlayout4 = qtw.QHBoxLayout()
		
		self.vlayout.addWidget(self.q_label)
		
		self.vlayout.addLayout(self.hlayout1)
		self.hlayout1.addWidget(self.merk_label)
		self.hlayout1.addWidget(self.merk_le)
		
		self.vlayout.addLayout(self.hlayout2)
		self.hlayout2.addWidget(self.prijs_label)
		self.hlayout2.addWidget(self.prijs_le)
		
		self.vlayout.addLayout(self.hlayout3)
		self.hlayout3.addWidget(self.rd_label)
		self.hlayout3.addWidget(self.rd_le)
		
		self.vlayout.addLayout(self.hlayout4)
		self.hlayout4.addWidget(self.m2_label)
		self.hlayout4.addWidget(self.m2_le)
		
		merk_veld = 'merk_' + isolatie_soort
		prijs_veld = 'prijs_' + isolatie_soort
		rd_veld = 'rd_' + isolatie_soort
		m2_veld = 'm2_' + isolatie_soort
		
		
		self.registerField(merk_veld,self.merk_le)
		self.registerField(prijs_veld,self.prijs_le)
		self.registerField(rd_veld,self.rd_le)
		self.registerField(m2_veld,self.m2_le)
		
		self.setLayout(self.vlayout)

#########
## Wizards voor vloer, dak, spouw en glasisolatie
#########	
	

class MijnVloerisolatieWizard(qtw.QWizard):
	submitted = qtc.pyqtSignal(object)
	 
	def __init__(self):
		super().__init__()
		self.isolatie_soort = 'vloer'
		self.addPage(IsolatieInputPage(self.isolatie_soort))
				
		self.button(qtw.QWizard.FinishButton).clicked.connect(self.onFinish)
		
		self.InitUI()
	
	def InitUI(self):
		beschrijving = 'Details van ' + self.isolatie_soort + 'isolatie'
		self.setWindowTitle(beschrijving)
	
	def onFinish(self):
		
		merk_veld = 'merk_' + self.isolatie_soort
		prijs_veld = 'prijs_' + self.isolatie_soort
		rd_veld = 'rd_' + self.isolatie_soort
		m2_veld = 'm2_' + self.isolatie_soort
		
		merk = self.field(merk_veld)
		prijs = self.field(prijs_veld)
		rd = self.field(rd_veld)
		m2 = self.field(m2_veld)

		vloer = iso.Vloerisolatie(merk,int(prijs),float(rd),float(m2))
		self.submitted.emit(vloer)
	
class MijnDakisolatieWizard(qtw.QWizard):
	submitted = qtc.pyqtSignal(object)
	 
	def __init__(self):
		super().__init__()
		self.isolatie_soort = 'dak'
		self.addPage(IsolatieInputPage(self.isolatie_soort))
				
		self.button(qtw.QWizard.FinishButton).clicked.connect(self.onFinish)
		
		self.InitUI()
	
	def InitUI(self):
		beschrijving = 'Details van ' + self.isolatie_soort + 'isolatie'
		self.setWindowTitle(beschrijving)
	
	def onFinish(self):
		
		merk_veld = 'merk_' + self.isolatie_soort
		prijs_veld = 'prijs_' + self.isolatie_soort
		rd_veld = 'rd_' + self.isolatie_soort
		m2_veld = 'm2_' + self.isolatie_soort
		
		merk = self.field(merk_veld)
		prijs = self.field(prijs_veld)
		rd = self.field(rd_veld)
		m2 = self.field(m2_veld)

		dak = iso.Dakisolatie(merk,int(prijs),float(rd),float(m2))
		self.submitted.emit(dak)
	
class MijnSpouwisolatieWizard(qtw.QWizard):
	submitted = qtc.pyqtSignal(object)
	 
	def __init__(self):
		super().__init__()
		self.isolatie_soort = 'spouw'
		self.addPage(IsolatieInputPage(self.isolatie_soort))
				
		self.button(qtw.QWizard.FinishButton).clicked.connect(self.onFinish)
		
		self.InitUI()
	
	def InitUI(self):
		beschrijving = 'Details van ' + self.isolatie_soort + 'isolatie'
		self.setWindowTitle(beschrijving)
	
	def onFinish(self):
		
		merk_veld = 'merk_' + self.isolatie_soort
		prijs_veld = 'prijs_' + self.isolatie_soort
		rd_veld = 'rd_' + self.isolatie_soort
		m2_veld = 'm2_' + self.isolatie_soort
		
		merk = self.field(merk_veld)
		prijs = self.field(prijs_veld)
		rd = self.field(rd_veld)
		m2 = self.field(m2_veld)

		spouw = iso.Spouwisolatie(merk,int(prijs),float(rd),float(m2))
		self.submitted.emit(spouw)

class MijnGlasisolatieWizard(qtw.QWizard):
	submitted = qtc.pyqtSignal(object)
	 
	def __init__(self):
		super().__init__()
		self.isolatie_soort = 'glas'
		self.addPage(IsolatieInputPage(self.isolatie_soort))
				
		self.button(qtw.QWizard.FinishButton).clicked.connect(self.onFinish)
		
		self.InitUI()
	
	def InitUI(self):
		beschrijving = 'Details van ' + self.isolatie_soort + 'isolatie'
		self.setWindowTitle(beschrijving)
	
	def onFinish(self):
		
		merk_veld = 'merk_' + self.isolatie_soort
		prijs_veld = 'prijs_' + self.isolatie_soort
		rd_veld = 'rd_' + self.isolatie_soort
		m2_veld = 'm2_' + self.isolatie_soort
		
		merk = self.field(merk_veld)
		prijs = self.field(prijs_veld)
		rd = self.field(rd_veld)
		m2 = self.field(m2_veld)

		glas = iso.Glasisolatie(merk,int(prijs),float(rd),float(m2))
		self.submitted.emit(glas)

###############################
##### Hoofdscherm
########################


class MainWindow(qtw.QMainWindow): # change to mainwindow
	
	def __init__(self):
	
		super().__init__()
		
		self.s_nr = 0
		self.huizen = []
		self.apparaten = []
		self.isolaties = []
		self.scenario_emmer = []
		self.scenarios = []
		self.title = 'Duurzaamheids Scenario'
		self.left = 500
		self.top = 200
		self.width = 800
		self.height = 250
		self.InitUI()
		# Main UI code goes here
		
	def InitUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left,self.top,self.width,self.height)
	
		## maak de hoofdwidget en layouts aan
		
		self.cwidget = qtw.QWidget()	
		self.hlayout = qtw.QHBoxLayout()
		self.vlayout_left = qtw.QVBoxLayout()
		self.vlayout_mid = qtw.QVBoxLayout()
		self.vlayout_right = qtw.QVBoxLayout()
		
		self.cwidget.setLayout(self.hlayout)
		self.hlayout.addLayout(self.vlayout_left)
		self.hlayout.addLayout(self.vlayout_mid)
		self.hlayout.addLayout(self.vlayout_right)

		## Maak de widgets (knoppen, labels en lijsten) aan	 
		
		self.emmer_button = qtw.QPushButton(
			"Bereken Scenario",
			clicked= self.bereken_scenario_van_emmer)
		
		self.scenario_vergelijk_button = qtw.QPushButton(
			"Vergelijk Scenarios",
			clicked= self.vergelijk_scenarios)
			
		self.edit_huis_button = qtw.QPushButton(
			"Edit",
			clicked= self.edit_huis)
	
		self.del_huis_button = qtw.QPushButton(
			"Del",
			clicked= self.del_huis)
		
		self.edit_app_button = qtw.QPushButton(
			"Edit",
			clicked= self.edit_app)
	
		self.del_app_button = qtw.QPushButton(
			"Del",
			clicked= self.del_app)
		
		self.edit_iso_button = qtw.QPushButton(
			"Edit",
			clicked= self.edit_iso)
	
		self.del_iso_button = qtw.QPushButton(
			"Del",
			clicked= self.del_iso)
		
		self.del_emmer_button = qtw.QPushButton(
			"Del",
			clicked= self.del_emmer)
		
		self.del_scenario_button = qtw.QPushButton(
			"Del",
			clicked= self.del_scenario)
		
		self.button_layout_huis = qtw.QHBoxLayout()
		self.button_layout_huis.addWidget(self.edit_huis_button)
		self.button_layout_huis.addWidget(self.del_huis_button)

		self.button_layout_app = qtw.QHBoxLayout()
		self.button_layout_app.addWidget(self.edit_app_button)
		self.button_layout_app.addWidget(self.del_app_button)

		self.button_layout_iso = qtw.QHBoxLayout()
		self.button_layout_iso.addWidget(self.edit_iso_button)
		self.button_layout_iso.addWidget(self.del_iso_button)
		
		self.button_layout_emmer = qtw.QHBoxLayout()
		self.button_layout_emmer.addWidget(self.emmer_button)
		self.button_layout_emmer.addWidget(self.del_emmer_button)
		
		self.button_layout_scenario = qtw.QHBoxLayout()
		self.button_layout_scenario.addWidget(self.scenario_vergelijk_button)
		self.button_layout_scenario.addWidget(self.del_scenario_button)
		
		self.huis_label = qtw.QLabel('Huizen')
		self.huis_lijst = qtw.QListWidget()
		self.apparaten_label = qtw.QLabel('Apparaten')
		self.apparaten_lijst = qtw.QListWidget()
		self.isolatie_label = qtw.QLabel('Isolatie')
		self.isolatie_lijst = qtw.QListWidget()
		self.scenario_emmer_label = qtw.QLabel('Scenario emmer ')
		self.scenario_emmer_lijst = qtw.QListWidget()
		self.scenarios_label = qtw.QLabel('Scenarios')
		self.edit_label = qtw.QLabel('                                   ')
		self.scenarios_lijst = qtw.QListWidget()
		#self.scenarios_lijst.setSelectionMode(qtw.QListWidget.MultiSelection)
		
	
		## Bouw het scherm op met geneste layouts en widgets in layouts
		self.vlayout_left.addWidget(self.huis_label)
		self.vlayout_left.addWidget(self.huis_lijst)
		self.vlayout_left.addLayout(self.button_layout_huis)
		
		self.vlayout_left.addWidget(self.apparaten_label)
		self.vlayout_left.addWidget(self.apparaten_lijst)
		self.vlayout_left.addLayout(self.button_layout_app)
		
		self.vlayout_left.addWidget(self.isolatie_label)
		self.vlayout_left.addWidget(self.isolatie_lijst)
		self.vlayout_left.addLayout(self.button_layout_iso)
		
		self.vlayout_mid.addWidget(self.scenario_emmer_label)
		self.vlayout_mid.addWidget(self.scenario_emmer_lijst)
		self.vlayout_mid.addLayout(self.button_layout_emmer)
		
		self.vlayout_mid.addWidget(self.scenarios_label)
		self.vlayout_mid.addWidget(self.scenarios_lijst)
		self.vlayout_mid.addLayout(self.button_layout_scenario)
		
		self.vlayout_right.addWidget(self.edit_label)
		self.setCentralWidget(self.cwidget)
		
		### Bij Dubbelklik op lijst apparaten, huis of isolatie
		self.huis_lijst.itemDoubleClicked.connect(self.huis_2clicked)
		self.apparaten_lijst.itemDoubleClicked.connect(self.apparaat_2clicked)
		self.isolatie_lijst.itemDoubleClicked.connect(self.isolatie_2clicked)
		
		## Bi dubbelklik op scenario
		self.scenarios_lijst.itemDoubleClicked.connect(self.scenarios_2clicked)
		
		### Toon de GUI
		self.show()
	
		#################
		# The Statusbar #
		#################
		
		self.statusBar().showMessage('Bereken de duurzaamheids investeringen')
		

		###############j
		# The menubar #
		###############
		menubar = self.menuBar()
		menubar.setNativeMenuBar(False)

		# add submenus to a menu
		file_menu = menubar.addMenu('File')
		huis_menu = menubar.addMenu('Huis')
		apparaten_menu = menubar.addMenu('Apparaten')
		isolatie_menu = menubar.addMenu('Isolatie')
		scenario_menu = menubar.addMenu('Scenario')
		help_menu = menubar.addMenu('Help')
		exit_menu = menubar.addMenu('Exit')
		
		# add actions Huis
		nieuw_huis = huis_menu.addAction('Nieuw Huis',self.start_huis_wizard)
				
		# add actions Apparaten
		nieuwe_zonnepanelen = apparaten_menu.addAction('Zonnepanelen',self.start_zonnepanelen_wizard)
		nieuwe_zonneboiler = apparaten_menu.addAction('Zonneboiler',self.start_zonneboiler_wizard)
		nieuwe_warmtepomp = apparaten_menu.addAction('Warmtepomp',self.start_warmtepomp_wizard)
		nieuwe_huisbatterij = apparaten_menu.addAction('HuisBatterij',self.start_huisbatterij_wizard)
		
		# add actions Isolatie
		nieuwe_vloer = isolatie_menu.addAction('Vloer',self.start_vloerisolatie_wizard)
		nieuwe_dak = isolatie_menu.addAction('Dak',self.start_dakisolatie_wizard)
		nieuwe_spouw = isolatie_menu.addAction('Spouw',self.start_spouwisolatie_wizard)
		nieuwe_glas =isolatie_menu.addAction('Glas',self.start_glasisolatie_wizard)
		
		
		# add actions File
		open_action = file_menu.addAction('Open', self.open_from_file)
		save_action = file_menu.addAction('Save', self.save_to_file)
		
		
		# add separator
		file_menu.addSeparator()
	

	
	
	def open_from_file(self):
		with open('data_energie.json', 'r') as f:
			filedata = json.load(f)
			self.consume_file(filedata)
	
	def consume_file(self, filedata):
		h_dict = filedata['huizen']
		zb_dict = filedata['apparaten']['zonneboiler']
		zp_dict = filedata['apparaten']['zonnepanelen']
		wp_dict = filedata['apparaten']['warmtepomp']
		tb_dict = filedata['apparaten']['thuisbatterij']
		vi_dict = filedata['isolatie']['vloerisolatie']
		di_dict = filedata['isolatie']['dakisolatie']
		si_dict = filedata['isolatie']['spouwisolatie']
		gi_dict = filedata['isolatie']['glasisolatie']
		
		if len(self.huizen)==0 and len(self.apparaten)==0 and len(self.isolaties)==0:
			for huis in h_dict:
				energie_verbruik = hs.EnergieVerbruik('Verbruik', huis['gas'],huis['stroom'])
				energie_prijzen = hs.EnergiePrijs(huis['prijs_gas'],huis['prijs_stroom'],huis['prijs_gas_vast_dag'],huis['prijs_stroom_vast_dag'])
				self.voeg_huis_aan_lijst(hs.Huishouden(huis['naam'],
														huis['soort'],
														energie_verbruik,
														energie_prijzen)
														)
			for zp in zp_dict:
				self.voeg_zonnepanelen_aan_lijst(apr.Zonnepanelen(zp['naam'], 
																zp['prijs'], 
																zp['watt_pp'], 
																zp['aantal'], 
																zp['jaar_van_aanschaf'], 
																zp['schaduw_factor'])
																)
			for zb in zb_dict:
				self.voeg_zonneboiler_aan_lijst(apr.Zonneboiler(zb['naam'], 
																zb['prijs'], 
																zb['cap_kwh'],
																zb['watt'])
																)
			for wp in wp_dict:
				self.voeg_warmtepomp_aan_lijst(apr.Warmtepomp(wp['naam'], 
																wp['prijs'], 
																wp['cop'],
																wp['gbc'])
																)
			for tb in tb_dict:
				self.voeg_huisbatterij_aan_lijst(apr.Thijsbatterij(tb['naam'], 
																tb['prijs'], 
																tb['cap'])
																)
			for vi in vi_dict:
				self.voeg_vloerisolatie_aan_lijst(iso.Vloerisolatie(vi['naam'], 
																vi['prijs'], 
																vi['rd'],
																vi['m2'])
																)
			for di in di_dict:
				self.voeg_dakisolatie_aan_lijst(iso.Dakisolatie(di['naam'], 
																di['prijs'], 
																di['rd'],
																di['m2'])
																)
			for si in si_dict:
				self.voeg_spouwisolatie_aan_lijst(iso.Spouwisolatie(si['naam'], 
																si['prijs'], 
																si['rd'],
																si['m2'])
																)
			for gi in gi_dict:
				self.voeg_glasisolatie_aan_lijst(iso.Glasisolatie(si['naam'], 
																si['prijs'], 
																si['rd'],
																si['m2'])
																)
	
	def prepare_file(self):
		
		h_dict = []
		zb_dict = []
		zp_dict = []
		wp_dict = []
		tb_dict = []
		
		vi_dict = []
		di_dict = []
		si_dict = []
		gi_dict = []
		
		for item in self.huizen:
			h_dict.append(item.make_dict())
		
		huizen_dict = {'huizen': h_dict }
		
		for item in self.apparaten:
			if item.soort == 'zonneboiler':
				zb_dict.append(item.make_dict())
			if item.soort == 'zonnepanelen':
				zp_dict.append(item.make_dict())
			if item.soort == 'warmtepomp':
				wp_dict.append(item.make_dict())
			if item.soort == 'thuisbatterij':
				tb_dict.append(item.make_dict())
		
		zb_dict = {'zonneboiler' : zb_dict }
		zp_dict = {'zonnepanelen' : zp_dict }
		wp_dict = {'warmtepomp' : wp_dict }
		tb_dict = {'thuisbatterij' : tb_dict }
		
		apparaten_union = zb_dict | zp_dict | wp_dict | tb_dict
		apparaten_dict = { 'apparaten' : apparaten_union }
		
		for item in self.isolaties:
			
			if item.soort == 'vloerisolatie':
				vi_dict.append(item.make_dict())
			if item.soort =='dakisolatie':
				di_dict.append(item.make_dict()) 
			if item.soort =='spouwisolatie':
				si_dict.append(item.make_dict()) 
			if item.soort =='glasisolatie':
				gi_dict.append(item.make_dict())
		
		vi_dict = {'vloerisolatie' : vi_dict }
		di_dict = {'dakisolatie' : di_dict }
		si_dict = {'spouwisolatie' : si_dict }
		gi_dict = {'glasisolatie' : gi_dict }
		
		isolatie_union = vi_dict | di_dict | si_dict | gi_dict
		isolatie_dict = { 'isolatie' : isolatie_union }
		
		file_dict = huizen_dict | apparaten_dict | isolatie_dict
		
		return file_dict
	
	def save_to_file(self):
		
		data_dict = self.prepare_file()
		
		with open('data_energie.json', 'w') as f:
			json.dump(data_dict, f)
	
	def start_plafond_wizard(self):
		self.plafond_wizard = MijnPlafondWizard()
		self.plafond_wizard.show()
		self.plafond.submitted.connect(self.voeg_plafond_aan_lijst)
			
	def start_huis_wizard(self):
		self.huis_wizard = MijnHuisWizard()
		self.huis_wizard.show()
		self.huis_wizard.submitted.connect(self.voeg_huis_aan_lijst)
		
	def start_zonnepanelen_wizard(self):
		self.zonnepanelen_wizard = MijnZonnepanelenWizard()
		self.zonnepanelen_wizard.show()
		self.zonnepanelen_wizard.submitted.connect(self.voeg_zonnepanelen_aan_lijst)
	
	def start_zonneboiler_wizard(self):
		self.zonneboiler_wizard = MijnZonneboilerWizard()
		self.zonneboiler_wizard.show()
		self.zonneboiler_wizard.submitted.connect(self.voeg_zonneboiler_aan_lijst)
	
	def start_warmtepomp_wizard(self):
		self.warmtepomp_wizard = MijnWarmtepompWizard()
		self.warmtepomp_wizard.show()
		self.warmtepomp_wizard.submitted.connect(self.voeg_warmtepomp_aan_lijst)
		
	def start_huisbatterij_wizard(self):
		self.huisbatterij_wizard = MijnHuisbatterijWizard()
		self.huisbatterij_wizard.show()
		self.huisbatterij_wizard.submitted.connect(self.voeg_huisbatterij_aan_lijst)
	
	def start_vloerisolatie_wizard(self):
		self.vloerisolatie_wizard = MijnVloerisolatieWizard()
		self.vloerisolatie_wizard.show()
		self.vloerisolatie_wizard.submitted.connect(self.voeg_vloerisolatie_aan_lijst)
		
	def start_dakisolatie_wizard(self):
		self.dakisolatie_wizard = MijnDakisolatieWizard()
		self.dakisolatie_wizard.show()
		self.dakisolatie_wizard.submitted.connect(self.voeg_dakisolatie_aan_lijst)
	
	def start_spouwisolatie_wizard(self):
		self.spouwisolatie_wizard = MijnSpouwisolatieWizard()
		self.spouwisolatie_wizard.show()
		self.spouwisolatie_wizard.submitted.connect(self.voeg_spouwisolatie_aan_lijst)
	
	def start_glasisolatie_wizard(self):
		self.glasisolatie_wizard = MijnGlasisolatieWizard()
		self.glasisolatie_wizard.show()
		self.glasisolatie_wizard.submitted.connect(self.voeg_glasisolatie_aan_lijst)
	
	def voeg_huis_aan_lijst(self, huis):
		self.huizen.append(huis)
		self.huis_lijst.addItems([huis.naam])		
		
	def voeg_zonnepanelen_aan_lijst(self, zonnepanelen):
		self.apparaten.append(zonnepanelen)
		naam = zonnepanelen.naam + ',' + zonnepanelen.soort
		self.apparaten_lijst.addItems([naam])	
	
	def voeg_zonneboiler_aan_lijst(self, zonneboiler):
		self.apparaten.append(zonneboiler)
		naam = zonneboiler.naam + ',' + zonneboiler.soort
		self.apparaten_lijst.addItems([naam])	
	
	def voeg_warmtepomp_aan_lijst(self, warmtepomp):
		self.apparaten.append(warmtepomp)
		naam = warmtepomp.naam + ',' + warmtepomp.soort
		self.apparaten_lijst.addItems([naam])
	
	
	def voeg_vloerisolatie_aan_lijst(self, vloerisolatie):
		self.isolaties.append(vloerisolatie)
		naam = vloerisolatie.naam + ',' + vloerisolatie.soort
		self.isolatie_lijst.addItems([naam])
	
	def voeg_dakisolatie_aan_lijst(self, dakisolatie):
		self.isolaties.append(dakisolatie)
		naam = dakisolatie.naam + ',' + dakisolatie.soort
		self.isolatie_lijst.addItems([naam])
	
	def voeg_spouwisolatie_aan_lijst(self, spouwisolatie):
		self.isolaties.append(spouwisolatie)
		naam = spouwisolatie.naam + ',' + spouwisolatie.soort
		self.isolatie_lijst.addItems([naam])

	def voeg_glasisolatie_aan_lijst(self, glasisolatie):
		self.isolaties.append(glasisolatie)
		naam = glasisolatie.naam + ',' + glasisolatie.soort
		self.isolatie_lijst.addItems([naam])
		
	def voeg_pscenario_aan_lijst(self, pscenario):
		self.scenarios.append(pscenario)
		self.scenarios_lijst.addItems([pscenario.naam])
	
	def huis_clicked(self, item):
		for h in self.huizen:
			if h.naam == item.text():
				print(h)
				
	def huis_2clicked(self, item):
		for huis in self.huizen:
			if huis.naam == item.text() and huis not in self.scenario_emmer:
				self.scenario_emmer_lijst.addItems([item.text()])
				self.scenario_emmer.append(huis)
	
	def isolatie_2clicked(self, item):
		txt = item.text()
		txt_l = txt.split(',')
		for isolatie in self.isolaties:
			if isolatie.naam == txt_l[0] and isolatie not in self.scenario_emmer:
				self.scenario_emmer_lijst.addItems([item.text()])
				self.scenario_emmer.append(isolatie)
	
	def apparaat_2clicked(self, item):
		txt = item.text()
		txt_l = txt.split(',')
		for apparaat in self.apparaten:
			if apparaat.naam == txt_l[0] and apparaat not in self.scenario_emmer:
				self.scenario_emmer_lijst.addItems([item.text()])
				self.scenario_emmer.append(apparaat)

				
	def bereken_scenario_van_emmer(self):
	
		text, ok = qtw.QInputDialog.getText(self, 'Scenario Naam', 'Naam van scenario:')
		if ok:
			naam = text
				
		iso_lijst = []
		app_lijst = []
		
		for item in self.scenario_emmer:
			if item.soort == 'zonneboiler' or item.soort == 'zonnepanelen' or item.soort == 'warmtepomp' or item.soort == 'thuisbatterij':
				app_lijst.append(item)
			if item.soort == 'vloerisolatie' or item.soort == 'dakisolatie' or item.soort == 'spouwisolatie' or item.soort == 'glasisolatie':
				iso_lijst.append(item)
				
		for huis in self.scenario_emmer:
			if type(huis) == hs.Huishouden: 
				scenario = sc.ScenarioZonderPlafond(naam,iso_lijst, app_lijst, huis)
				self.scenarios_lijst.addItems([scenario.naam])
				self.scenarios.append(scenario)
		
	
	def scenarios_2clicked(self,item):
		
		for scenario in self.scenarios:
			if scenario.naam == item.text():
				self.scenario_widget = ScenarioWidget(scenario)
				self.scenario_widget.submitted.connect(self.voeg_pscenario_aan_lijst)
				self.scenario_widget.show()
	
	
	def edit_huis(self):
		huis_l  = self.huis_lijst.selectedItems()
		
		if len(self.huizen) >0 and len(huis_l) >0: 
			for huis in self.huizen:
				if huis_l[0].text() == huis.naam:
					self.edit_huis_widget = EditHuisWidget(huis)
					self.vlayout_right.addWidget(self.edit_huis_widget)
					
	def del_huis(self):
		huis_l  = self.huis_lijst.selectedItems()
		
		row=0
		if len(self.huizen) >0 and len(huis_l) >0: 
			for huis in self.huizen:			
				if huis_l[0].text() == huis.naam:
				
					self.huizen.remove(huis)
					self.huis_lijst.takeItem(row)
				row+=1
	
	def edit_app(self):
		app_l  = self.apparaten_lijst.selectedItems()
		txt = app_l[0].text()
		txt_l = txt.split(',')	
		
		if len(self.apparaten) >0 and len(app_l) >0: 
			for apparaat in self.apparaten:
				
				if txt_l[0] == apparaat.naam:
					edit_widget = EditWidget(apparaat)
					self.vlayout_right.addWidget(	edit_widget)
					
	def del_app(self):
		app_l  = self.apparaten_lijst.selectedItems()
		txt = app_l[0].text()
		txt_l = txt.split(',')	
		
		row=0
		if len(self.apparaten) >0 and len(app_l) >0: 
			for apparaat in self.apparaten:	
				if txt_l[0] == apparaat.naam:
					self.apparaten.remove(apparaat)
					self.apparaten_lijst.takeItem(row)
				row+=1
	
	def edit_iso(self):
		iso_l  = self.isolatie_lijst.selectedItems()
		txt = iso_l[0].text()
		txt_l = txt.split(',')	
		
		if len(self.isolaties) >0 and len(iso_l) >0: 
			for isolatie in self.isolaties:
				
				if txt_l[0] == isolatie.naam:
					edit_widget = EditWidget(isolatie)
					self.vlayout_right.addWidget(edit_widget)
					
	def del_iso(self):
		app_l  = self.isolatie_lijst.selectedItems()
		txt = app_l[0].text()
		txt_l = txt.split(',')	
		
		row=0
		if len(self.isolaties) >0 and len(app_l) >0: 
			for isolatie in self.isolaties:	
				if txt_l[0] == isolatie.naam:
					self.isolaties.remove(isolatie)
					self.isolatie_lijst.takeItem(row)
				row+=1
	
	def del_emmer(self):
		emmer_l  = self.scenario_emmer_lijst.selectedItems()
		txt = emmer_l[0].text()
		txt_l = txt.split(',')	
		
		row=0
		if len(self.scenario_emmer) >0 and len(emmer_l) >0: 
			for maatregel in self.scenario_emmer:	
				if txt_l[0] == maatregel.naam:
					self.scenario_emmer.remove(maatregel)
					self.scenario_emmer_lijst.takeItem(row)
				row+=1
	
	def del_scenario(self):
		scenario_l  = self.scenarios_lijst.selectedItems()
	
		row=0
		if len(self.scenarios) >0 and len(scenario_l) >0: 
			for scenario in self.scenarios:	
				if scenario_l[0].text() == scenario.naam:
					self.scenarios.remove(scenario)
					self.scenarios_lijst.takeItem(row)
				row+=1
	
	
	def vergelijk_scenarios(self):
		self.selecteer_scenarios_widget = SelecteerScenariosWidget(self.scenarios)
		self.selecteer_scenarios_widget.show()

	
##############################################
	

		
if __name__ == '__main__':
	
	app = qtw.QApplication(sys.argv)
	
	
	
	mw = MainWindow()
	
			
	
	
	sys.exit(app.exec_())