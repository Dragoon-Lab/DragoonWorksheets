import json
# Classes
class Workbook:
# Objects of every other class will ultimately be appended to one of the lists in a workbook object. This is what gets converted into the HTML workbook.
	def __init__(self,filename):
		self.name = filename
		# This will be the name of the HTML file.
		self.questions = []
		self.loose = []
	def jsonable(self):
		return self.__dict__
	def from_dict(dct):
	#This constructor converts a dict to a instance of this class. Used to load objects from jsons.
		wks = Workbook(dct['name'])
		wks.questions = list(map(CustomTypeDecoder,dct['questions'])) # for each item, decode it
		wks.loose = list(map(CustomTypeDecoder,dct['loose']))
		return wks
		
class LsText:
#This class is for text that is not part of any particular question.
	def __init__(self,wkst):
		if isinstance(wkst,Workbook):
		#If the parts of this question are not already defined, ask for them.
			self.before = input ("Before Question ")
			self.text = input ("Text: ")
			wkst.loose.append(self)
		else:
		#If the parts of this question are already defined, don't ask for them again.
			self.before = wkst
			self.text = ""
	def from_dict(dct):
	#This constructor converts a dict to a instance of this class. Used to load objects from jsons.
		ltx = LsText(dct['before'])
		ltx.text = dct['text']
		return ltx
		
class LsImage:
#This class is for images that are not part of any particualr question.
	def __init__(self,wkst):
		if isinstance(wkst,Workbook):
		#If the parts of this image are not already defined, ask for them.
			self.before = input ("Before Question ")
			self.img = input ("File/Folder name: ")
			wkst.loose.append(self)
		else:
		#If the parts of this question are not already defined, don't ask for them again.
			self.before = wkst
			self.img = ""
	def from_dict(dct):
	#This constructor converts a dict to a instance of this class. Used to load objects from jsons.
		lig = LsText(dct['before'])
		lig.img = dct['img']
		return lig
		
class Question:
#This is the main way that the workbooks are broken up; a student cannot move to the next question without finishing the current one. Questions contain lists of sections.
	def __init__ (self,initializer):
		if isinstance(initializer,Workbook):
		#If the parts of this question are not already defined, ask for them.
			self.sub = input ("Subheading: ")
			# This will be placed in <h3> tags.
			self.sections = []
			initializer.questions.append(self)
		elif isinstance(initializer,str):
		#If the parts of this question are already defined, don't ask for them again.
			self.sub = initializer
			self.sections = []
		else:
			raise Exception("Bad initializer to question")
	def from_dict(dct):
	#This constructor converts a dict to a instance of this class. Used to load objects from jsons.
		qes = Question(dct['sub'])
		qes.sections = list(map(CustomTypeDecoder,dct['sections']))
		return qes
		
class Section:
#Every section starts on a new line. Sections contain Dragoon problems, tables, dropdown boxes, large textboxes, text, images, and checkboxes.
	def __init__ (self,qstn):
		if isinstance(qstn,Question):
		#If the parts of this section are not already defined, ask for them.
			self.content = []
			qstn.sections.append(self)
		else:
		#If the parts of this section are already defined, don't ask for them again.
			self.content = qstn
	def from_dict(dct):
	#This constructor converts a dict to a instance of this class. Used to load objects from jsons.
		sct = Section(list(map(CustomTypeDecoder,dct['content'])))
		return sct
		
class Dragoon:
#A Dragoon object contains the problem name and mode of the Dragoon problem to be inserted.
	def __init__ (self,sect):
		if isinstance(sect,Section):
		#If the parts of this Dragoon problem have not already been defined, ask for them.
			self.problem = input ("Problem: ")
			self.mode = input ("Mode: ").upper()
			sect.content.append(self)
		else:
		#If the parts of this Dragoon problem have already been defined, don't ask for them again.
			self.problem = sect
			self.mode = ""
	def from_dict(dct):
	#This constructor converts a dict to a instance of this class. Used to load objects from jsons.
		drg = Dragoon(dct['problem'])
		drg.mode = dct['mode']
		return drg
		
class Table:
#A table object has a header and lists of rows, which are themselves lists of content for each cell, some of which contain dropdown boxes.
	def __init__(self,sect):
		if isinstance(sect,Section):
		#If the parts of this table have not already been defined, ask for them.
			self.header = input ("Header: ").split(",")
			self.rows = []
			line = input ("Line: ").split(",")
			while not "end" in line:
			#If the author enters, "end" as one of the cells in a line, the program will stop asking for lines.
				line2 = []
				for cell in line:
					if cell == "dropdown":
					#If the author enters, "dropdown" as one of the cells in a line, the program will ask the author for content to put in that cell.
						cell = input ("Cell: ").split(",")
						for element in cell:
							indx = cell.index(element)
							if element == "dropdown":
							#If the author enters, "dropdown" as one of the elements in a cell, the program will set up that piece as a dropbox and ask for all possible answers and the correct answer.
								element = []
								options = input ("Answers: ").split(",")
								correct = input ("Right answer: ")
								if not correct in options:
								#If the right answer is not in the list of possible answers, the program asks the author for one that is in that list.
									print("Please choose one of the given answers as the right answer.")
									correct = input ("Right answer: ")
								element.append(options)
								element.append(correct)
								cell[indx] = element
					line2.append(cell)	
				self.rows.append(line2)
				line = input ("Line: ").split(",")
			sect.content.append(self)
		else:
		#If the parts of this table have already been defined, don't ask for them again.
			self.header = sect
			self.rows = []
	def from_dict(dct):
	#This constructor converts a dict to a instance of this class. Used to load objects from jsons.
		tbl = Table(dct['header'])
		tbl.rows = list(map(Table.decodeRow,dct['rows']))
		return tbl
	def decodeRow(row):
	#This function works with from_dict specifically to load the rows.
		return list(map(CustomTypeDecoder,row))

