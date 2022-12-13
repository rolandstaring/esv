
class GlobalSupport:
	
	def max_len_label(self,labels_list):
		l = []
		for label in labels_list:
			l.append(len(label))
		return max(l)
	
	
	def print_html_tabbed_sum_list(self,header, labels_list, vars_list, line_nr):
		
		
		if len(labels_list) != len(vars_list):
			return 'Unequal length of vars'
			
	
		lab_var_tuple = tuple(zip(labels_list, vars_list))
		
		html_str = f"<p><b>{header}</b></p>"
		html_str += f"<table>"
		
		streep = 10*'-'
		
		i = 0
		for t in lab_var_tuple:
			i += 1
			if i == line_nr:
				html_str += f"<tr><td></td><td>{streep}</td></tr>"
			html_str+= f"<tr><td>{t[0]}</td><td align='right'>{t[1]} €</td></tr>"
			
		
		html_str += f"</table>"
		
		return html_str
		
		
