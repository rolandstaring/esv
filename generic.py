
class Color:
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


class Global:
	DIRECT_VERBRUIK_PERC = 0.2
	KWH_1M3_GAS = 10
		
class Formula:
	
	def max_len_label(labels_list):
		l = []
		for label in labels_list:
			l.append(len(label))
		return max(l)
	
	def print_html_formula(labels_list, values_list, mp_str):
		html = f"<p><table>"
		html += f"<tr><th>-------------------------------</th><th></th><th></th></tr>"
		out_l = values_list.copy()
		outcome = out_l.pop(0)
		
		if mp_str == '+':
			for i in out_l:
				outcome += i
		elif mp_str == '-':
			for i in out_l:
				outcome -= i
		elif mp_str == '*':
			for i in out_l:
				outcome *= i
		else:
			return 'Error'
							
		for label,value in zip(labels_list, values_list):
			html += f"<tr><td>{label}</td><td align='right'>{str(value)}</td><td></td></tr>"
		lijn_str= 6*'-'+'\n'
		html += f"<tr><td></td><td align='right'>{lijn_str}</td> <td>{mp_str}</td></tr>"
		html += f"<tr><td></td><td align='right'>{str(round(outcome))}</td><td></td></tr>"
		html += f"</table></p>"
	
		return html