class Dropdown:
	def __init__(self,sect):
		if isinstance (sect,Section):
		#If the parts of this dropdown box have not already been defined, ask for them.
			self.options = input ("Answers: ").split(",")
			self.correct = input ("Right answer: ")
			if not self.correct in self.options:
				print("Please choose one of the given answers as the right answer.")
				self.correct = input ("Right answer: ")
			sect.content.append(self)
		else:
		#If the parts of this dropdown box have already been defined, don't ask for them again.
			self.options = []
			self.correct = sect
	def from_dict(dct):
	#This constructor converts a dict to a instance of this class. Used to load objects from jsons.
		drp = Dropdown(dct['correct'])
		drp.options = list(map(CustomTypeDecoder,dct['options']))
		return drp

class Textbox:
	def __init__(self,sect):
		if isinstance (sect,Section):
		#If the parts of this text box have not already been defined, ask for them.
			self.example = input ("Example right answer: ")
			sect.content.append(self)
		else:
		#If the parts of this text box have already been defined, don't ask for them again.
			self.example = sect
	def from_dict(dct):
	#This constructor converts a dict to a instance of this class. Used to load objects from jsons.
		box = Textbox(dct['example'])
		return box
		
class Text:
	def __init__ (self,sect):
		if isinstance (sect,Section):
		#If the parts of this section of text have not already been defined, ask for them.
			self.text = input ("Text: ")
			sect.content.append(self)
		else:
		#If the parts of this section of text have already been defined, don't ask for them again.
			self.text = sect
	def from_dict(dct):
	#This constructor converts a dict to a instance of this class. Used to load objects from jsons.
		stx = Text(dct['text'])
		return stx

class Image:
	def __init__ (self,sect):
		if isinstance (sect,Section):
		#If the parts of this image have not already been defined, ask for them.
			self.image = input ("Folder/file name: ")
			sect.content.append(self)
		else:
		#If the parts of this image have already been defined, don't ask for them again.
			self.image = sect
	def from_dict(dct):
	#This constructor converts a dict to a instance of this class. Used to load objects from jsons.
		sig = Image(dct['image'])
		return sig
		
class Checkbox:
	def __init__(self,sect):
		if isinstance (sect,Section):
		#If the parts of this checkbox have not already been defined, ask for them.
			self.options_c = input ("Answers: ").split(",")
			self.correct_c = input ("Right answers: ").split(",")
			for item in self.correct_c:
				if not item in self.options_c:
					print("Please choose the right answers from the list of possible answers you have already entered.")
					self.correct = input ("Right answers: ").split(",")
			sect.content.append(self)
		else:
		#If the parts of this checkbox have already been defined, don't ask for them again.
			self.options_c = []
			self.correct_c = sect
	def from_dict(dct):
	#This constructor converts a dict to a instance of this class. Used to load objects from jsons.
		chk = Checkbox(dct['correct_c'])
		chk.options_c = list(map(CustomTypeDecoder,dct['options_c']))
		return chk
		
TYPES = { 'Workbook': Workbook,
		  'LsText': LsText,
		  'LsImage': LsImage,
          'Question': Question,
		  'Dragoon': Dragoon,
		  'Section': Section,
		  'Table': Table,
		  'Dropdown': Dropdown,
		  'Textbox': Textbox,
		  'Checkbox': Checkbox,
		  'Text': Text,
		  'Image': Image
		  }


class CustomTypeEncoder(json.JSONEncoder):
	"""A custom JSONEncoder class that knows how to encode core custom
    objects.

    Custom objects are encoded as JSON object literals (ie, dicts) with
    one key, '__TypeName__' where 'TypeName' is the actual name of the
    type to which the object belongs.  That single key maps to another
    object literal which is just the __dict__ of the object encoded."""

	def default(self, obj):
		if isinstance(obj, tuple(TYPES.values())):
			key = '__%s__' % obj.__class__.__name__
			return { key: obj.__dict__ }
			return json.JSONEncoder.default(self, obj)


def CustomTypeDecoder(dct):
#This function is called whenever the loadWorkbook function is called. It converts the JSON file back into an object that Python can use.
	if type(dct) is dict and len(dct) == 1:
	#If the decoder encounters a dictionary, list its contents.
		type_name, value = list(dct.items())[0]
		type_name = type_name.strip('_')
		if type_name in TYPES:
		#Return the class of the object if the class is listed under "TYPES" in lines 238-249.
			return TYPES[type_name].from_dict(value)
	return dct

