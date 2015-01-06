import json
class Worksheet:
	name = ""
	def __init__(self, filename):
		self.name = filename
		self.problems = []#list of questions
wk1 = Worksheet("testworksheet")
with open("worksheet.json","w") as outfile:
	json.dump(wk1.__dict__,outfile)	
class Question:
	genDescrip: ""
	content: []#list of sections, text, and images
	wks.questions.append(Q);#?
class Section:
	content: []#list of text,images,dropdown,table
class Table:
	header: ""
	rows: []#list of lists ; one list per row inside the row: strings and dropdowns
class Dropdown:
	options: []
	correct: ""