######################
# Generator functions

def generateHTMLWorkbook(wks):
	# Converts Workbook object, "wks" into an html/javascript file
	workbook = "<!DOCTYPE html>\n<html>\n<head>\n<title>Dragoon Workbook</title>\n<script type=\"text/javascript\">\nfunction\nopenDragoonProblem(num){\nvar u = document.getElementById(\"user\").value;\nvar s;\nif ((window.location.href.search(\"s=\") != -1)) {\ns = window.location.href.substr(window.location.href.search(\"s=\")+2)\n} else {\ns = document.getElementById(\"section\").value;\n};\nvar problemID = \"problem\" + num.toString();\nvar p = document.getElementById(problemID).value;\nvar modeID = \"mode\" + num.toString();\nvar m = document.getElementById(modeID).value;\nvar urlString = \"http://dragoon.asu.edu/demo/index.html?u=\"+u+\"&m=\"+m+\"&p=\"+p+\"&s=\"+s;\nwindow.open(urlString);\n}\nfunction checkAnswers(inputId, rightAnswer)\n{\nif(document.getElementById(inputId).value===rightAnswer) {\ndocument.getElementById(inputId).style.background=\"#66FF33\";\nreturn true;\n}\nelse\n{\ndocument.getElementById(inputId).style.background=\"#FF3333\";\nreturn false;\n}\n};\nfunction checkTextbox(inputId) {\nif (!(document.getElementById(inputId).value===\"\")) {\ndocument.getElementById(inputId).style.background=\"#66FF33\";\nreturn true;\n}\nelse {\ndocument.getElementById(inputId).style.background=\"#FF3333\";\nreturn false;\n}\n};\n\nfunction checkbox(textId,checkedId,uncheckedId) {\nck = 0\nunck = 0\nfor (i = 0; i<checkedId.length; i++) {\nif (document.getElementById(checkedId[i]).checked) {\nck = ck + 1;\n}\n};\nfor (i = 0; i<uncheckedId.length; i++) {\nif (!(document.getElementById(uncheckedId[i]).checked)) {\nunck = unck + 1;\n}\n};\nif (checkedId.length == ck && uncheckedId.length == unck)\n{\ndocument.getElementById(textId).style.background=\"#66FF33\";\nreturn true\n}\nelse {\ndocument.getElementById(textId).style.background=\"#FF3333\";\nreturn false\n}\n};\n\nfunction checkboxCorrection(textId,checkedId,uncheckedId) {\nfor (i=0; i<checkedId.length; i++) {\ndocument.getElementById(checkedId[i]).checked = true;\n};\nfor (i=0; i<uncheckedId.length; i++) {\ndocument.getElementById(uncheckedId[i]).checked = false;\n};\ndocument.getElementById(textId).style.background = \"#FFFF00\"\n};\n\nfunction retrieveCheckboxValue(total) {\nresponse = []\nfor (i=0; i<total.length; i++) {\nif\n(document.getElementById (total[i]).checked) {\nresponse.push(total[i])\n}\n};\nreturn response\n};\n\nvar tim1 = 0;\nfunction time1 () {\nif (yestim1=1){\ntim1 = tim1 + 1;\nt = setTimeout(function() {time1()},1000);\n}\n};\nvar yestim1 = 1;\ntime1();\nfunction checkCompletion(num){\n// id is the id of the continue button or I just need a the number of the question i.e. if its cont1 just send me 1 and it will do\nvar u = document.getElementById(\"user\").value;\nvar s = document.getElementById(\"section\").value;\nvar problemID = \"problem\" + num.toString();\nvar p = document.getElementById(problemID).value.slice(0,30);\nvar modeID = \"mode\" + num.toString();\nvar m = document.getElementById(modeID).value;\nvar xmlHTTP = new XMLHttpRequest();\nvar userObject;\nxmlHTTP.onreadystatechange = function(){\nif(xmlHTTP.readyState == 4 && xmlHTTP.status == 200){\nuserObject = JSON.parse(xmlHTTP.responseText);\n}\n}\nvar url = \"../../demo/log/dashboard_js.php?m=\"+m+\"&u=\"+u+\"&s=\"+s+\"&p=\"+p;\n//var url = \"log/dashboard_js.php?m=\"+m+\"&u=\"+u+\"&s=\"+s+\"&p=\"+p;\nxmlHTTP.open(\"GET\", url, false);\nxmlHTTP.send();\nvar id = \"dragoonErrorMessage\" + num.toString();\nvar result = false;\n if(userObject != null){\nresult = userObject[0].problemComplete;\n}\nif(result) {\ndocument.getElementById(id).style.display = \"none\";\n} else {\ndocument.getElementById(id).style.display = \"\";\n}\nreturn result;\n}</script>\n</head>\n<body>\n<label>Username :</label>&nbsp;<input type=\"text\" name=\"user\" id=\"user\">\n<input type=\"hidden\" name=\"section\" id=\"section\" value=\"public-workbook\">\n<br><br><button id=\"usernameCheck\" onClick=\"enterUsername();\">Start Workbook</button><div id=\"wkstBody\" style=\"display: none\">\n<script type=\"text/javascript\">\nif ((window.location.href.search(\"u=\") != -1)) {\nif ((window.location.href.search(\"s=\") != -1)&&(window.location.href.search(\"s=\")>window.location.href.search(\"u=\"))) {\ndocument.getElementById(\"user\").value = window.location.href.substr((window.location.href.search(\"u=\")+2),((window.location.href.search(\"&s=\"))-(window.location.href.search(\"u=\")+2)));\ndocument.getElementById(\"section\").value = window.location.href.substr(window.location.href.search(\"s=\")+2);\n} else {\ndocument.getElementById(\"user\").value = window.location.href.substr(window.location.href.search(\"u=\")+2);\ndocument.getElementById(\"section\").value = window.location.href.substr((window.location.href.search(\"s=\")+2),((window.location.href.search(\"&u=\"))-(window.location.href.search(\"s=\")+2)));\n};\ndocument.getElementById(\"wkstBody\").style.display=\"\";\ndocument.getElementById(\"usernameCheck\").style.display=\"none\";\ndocument.getElementById(\"user\").disabled=true;\n};\nfunction enterUsername() {\nif (document.getElementById(\"user\").value!==\"\" && document.getElementById(\"user\").value.length<=30) {\ndocument.getElementById(\"wkstBody\").style.display=\"\";document.getElementById(\"usernameCheck\").style.display=\"none\";\ndocument.getElementById(\"user\").style.background=\"\";\ndocument.getElementById(\"user\").disabled=true;\n}\nelse {\ndocument.getElementById(\"user\").style.background=\"#FF3333\";alert(\"Please make sure you have entered a username and that your username is between 1 and 30 characters long.\");\n}\n};\n</script>" # This contains everything that comes before the first question or piece of loose content, including the username box and several function definitions.
	divset = "\n</div>"
	endtbl = "<div id=\"resultsTable\" style=\"display:none\">\n<table>\n<thead>\n<td style=\"border: 2pt black solid\">Question</td>\n<td style=\"border: 2pt black solid\">Correct Answer</td>\n<td style=\"border: 2pt black solid\">Student Answers</td>\n<td style=\"border: 2pt black solid\">Number of Wrong Tries</td>\n<td style=\"border: 2pt black solid\">Time for Entire Question (s)</td>\n</thead>\n<tbody>"
	endfn = "<script type=\"text/javascript\">\nfunction displayAnswers () {\ndocument.getElementById(\"resultsTable\").style.display=\"\""
	alph = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
	rnum = ["i","ii","iii","iv","v","vi","vii","viii","ix","x","xi","xii","xiii","xiv","xv","xvi","xvii","xviii","xix","xx","xxi","xxii","xxiii","xxiv","xxv"]
	docname = wks.name + ".html"
	qno = 0
	for ques in wks.questions:
	#This separates the individual questions from each other.
		dragoon_link = ""
		qno = str(int(qno) + 1)
		for lse in wks.loose:
		#This separates out the loose content.
			if int(qno) == int(lse.before):
			#This prints the loose content before a given question if that question's number is listed as its "before" value.
				if lse.__class__.__name__ == "LsImage": #This prints the loose content as a picture if it is of the class "LsImage".
					workbook = workbook + "\n</p><img src =\"" + lse.img + ".JPG\"/><p>"
				else:
				#This prints the loose content as text if it is not of the class "LsImage", i.e., if it is of the class "LsText".
					workbook = workbook + "\n<p>" + lse.text + "</p>"
		contfn = "function cont" + qno + "() {\nvar yestim" + qno + " = 0;"
		chkans = ""
		chkcpl = "if ("
		contif = "if ("
		disabl = ""
		ctwrng = ""
		ctr = ""
		varset = "var set" + str(qno) + " = {"
		workbook = workbook + "\n<h3>" + ques.sub + "</h3>"
		alphindex = 0
		for sect in ques.sections:
		#This separates the sections in a given question from each other.
			lno = alph[alphindex]
			alphindex = alphindex + 1
			romannum = 0
			for part in sect.content:
			#This separates the parts in a given section from each other.
				if part.__class__.__name__ == "Dragoon":
				#If the part is a Dragoon problem, this formats it as such.
					workbook = workbook + "</p>\n<input type=\"hidden\" name=\"problem" + qno + "\" id=\"problem" + qno + "\" value=\"" + part.problem + "\">\n<input type=\"hidden\" name=\"mode" + qno + "\" id=\"mode" + qno + "\" value=\"" + part.mode + "\">\n<br><button id=\"dragoonButton" + qno + "\" onClick=\"openDragoonProblem(" + qno + ");\">Open Dragoon</button>\n<div id=\"dragoonErrorMessage" + qno + "\" style=\"color:red;display:none\"><p>Your Dragoon problem is incomplete!  Please make sure your nodes are finished (i.e. have solid borders) and that you can view the model's graph and table of values.</p></div><p>"
					contif = contif + "checkCompletion(" + qno + ") && "
				elif part.__class__.__name__ == "Dropdown":
				#If the part is a dropdown box, this formats it as such.
					rno = rnum[romannum]
					romannum = romannum + 1
					allans = ""
					for item in part.options:
					#This places all of the listed options between <option> tags.
						item = "\n<option>" + str(item) + "</option>"
						allans = allans + item
					varset = varset + "\n" + lno + rno + ":0,"
					chkans = chkans + "\ncheckAnswers(\"" + qno + lno + rno + "\", \"" + part.correct + "\");"
					chkcpl = chkcpl + "document.getElementById(\"" + qno + lno + rno + "\").value===\"\" || "
					ctr = ctr + "if (!checkAnswers(\"" + qno + lno + rno + "\", \"" + part.correct + "\")) { \n set" + qno + "." + lno + rno + " = set" + qno + "." + lno + rno + " + 1;}"
					contif = contif + "(checkAnswers(\"" + qno + lno + rno + "\", \"" + part.correct + "\") || set" + qno + "." + lno + rno + "===3) &&"
					ctwrng = ctwrng + "\nif (!checkAnswers(\"" + qno + lno + rno + "\", \"" + part.correct + "\")) {\nif (set" + qno + "." + lno + rno + "===3) {\ndocument.getElementById(\"" + qno + lno + rno + "\").style.background=\"#FFFF00\";\n document.getElementById(\"" + qno + lno + rno + "Answer3\").innerHTML = document.getElementById(\"" + qno + lno + rno + "\").value \n }\nif (set" + qno + "." + lno + rno + "=== 1) { \n document.getElementById(\"" + qno + lno + rno + "Answer1\").innerHTML = \"; \" + document.getElementById(\"" + qno + lno + rno + "\").value \n } \n else if (set" + qno + "." + lno + rno + "=== 2) { \n document.getElementById(\"" + qno + lno + rno + "Answer2\").innerHTML = \"; \" + document.getElementById(\"" + qno + lno + rno + "\").value \n } \n else { \n document.getElementById(\"" + qno + lno + rno + "Answer3\").innerHTML = \"; \" + document.getElementById(\"" + qno + lno + rno + "\").value \n } \n } \n else { \n if (set" + qno + "." + lno + rno + "=== 0) { \n document.getElementById(\"" + qno + lno + rno + "Answer1\").innerHTML = \"; \" + document.getElementById(\"" + qno + lno + rno + "\").value \n } \n else if (set" + qno + "." + lno + rno + "=== 1) { \n document.getElementById(\"" + qno + lno + rno + "Answer2\").innerHTML = \"; \" + document.getElementById(\"" + qno + lno + rno + "\").value \n } \n else { \n document.getElementById(\"" + qno + lno + rno + "Answer3\").innerHTML = \"; \" + document.getElementById(\"" + qno + lno + rno + "\").value\n}\n};\nif(set" + qno + "." + lno + rno + "===3)\n{document.getElementById(\"" + qno + lno + rno + "\").value=\"" + part.correct + "\"};"
					workbook = workbook + "<select id=\"" + qno + lno + rno + "\">\n<option></option>" + allans + "</select>"
					endtbl = endtbl + "\n<tr>\n<td style=\"border: 2pt black solid\">" + qno + lno + ". " + rno + ".</td>\n<td style=\"border: 2pt black solid\">" + part.correct + "</td>\n<td style=\"border: 2pt black solid\"><div id=\"" + qno + lno + rno + "Answer1\"></div><div id=\"" + qno + lno + rno + "Answer2\"></div><div id=\"" + qno + lno + rno + "Answer3\"></div></td>\n<td style=\"border: 2pt black solid\"><div id=\"" + qno + lno + rno + "Tries\"></div></td>\n<td style=\"border: 2pt black solid\">"
					disabl = disabl + "\ndocument.getElementById(\""+ qno + lno + rno +"\").disabled=true;"
					if lno == "a" and rno == "i":
					#If this is the first part of the first section of a question, its row in the results table will display the time the number of seconds the student took for the whole question.
						endtbl = endtbl + "<div id=\"" + qno + "Time\"></div></td>\n<tr>"
						contfn = contfn + "\ndocument.getElementById(\"" + qno + "Time\").innerHTML = tim" + qno + ";"
					else:
						endtbl = endtbl + "</td>\n</tr>"
					endfn = endfn + "\ndocument.getElementById(\"" + qno + lno + rno + "Tries\").innerHTML=set" + qno + "." + lno + rno + ";"
				elif part.__class__.__name__ == "Textbox":
				#If the part is a textbox, this formats it as such.
					rno = rnum[romannum]
					romannum = romannum + 1
					chkans = chkans + "\ncheckTextbox(\"" + qno + lno + rno + "\");\ndocument.getElementById(\"" + qno + lno + rno + "Example\").innerHTML = document.getElementById(\"" + qno + lno + rno + "\").value"
					chkcpl = chkcpl + "document.getElementById(\"" + qno + lno + rno + "\").value===\"\" || "
					contif = contif + "checkTextbox(\"" + qno + lno + rno + "\") &&"
					workbook = workbook + "<div id=\"new" + qno + lno + rno + "\"><textarea id=\"" + qno + lno + rno + "\" cols=\"40\" rows=\"5\"></textarea></div>"
					endtbl = endtbl + "\n<tr>\n<td style=\"border: 2pt black solid\">" + qno + lno + ". " + rno + ".</td>\n<td style=\"border: 2pt black solid\">" + part.example + "</td>\n<td style=\"border: 2pt black solid\"><div id=\"" + qno + lno + rno + "Example\"</div></td>\n<td style=\"border: 2pt black solid\"></td>\n<td style=\"border: 2pt black solid\">"
					if lno == "a" and rno == "i":
					#If this is the first part of the first section of a question, its row in the results table will display the time the number of seconds the student took for the whole question.
						endtbl = endtbl + "<div id=\"" + qno + "Time\"></div></td>\n<tr>"
						contfn = contfn + "\ndocument.getElementById(\"" + qno + "Time\").innerHTML = tim" + qno + ";"
					else:
						endtbl = endtbl + "</td>\n</tr>"
					disabl = disabl + "\ndocument.getElementById(\""+ qno + lno + rno +"\").disabled=true;"
				elif part.__class__.__name__ == "Table":
				#If the part is a table, this formats it as such.
					chktbl = ""
					allhead = ""
					allbody = ""
					allline = ""
					for item in part.header:
					#This prints every item in the header list in bold in a table cell.
						item = "\n<td style=\"border: 2pt black solid\"><b>" + str(item) + "</b></td>"
						allhead = allhead + item
					for body in part.rows:
					#This separates the rows in a give table object from each other.
						allline = allline + "<tr>"
						for drdn in body:
						#This separates the cells in a given row from each other.
							if isinstance(drdn, str):
							#If the cell is a string, it can be printed directly into the cell. If it is not a string, the cell contains at least one dropdown box and must be formatted differently.
								item = "\n<td style=\"border: 2pt black solid\">" + drdn + "</td>"
								allline = allline + item
							else:
								allline = allline + "<td style=\"border: 2pt black solid\">"
								for piece in drdn:
								#This separates the contents of a cell that contains at least one dropdown box.
									if isinstance(piece,str): #If the item in the list of content for a given cell is a string, it can be inserted directly.
										allline = allline + piece
									else:
									#If the item is not a string, it must be printed as a dropdown box.
										allans = ""
										rta = str(piece[1])
										for choice in piece[0]:
										#This places all of the listed options between <option> tags.
											option = "\n<option>" + str(choice) + "</option>"
											allans = allans + option
										rno = rnum[romannum]
										romannum = romannum + 1
										varset = varset + "\n" + lno + rno + ":0,"
										chkans = chkans + "checkAnswers(\"" + qno + lno + rno + "\", \"" + rta + "\");"
										chktbl = chktbl + "checkAnswers(\"" + qno + lno + rno + "\", \"" + rta + "\");"
										chkcpl = chkcpl + "document.getElementById(\"" + qno + lno + rno + "\").value===\"\" || "
										ctr = ctr + "if (!checkAnswers(\"" + qno + lno + rno + "\", \"" + rta + "\")) { \n set" + qno + "." + lno + rno + " = set" + qno + "." + lno + rno + " + 1;}"
										contif = contif + "(checkAnswers(\"" + qno + lno + rno + "\", \"" + rta + "\") || set" + qno + "." + lno + rno + "===3) &&"
										ctwrng = ctwrng + "\nif (!checkAnswers(\"" + qno + lno + rno + "\", \"" + rta + "\")) {\nif (set" + qno + "." + lno + rno + "===3) {\ndocument.getElementById(\"" + qno + lno + rno + "\").style.background=\"#FFFF00\";\n document.getElementById(\"" + qno + lno + rno + "Answer3\").innerHTML = document.getElementById(\"" + qno + lno + rno + "\").value \n }\nif (set" + qno + "." + lno + rno + "=== 1) { \n document.getElementById(\"" + qno + lno + rno + "Answer1\").innerHTML = \"; \" + document.getElementById(\"" + qno + lno + rno + "\").value \n } \n else if (set" + qno + "." + lno + rno + "=== 2) { \n document.getElementById(\"" + qno + lno + rno + "Answer2\").innerHTML = \"; \" + document.getElementById(\"" + qno + lno + rno + "\").value \n } \n else { \n document.getElementById(\"" + qno + lno + rno + "Answer3\").innerHTML = \"; \" + document.getElementById(\"" + qno + lno + rno + "\").value \n } \n } \n else { \n if (set" + qno + "." + lno + rno + "=== 0) { \n document.getElementById(\"" + qno + lno + rno + "Answer1\").innerHTML = \"; \" + document.getElementById(\"" + qno + lno + rno + "\").value \n } \n else if (set" + qno + "." + lno + rno + "=== 1) { \n document.getElementById(\"" + qno + lno + rno + "Answer2\").innerHTML = \"; \" + document.getElementById(\"" + qno + lno + rno + "\").value \n } \n else { \n document.getElementById(\"" + qno + lno + rno + "Answer3\").innerHTML = \"; \" + document.getElementById(\"" + qno + lno + rno + "\").value\n}\n};\nif(set" + qno + "." + lno + rno + "===3)\n{document.getElementById(\"" + qno + lno + rno + "\").value=\"" + rta + "\"};"
										allline = allline + "\n<select id=\"" + qno + lno + rno + "\">\n<option></option>" + allans + "</select>"
										endtbl = endtbl + "\n<tr>\n<td style=\"border: 2pt black solid\">" + qno + lno + ". " + rno + ".</td>\n<td style=\"border: 2pt black solid\">" + rta + "</td>\n<td style=\"border: 2pt black solid\"><div id=\"" + qno + lno + rno + "Answer1\"></div><div id=\"" + qno + lno + rno + "Answer2\"></div><div id=\"" + qno + lno + rno + "Answer3\"></div></td>\n<td style=\"border: 2pt black solid\"><div id=\"" + qno + lno + rno + "Tries\"></div></td>\n<td style=\"border: 2pt black solid\">"
										disabl = disabl + "\ndocument.getElementById(\""+ qno + lno + rno +"\").disabled=true;"
										endfn = endfn + "\ndocument.getElementById(\"" + qno + lno + rno + "Tries\").innerHTML=set" + qno + "." + lno + rno + ";"
										if lno == "a" and rno == "i":
										#If this is the first part of the first section of a question, its row in the results table will display the time the number of seconds the student took for the whole question.
											endtbl = endtbl + "<div id=\"" + qno + "Time\"></div></td>\n<tr>"
											contfn = contfn + "\ndocument.getElementById(\"" + qno + "Time\").innerHTML = tim" + qno + ";"
										else:
											endtbl = endtbl + "</td>\n</tr>"
								allline = allline + "</td>"
						allline = allline + "</tr>"
					allbody = allbody + allline
					workbook = workbook + "<table>\n<thead>" + allhead + "\n</thead>\n<tbody>" + allbody + "\n</tbody>\n</table>"
				elif part.__class__.__name__ == "Text":
				#If the item is a piece of text, this formats it as such.
					workbook = workbook + part.text
				elif part.__class__.__name__ == "Image":
				#If the item is an image, this formats it as such.
					workbook = workbook + "\n</p><img src =\"" + part.image + ".JPG\"/><p>"
				elif part.__class__.__name__ == "Checkbox":
				#If the item is a checkbox, this formats it as such.
					rno = rnum[romannum]
					romannum = romannum + 1
					allans = ""
					wrngcb = []
					for item in part.options_c:
					#This separates the options from each other.
						if not item in part.correct_c:
						#This creates a list of answers that are not supposed to be checked.
							wrngcb.append(item)
						item = "\n<input type=\"checkbox\" name=\"" + qno + lno + rno + "\" id=\"" + str(item) + "\">" + str(item) + "<br>"
						allans = allans + item
						chkbox = "1"
					for item in part.correct_c:
					#This separates the correct answers from each other.
						item = "\n(document.getElementById(\"" + qno + lno + rno + "\")"
						chkbox = chkbox + " && " + item
					varset = varset + "\n" + lno + rno + ":0,"
					chkans = chkans + "checkbox(\"" + qno + lno + rno + "\"," + str(part.correct_c) + "," + str(wrngcb) + ")"
					chkcpl = chkcpl + "checkbox(\"" + qno + lno + rno + "\",[]," + str(part.options_c) + ") || "
					ctr = ctr + "if (!checkbox(\"" + qno + lno + rno + "\"," + str(part.correct_c) + "," + str(wrngcb) + ")) { \n set" + qno + "." + lno + rno + " = set" + qno + "." + lno + rno + " + 1;}"
					contif = contif + "(checkbox(\"" + qno + lno + rno + "\"," + str(part.correct_c) + "," + str(wrngcb) + ")|| set" + qno + "." + lno + rno + "===3) && "
					ctwrng = ctwrng + "\nif (!checkbox(\"" + qno + lno + rno + "\"," + str(part.correct_c) + "," + str(wrngcb) + ")) {\nif (set" + qno + "." + lno + rno + "=== 1) { \n document.getElementById(\"" + qno + lno + rno + "Answer1\").innerHTML = retrieveCheckboxValue(" + str(part.options_c) + ")\n } \n else if (set" + qno + "." + lno + rno + "=== 2) { \n document.getElementById(\"" + qno + lno + rno + "Answer2\").innerHTML = retrieveCheckboxValue(" + str(part.options_c) + ")\n}\nelse {\ndocument.getElementById(\"" + qno + lno + rno + "Answer3\").innerHTML = retrieveCheckboxValue(" + str(part.options_c) + ")\n } \nif (set" + qno + "." + lno + rno + "===3) {\ncheckboxCorrection(\"" + qno + lno + rno + "\"," + str(part.correct_c) + "," + str(wrngcb) + ")}\n} \n else { \n if (set" + qno + "." + lno + rno + "=== 0) { \n document.getElementById(\"" + qno + lno + rno + "Answer1\").innerHTML = retrieveCheckboxValue(" + str(part.options_c) + ")\n } \n else if (set" + qno + "." + lno + rno + "=== 1) { \n document.getElementById(\"" + qno + lno + rno + "Answer2\").innerHTML = retrieveCheckboxValue(" + str(part.options_c) + ")\n } \n else { \n document.getElementById(\"" + qno + lno + rno + "Answer3\").innerHTML = retrieveCheckboxValue(" + str(part.options_c) + ")\n}\n};"
					workbook = workbook + "<div id=\"" + qno + lno + rno + "\">" + allans + "</div>"
					endtbl = endtbl + "\n<tr>\n<td style=\"border: 2pt black solid\">" + qno + lno + ". " + rno + ".</td>\n<td style=\"border: 2pt black solid\">" + str(part.correct_c) + "</td>\n<td style=\"border: 2pt black solid\"><div id=\"" + qno + lno + rno + "Answer1\"></div><div id=\"" + qno + lno + rno + "Answer2\"></div><div id=\"" + qno + lno + rno + "Answer3\"></div></td>\n<td style=\"border: 2pt black solid\"><div id=\"" + qno + lno + rno + "Tries\"></div></td>\n<td style=\"border: 2pt black solid\">"
					disset = ""
					for item in part.options_c:
					#This separates the options from each other.
						disset = disset + "\ndocument.getElementById(\"" + item + "\").disabled=true;"
					disabl = disabl + disset
					if lno == "a" and rno == "i":
					#If this is the first part of the first section of a question, its row in the results table will display the time the number of seconds the student took for the whole question.
						endtbl = endtbl + "<div id=\"" + qno + "Time\"></div></td>\n<tr>"
						contfn = contfn + "\ndocument.getElementById(\"" + qno + "Time\").innerHTML = tim" + qno + ";"
					else:
						endtbl = endtbl + "</td>\n</tr>"
					endfn = endfn + "\ndocument.getElementById(\"" + qno + lno + rno + "Tries\").innerHTML=set" + qno + "." + lno + rno + ";"
			workbook = workbook + "</p>"
		if int(qno) < len(list(wks.questions)):
		#If the question is the last question in the workbook, it needs to be formatted differently.
			chkcpl = chkcpl + "0) {\n alert(\"It appears you have left at least one of these fields blank. Please remedy this immediately.\");\n}"
			contif = contif + "1) {\n document.getElementById(\"question" + str(int(qno)+1) + "\").style.display = \"\";\n document.getElementById(\"button" + qno + "\").style.display = \"none\";\n" + disabl + "\ntim" + str(int(qno)+1) + "= 0;\n\nfunction time" + str(int(qno)+1) + "() {\nif (yestim" + str(int(qno)+1) + "){\ntim" + str(int(qno)+1) + " = tim" + str(int(qno)+1) + " + 1;\nt = setTimeout(function() {time" + str(int(qno)+1) + "()},1000);\n}\n};\nvar yestim" + str(int(qno)+1) + " = 1;\ntime" + str(int(qno)+1) + "();\n}"
			varset = varset + "}; \n"
			contfn = contfn + "\n" + chkans + "\n" + chkcpl + "\n" + ctr + "\n" + contif + "\n" + ctwrng
			workbook = workbook + "\n<script type=\"text/javascript\">" + varset + contfn + "};\n</script>\n" + dragoon_link + "\n<br><button id=\"button" + qno + "\" onClick=\"cont" + qno + "();\">Continue</button>\n<div id=\"question" + str(int(qno)+1) + "\" style=\"display: none\">"
			divset = divset + "</div>"
		else:
			varset = varset + "}; \n"
			chkcpl = chkcpl + "0) {\n alert(\"It appears you have left at least one of these fields blank. Please remedy this immediately.\");\n}"
			contif = contif + "1) {\n document.getElementById(\"question" + str(int(qno)+1) + "\").style.display = \"\";\n document.getElementById(\"button" + qno + "\").style.display = \"none\";\n" + disabl + "\ndisplayAnswers();\n}"
			contfn = contfn + "\n" + chkans + "\n" + chkcpl + "\n" + ctr + "\n" + contif + "\n" + ctwrng
			workbook = workbook + "\n<script type=\"text/javascript\">" + varset + contfn + "};\n</script>\n" + dragoon_link + "\n<br><button id=\"button" + qno + "\" onClick=\"cont" + qno + "();\">Continue</button>\n<div id=\"question" + str(int(qno)+1) + "\" style=\"display: none\">"
			divset = divset + "</div>"
	endtbl = endtbl + "\n</tbody>\n</table>\n</div>"
	endfn = endfn + "\n};\n</script>"
	workbook = workbook + divset + endtbl + endfn + "</body></html>"
	open(docname,"w").write(workbook)
	#Create a document in which the filename is the value of the variable "docname" (defined as the name given by the author + ".html") and all the content in the variable "workbook".

######################
# Construct an example:
	
def generateJSON(wkst,filename):
#converts the workbook object wkst into a JSON with filename as the filename
	with open(filename,"w") as outfile:
		json.dump(wkst,outfile,cls = CustomTypeEncoder, indent = 4)

def loadWorkbook(filename):
#loads the workbook object from the file with filename as its name
	with open(filename,"r") as outfile:
		wksht_dct = json.load(outfile)
		return CustomTypeDecoder(wksht_dct)
