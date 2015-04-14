import json
A = ["\u0022","\"","\u0027","'","-","\u2014","^o","/="]
B = ["&quot;","&quot;","&#39;","&#39;","&#45;","&#45;","&#176;","&#8800"]
class Worksheet:
	def __init__(self, filename):
		self.name = filename
		self.questions = []
		self.loose = []
	def jsonable(self):
		return self.__dict__
	def from_dict(dct):
		wks = Worksheet(dct['name'])
		wks.questions = list(map(CustomTypeDecoder,dct['questions'])) # for each item, decode it
		wks.loose = list(map(CustomTypeDecoder,dct['loose']))
		return wks
		
class LsText:
	def __init__(self,qstn):		
		self.before = qstn
	def from_scratch(qstn,wkst):
		ltx = LsText(qstn)
		ltx.text = input ("Text: ")
		for x in A:
			ltx.text = ltx.text.replace(x,B[A.index(x)])
		wkst.loose.append(self.from_scratch)
	def from_dict(dct):
		ltx = LsText(dct['before'])
		ltx.text = dct['text']
		return ltx
		
class LsImage:
	def __init__(self,qstn):
		self.before = qstn
	def from_scratch(qstn,wkst):
		lig = LsImage(qstn)
		lig.img = input ("File/Folder name: ")
		wkst.loose.append(self)
	def from_dict(dct):
		lig = LsImage(dct['before'])
		lig.img = dct['img']
		return lig
		
class Question:
	def __init__ (self,initializer):
		if isinstance(initializer,Worksheet):
			self.sub = input ("Subheading: ")
			for x in A:
				self.sub = self.sub.replace(x,B[A.index(x)])
			self.sections = []
			initializer.questions.append(self)
		elif isinstance(initializer,str):
			self.sub = initializer
			self.sections = []
		else:
			raise Exception("Bad initializer to question")
	def from_dict(dct):
		qes = Question(dct['sub'])
		qes.sections = list(map(CustomTypeDecoder,dct['sections']))
		return qes
		
class Section:
	def __init__ (self,qstn):
		if isinstance(qstn,Question):
			self.content = []
			qstn.sections.append(self)
		else:#elif isinstance(qstn,list):
			self.content = qstn
	def from_dict(dct):
		sct = Section(list(map(CustomTypeDecoder,dct['content'])))
		return sct
		
class Dragoon:
	def __init__ (self,sect):
		if isinstance(sect,Question):
			self.problem = input ("Problem: ")
			self.mode = input ("Mode: ").upper()
			qstn.sections.append(self)
		else:
			self.problem = sect
			self.mode = ""
	def from_dict(dct):
		drg = Dragoon(dct['problem'])
		drg.mode = dct['mode']
		return drg
		
class Table:
	def __init__(self,sect):
		if isinstance(sect,Section):
			self.header = input ("Header: ").split(",")
			self.rows = []
			line = input ("Line: ").split(",")
			while not "end" in line:
				line2 = []
				for cell in line:
					if cell == "dropdown":
						cell = input ("Cell: ").split(",")
						for item in cell:
							if item == "dropdown":
								item = []
								options = input ("Answers: ").split(",")
								correct = input ("Right answer: ")
								for x in A:
									correct = correct.replace(x,B[A.index(x)])
								if not correct in options:
									print("Please choose one of the given answers as the right answer.")
									correct = input ("Right answer: ")
									for x in A:
										correct = correct.replace(x,B[A.index(x)])
								item.append(options)
								item.append(correct)
								print(item)
					line2.append(cell)	
				self.rows.append(line2)
				line = input ("Line: ").split(",")
			sect.content.append(self)
		else:
			self.header = sect
			self.rows = []
	def from_dict(dct):
		tbl = Table(dct['header'])
		tbl.rows = list(map(Table.decodeRow,dct['rows']))
		return tbl
	def decodeRow(row):
		return list(map(CustomTypeDecoder,row))

class Dropdown:
	def __init__(self,sect):
		if isinstance (sect,Section):
			self.options = input ("Answers: ").split(",")
			for x in A:
				self.options = self.options.replace(x,B[A.index(x)])
			self.correct = input ("Right answer: ")
			for x in A:
				self.correct = self.correct.replace(x,B[A.index(x)])
			if not self.correct in self.options:
				print("Please choose one of the given answers as the right answer.")
				self.correct = input ("Right answer: ")
				for x in A:
					self.correct = self.correct.replace(x,B[A.index(x)])
			sect.content.append(self)
		else:#elif isinstance (sect,list):
			self.options = []
			self.correct = sect
	def from_dict(dct):
		drp = Dropdown(dct['correct'])
		drp.options = list(map(CustomTypeDecoder,dct['options']))
		return drp

class Textbox:
	def __init__(self,sect):
		if isinstance (sect,Section):
			self.example = input ("Example right answer: ")
			for x in A:
				self.example = self.example.replace(x,B[A.index(x)])
			sect.content.append(self)
		else:
			self.example = sect
	def from_dict(dct):
		box = Textbox(dct['example'])
		return box
		
class Text:
	def __init__ (self,sect):
		if isinstance (sect,Section):
			self.text = input ("Text: ")
			for x in A:
				self.text = self.text.replace(x,B[A.index(x)])
			sect.content.append(self)
		else:#elif isinstance (sect,list):
			self.text = sect
	def from_dict(dct):
		stx = Text(dct['text'])
		return stx

class Image:
	def __init__ (self,sect):
		if isinstance (sect,Section):
			self.image = input ("Folder/file name: ")
			sect.content.append(self)
		else:#elif isinstance (sect,list):
			self.image = sect
	def from_dict(dct):
		sig = Image(dct['image'])
		return sig
		
class Checkbox:
	def __init__(self,sect):
		if isinstance (sect,Section):
			self.options_c = input ("Answers: ").split(",")
			for x in A:
				self.options_c = self.options_c.replace(x,B[A.index(x)])
			self.correct_c = input ("Right answers: ").split(",")
			for x in A:
				self.correct_c = self.correct.replace(x,B[A.index(x)])
			for item in self.correct_c:
				if not item in self.options_c:
					print("Please choose one of the given answers as the right answer.")
					self.correct = input ("Right answers: ").split(",")
					for x in A:
						self.correct_c = self.correct.replace(x,B[A.index(x)])
			sect.content.append(self)
		else:
			self.options_c = []
			self.correct_c = sect
	def from_dict(dct):
		chk = Checkbox(dct['correct_c'])
		chk.options_c = list(map(CustomTypeDecoder,dct['options_c']))
		return chk
		
TYPES = { 'Worksheet': Worksheet,
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
	if type(dct) is dict and len(dct) == 1:
		#print(dct)
		#print(type(dct))
		type_name, value = list(dct.items())[0]
		type_name = type_name.strip('_')
		if type_name in TYPES:
			return TYPES[type_name].from_dict(value)
	return dct

######################
# Generator functions

		

def generateHTMLWorksheet(wks):
	# Converts Worksheet object, "wks" into an html/javascript file
	worksheet = "<!DOCTYPE html>\n<html>\n<head>\n<title>Dragoon Worksheet</title>\n<script type=\"text/javascript\">\nfunction\nopenDragoonProblem(num){\nvar u = document.getElementById(\"user\").value;\nvar s = document.getElementById(\"section\").value;\nvar problemID = \"problem\" + num.toString();\nvar p = document.getElementById(problemID).value;\nvar modeID = \"mode\" + num.toString();\nvar m = document.getElementById(modeID).value;\nvar urlString = \"http://dragoon.asu.edu/demo/index.html?u=\"+u+\"&m=\"+m+\"&p=\"+p+\"&s=\"+s;\nwindow.open(urlString);\n}\nfunction checkAnswers(inputId, rightAnswer)\n{\nif(document.getElementById(inputId).value===rightAnswer) {\ndocument.getElementById(inputId).style.background=\"#66FF33\";\nreturn true;\n}\nelse\n{\ndocument.getElementById(inputId).style.background=\"#FF3333\";\nreturn false;\n}\n};\nfunction checkTextbox(inputId) {\nif (!(document.getElementById(inputId).value===\"\")) {\ndocument.getElementById(inputId).style.background=\"#66FF33\";\nreturn true;\n}\nelse {\ndocument.getElementById(inputId).style.background=\"#FF3333\";\nreturn false;\n}\n};\n\nfunction checkbox(textId,checkedId,uncheckedId) {\nck = 0\nunck = 0\nfor (i = 0; i<checkedId.length; i++) {\nif (document.getElementById(checkedId[i]).checked) {\nck = ck + 1;\n}\n};\nfor (i = 0; i<uncheckedId.length; i++) {\nif (!(document.getElementById(uncheckedId[i]).checked)) {\nunck = unck + 1;\n}\n};\nif (checkedId.length == ck && uncheckedId.length == unck)\n{\ndocument.getElementById(textId).style.background=\"#66FF33\";\nreturn true\n}\nelse {\ndocument.getElementById(textId).style.background=\"#FF3333\";\nreturn false\n}\n};\n\nfunction checkboxCorrection(textId,checkedId,uncheckedId) {\nfor (i=0; i<checkedId.length; i++) {\ndocument.getElementById(checkedId[i]).checked = true;\n};\nfor (i=0; i<uncheckedId.length; i++) {\ndocument.getElementById(uncheckedId[i]).checked = false;\n};\ndocument.getElementById(textId).style.background = \"#FFFF00\"\n};\n\nfunction retrieveCheckboxValue(total) {\nresponse = []\nfor (i=0; i<total.length; i++) {\nif\n(document.getElementById (total[i]).checked) {\nresponse.push(total[i])\n}\n};\nreturn response\n};\n\nvar tim1 = 0;\nfunction time1 () {\nif (yestim1=1){\ntim1 = tim1 + 1;\nt = setTimeout(function() {time1()},1000);\n}\n};\nvar yestim1 = 1;\ntime1();\nfunction checkCompletion(num){\n// id is the id of the continue button or I just need a the number of the question i.e. if its cont1 just send me 1 and it will do\nvar u = document.getElementById(\"user\").value;\nvar s = document.getElementById(\"section\").value;\nvar problemID = \"problem\" + num.toString();\nvar p = document.getElementById(problemID).value.slice(0,30);\nvar modeID = \"mode\" + num.toString();\nvar m = document.getElementById(modeID).value;\nvar xmlHTTP = new XMLHttpRequest();\nvar userObject;\nxmlHTTP.onreadystatechange = function(){\nif(xmlHTTP.readyState == 4 && xmlHTTP.status == 200){\nuserObject = JSON.parse(xmlHTTP.responseText);\n}\n}\nvar url = \"../demo/log/dashboard_js.php?m=\"+m+\"&u=\"+u+\"&s=\"+s+\"&p=\"+p;\n//var url = \"log/dashboard_js.php?m=\"+m+\"&u=\"+u+\"&s=\"+s+\"&p=\"+p;\nxmlHTTP.open(\"GET\", url, false);\nxmlHTTP.send();\nvar id = \"dragoonErrorMessage\" + num.toString();\nvar result = false;\n if(userObject != null){\nresult = userObject[0].problemComplete;\n}\nif(result) {\ndocument.getElementById(id).style.display = \"none\";\n} else {\ndocument.getElementById(id).style.display = \"\";\n}\nreturn result;\n}</script>\n</head>\n<body>\n<label>Username :</label>&nbsp;<input type=\"text\" name=\"user\" id=\"user\">\n<input type=\"hidden\" name=\"section\" id=\"section\" value=\"public-worksheet\">\n<script type=\"text/javascript\">\nfunction enterUsername() {\nif (document.getElementById(\"user\").value!==\"\" && document.getElementById(\"user\").value.length<=30) {\ndocument.getElementById(\"wkstBody\").style.display=\"\";\ndocument.getElementById(\"usernameCheck\").style.display=\"none\";\ndocument.getElementById(\"user\").style.background=\"\";\ndocument.getElementById(\"user\").disabled=true;\n}\nelse {\ndocument.getElementById(\"user\").style.background=\"#FF3333\";\nalert(\"Please make sure you have entered a username and that your username is between 1 and 30 characters long.\");\n}\n};\n</script>\n<br><br><button id=\"usernameCheck\" onClick=\"enterUsername();\">Start Worksheet</button><div id=\"wkstBody\" style=\"display: none\">"
	divset = "\n</div>"
	endtbl = "<div id=\"resultsTable\" style=\"display:none\">\n<table>\n<thead>\n<td style=\"border: 2pt black solid\">Question</td>\n<td style=\"border: 2pt black solid\">Correct Answer</td>\n<td style=\"border: 2pt black solid\">Student Answers</td>\n<td style=\"border: 2pt black solid\">Number of Wrong Tries</td>\n<td style=\"border: 2pt black solid\">Time for Entire Question (s)</td>\n</thead>\n<tbody>"
	endfn = "<script type=\"text/javascript\">\nfunction displayAnswers () {\ndocument.getElementById(\"resultsTable\").style.display=\"\""
	alph = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
	rnum = ["i","ii","iii","iv","v","vi","vii","viii","ix","x","xi","xii","xiii","xiv","xv","xvi","xvii","xviii","xix","xx","xxi","xxii","xxiii","xxiv","xxv"]
	docname = wks.name + ".html"
	qno = 0
	for ques in wks.questions:
		dragoon_link = ""
		qno = str(int(qno) + 1)
		for lse in wks.loose:
			if int(qno) == int(lse.before):
				if lse.__class__.__name__ == "LsImage":
					worksheet = worksheet + "\n</p><img src =\"" + lse.img + ".JPG\"/><p>"
				else:
					worksheet = worksheet + "\n<p>" + lse.text + "</p>"
		contfn = "function cont" + qno + "() {\nvar yestim" + qno + " = 0;"
		chkans = ""
		chkcpl = "if ("
		contif = "if ("
		disabl = ""
		ctwrng = ""
		ctr = ""
		varset = "var set" + str(qno) + " = {"
		worksheet = worksheet + "\n<h3>" + ques.sub + "</h3>"
		alphindex = 0
		for sect in ques.sections:
			lno = alph[alphindex]
			alphindex = alphindex + 1
			romannum = 0
			for part in sect.content:
				if part.__class__.__name__ == "Dragoon":
					worksheet = worksheet + "</p>\n<input type=\"hidden\" name=\"problem" + qno + "\" id=\"problem" + qno + "\" value=\"" + part.problem + "\">\n<input type=\"hidden\" name=\"mode" + qno + "\" id=\"mode" + qno + "\" value=\"" + part.mode + "\">\n<br><button id=\"dragoonButton" + qno + "\" onClick=\"openDragoonProblem(" + qno + ");\">Open Dragoon</button>\n<div id=\"dragoonErrorMessage" + qno + "\" style=\"color:red;display:none\"><p>Your Dragoon problem is incomplete!  Please make sure your nodes are finished (i.e. have solid borders) and that you can view the model's graph and table of values.</p></div><p>"
					contif = contif + "checkCompletion(" + qno + ") && "
				elif part.__class__.__name__ == "Dropdown":
					rno = rnum[romannum]
					romannum = romannum + 1
					allans = ""
					for item in part.options:
						item = "\n<option>" + str(item) + "</option>"
						allans = allans + item
					varset = varset + "\n" + lno + rno + ":0,"
					chkans = chkans + "\ncheckAnswers(\"" + qno + lno + rno + "\", \"" + part.correct + "\");"
					chkcpl = chkcpl + "document.getElementById(\"" + qno + lno + rno + "\").value===\"\" || "
					ctr = ctr + "if (!checkAnswers(\"" + qno + lno + rno + "\", \"" + part.correct + "\")) { \n set" + qno + "." + lno + rno + " = set" + qno + "." + lno + rno + " + 1;}"
					contif = contif + "(checkAnswers(\"" + qno + lno + rno + "\", \"" + part.correct + "\") || set" + qno + "." + lno + rno + "===3) &&"
					ctwrng = ctwrng + "\nif (!checkAnswers(\"" + qno + lno + rno + "\", \"" + part.correct + "\")) {\nif (set" + qno + "." + lno + rno + "===3) {\ndocument.getElementById(\"" + qno + lno + rno + "\").style.background=\"#FFFF00\";\n document.getElementById(\"" + qno + lno + rno + "Answer3\").innerHTML = document.getElementById(\"" + qno + lno + rno + "\").value \n }\nif (set" + qno + "." + lno + rno + "=== 1) { \n document.getElementById(\"" + qno + lno + rno + "Answer1\").innerHTML = \"; \" + document.getElementById(\"" + qno + lno + rno + "\").value \n } \n else if (set" + qno + "." + lno + rno + "=== 2) { \n document.getElementById(\"" + qno + lno + rno + "Answer2\").innerHTML = \"; \" + document.getElementById(\"" + qno + lno + rno + "\").value \n } \n else { \n document.getElementById(\"" + qno + lno + rno + "Answer3\").innerHTML = \"; \" + document.getElementById(\"" + qno + lno + rno + "\").value \n } \n } \n else { \n if (set" + qno + "." + lno + rno + "=== 0) { \n document.getElementById(\"" + qno + lno + rno + "Answer1\").innerHTML = \"; \" + document.getElementById(\"" + qno + lno + rno + "\").value \n } \n else if (set" + qno + "." + lno + rno + "=== 1) { \n document.getElementById(\"" + qno + lno + rno + "Answer2\").innerHTML = \"; \" + document.getElementById(\"" + qno + lno + rno + "\").value \n } \n else { \n document.getElementById(\"" + qno + lno + rno + "Answer3\").innerHTML = \"; \" + document.getElementById(\"" + qno + lno + rno + "\").value\n}\n};\nif(set" + qno + "." + lno + rno + "===3)\n{document.getElementById(\"" + qno + lno + rno + "\").value=\"" + part.correct + "\"};"
					worksheet = worksheet + "<select id=\"" + qno + lno + rno + "\">\n<option></option>" + allans + "</select>"
					endtbl = endtbl + "\n<tr>\n<td style=\"border: 2pt black solid\">" + qno + lno + ". " + rno + ".</td>\n<td style=\"border: 2pt black solid\">" + part.correct + "</td>\n<td style=\"border: 2pt black solid\"><div id=\"" + qno + lno + rno + "Answer1\"></div><div id=\"" + qno + lno + rno + "Answer2\"></div><div id=\"" + qno + lno + rno + "Answer3\"></div></td>\n<td style=\"border: 2pt black solid\"><div id=\"" + qno + lno + rno + "Tries\"></div></td>\n<td style=\"border: 2pt black solid\">"
					disabl = disabl + "\ndocument.getElementById(\""+ qno + lno + rno +"\").disabled=true;"
					if lno == "a" and rno == "i":
						endtbl = endtbl + "<div id=\"" + qno + "Time\"></div></td>\n<tr>"
						contfn = contfn + "\ndocument.getElementById(\"" + qno + "Time\").innerHTML = tim" + qno + ";"
					else:
						endtbl = endtbl + "</td>\n</tr>"
					endfn = endfn + "\ndocument.getElementById(\"" + qno + lno + rno + "Tries\").innerHTML=set" + qno + "." + lno + rno + ";"
				elif part.__class__.__name__ == "Textbox":
					rno = rnum[romannum]
					romannum = romannum + 1
					chkans = chkans + "\ncheckTextbox(\"" + qno + lno + rno + "\");\ndocument.getElementById(\"" + qno + lno + rno + "Example\").innerHTML = document.getElementById(\"" + qno + lno + rno + "\").value"
					chkcpl = chkcpl + "document.getElementById(\"" + qno + lno + rno + "\").value===\"\" || "
					contif = contif + "checkTextbox(\"" + qno + lno + rno + "\") &&"
					worksheet = worksheet + "<div id=\"new" + qno + lno + rno + "\"><textarea id=\"" + qno + lno + rno + "\" cols=\"40\" rows=\"5\"></textarea></div>"
					endtbl = endtbl + "\n<tr>\n<td style=\"border: 2pt black solid\">" + qno + lno + ". " + rno + ".</td>\n<td style=\"border: 2pt black solid\">" + part.example + "</td>\n<td style=\"border: 2pt black solid\"><div id=\"" + qno + lno + rno + "Example\"</div></td>\n<td style=\"border: 2pt black solid\"></td>\n<td style=\"border: 2pt black solid\">"
					if lno == "a" and rno == "i":
						endtbl = endtbl + "<div id=\"" + qno + "Time\"></div></td>\n<tr>"
						contfn = contfn + "\ndocument.getElementById(\"" + qno + "Time\").innerHTML = tim" + qno + ";"
					else:
						endtbl = endtbl + "</td>\n</tr>"
					disabl = disabl + "\ndocument.getElementById(\""+ qno + lno + rno +"\").disabled=true;"
				elif part.__class__.__name__ == "Table":
					chktbl = ""
					allhead = ""
					allbody = ""
					allline = ""
					for item in part.header:
						item = "\n<td style=\"border: 2pt black solid\"><b>" + str(item) + "</b></td>"
						allhead = allhead + item
					for body in part.rows:
						allline = allline + "<tr>"
						for drdn in body:
							if isinstance(drdn, str):
								item = "\n<td style=\"border: 2pt black solid\">" + drdn + "</td>"
								allline = allline + item
							else:
								allans = ""
								rta = drdn[1]
								for choice in drdn[0]:
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
								ctwrng = ctwrng + "\nif (!checkAnswers(\"" + qno + lno + rno + "\", \"" + rta + "\")) {\nif (set" + qno + "." + lno + rno + "===3) {\ndocument.getElementById(\"" + qno + lno + rno + "\").value=\"" + rta + "\";\ndocument.getElementById(\"" + qno + lno + rno + "\").style.background=\"#FFFF00\"}\nif (set" + qno + "." + lno + rno + "=== 1) { \n document.getElementById(\"" + qno + lno + rno + "Answer1\").innerHTML = \"; \" + document.getElementById(\"" + qno + lno + rno + "\").value \n } \n else if (set" + qno + "." + lno + rno + "=== 2) { \n document.getElementById(\"" + qno + lno + rno + "Answer2\").innerHTML = \"; \" + document.getElementById(\"" + qno + lno + rno + "\").value \n } \n else { \n document.getElementById(\"" + qno + lno + rno + "Answer3\").innerHTML = \"; \" + document.getElementById(\"" + qno + lno + rno + "\").value \n } \n } \n else { \n if (set" + qno + "." + lno + rno + "=== 0) { \n document.getElementById(\"" + qno + lno + rno + "Answer1\").innerHTML = \"; \" + document.getElementById(\"" + qno + lno + rno + "\").value \n } \n else if (set" + qno + "." + lno + rno + "=== 1) { \n document.getElementById(\"" + qno + lno + rno + "Answer2\").innerHTML = \"; \" + document.getElementById(\"" + qno + lno + rno + "\").value \n } \n else { \n document.getElementById(\"" + qno + lno + rno + "Answer3\").innerHTML = \"; \" + document.getElementById(\"" + qno + lno + rno + "\").value\n}\n};"
								allline = allline + "<td style=\"border: 2pt black solid\"><select id=\"" + qno + lno + rno + "\">\n<option></option>" + allans + "</select></td>"
								endtbl = endtbl + "\n<tr>\n<td style=\"border: 2pt black solid\">" + qno + lno + ". " + rno + ".</td>\n<td style=\"border: 2pt black solid\">" + rta + "</td>\n<td style=\"border: 2pt black solid\"><div id=\"" + qno + lno + rno + "Answer1\"></div><div id=\"" + qno + lno + rno + "Answer2\"></div><div id=\"" + qno + lno + rno + "Answer3\"></div></td>\n<td style=\"border: 2pt black solid\"><div id=\"" + qno + lno + rno + "Tries\"></div></td>\n<td style=\"border: 2pt black solid\">"
								disabl = disabl + "\ndocument.getElementById(\""+ qno + lno + rno +"\").disabled=true;"
								if lno == "a" and rno == "i":
									endtbl = endtbl + "<div id=\"" + qno + "Time\"></div></td>\n<tr>"
									contfn = contfn + "\ndocument.getElementById(\"" + qno + "Time\").innerHTML = tim" + qno + ";"
								else:
									endtbl = endtbl + "</td>\n</tr>"
								endfn = endfn + "\ndocument.getElementById(\"" + qno + lno + rno + "Tries\").innerHTML=set" + qno + "." + lno + rno + ";"
						allline = allline + "</tr>"
					allbody = allbody + allline
					worksheet = worksheet + "<table>\n<thead>" + allhead + "\n</thead>\n<tbody>" + allbody + "\n</tbody>\n</table>"#"\n<script type=\"text/javascript\">\nfunction checkTable" + qno + lno + rno + "() {\n" + chktbl + "\n};\n</script>\n<br><br><button id=\"table" + qno + lno + rno + "\" onClick=\"checkTable" + qno + lno + rno + "();\">Check Table</button><br><br>"
				elif part.__class__.__name__ == "Text":
					worksheet = worksheet + part.text
				elif part.__class__.__name__ == "Image":
					worksheet = worksheet + "\n</p><img src =\"" + part.image + ".JPG\"/><p>"
				elif part.__class__.__name__ == "Checkbox":
					rno = rnum[romannum]
					romannum = romannum + 1
					allans = ""
					wrngcb = []
					for item in part.options_c:
						if not item in part.correct_c:
							wrngcb.append(item)
						item = "\n<input type=\"checkbox\" name=\"" + qno + lno + rno + "\" id=\"" + str(item) + "\">" + str(item) + "<br>"
						allans = allans + item
						chkbox = "1"
					for item in part.correct_c:
						item = "\n(document.getElementById(\"" + qno + lno + rno + "\")"
						chkbox = chkbox + " && " + item
					varset = varset + "\n" + lno + rno + ":0,"
					chkans = chkans + "checkbox(\"" + qno + lno + rno + "\"," + str(part.correct_c) + "," + str(wrngcb) + ")"
					chkcpl = chkcpl + "checkbox(\"" + qno + lno + rno + "\",[]," + str(part.options_c) + ") || "
					ctr = ctr + "if (!checkbox(\"" + qno + lno + rno + "\"," + str(part.correct_c) + "," + str(wrngcb) + ")) { \n set" + qno + "." + lno + rno + " = set" + qno + "." + lno + rno + " + 1;}"
					contif = contif + "(checkbox(\"" + qno + lno + rno + "\"," + str(part.correct_c) + "," + str(wrngcb) + ")|| set" + qno + "." + lno + rno + "===3) && "
					ctwrng = ctwrng + "\nif (!checkbox(\"" + qno + lno + rno + "\"," + str(part.correct_c) + "," + str(wrngcb) + ")) {\nif (set" + qno + "." + lno + rno + "=== 1) { \n document.getElementById(\"" + qno + lno + rno + "Answer1\").innerHTML = retrieveCheckboxValue(" + str(part.options_c) + ")\n } \n else if (set" + qno + "." + lno + rno + "=== 2) { \n document.getElementById(\"" + qno + lno + rno + "Answer2\").innerHTML = retrieveCheckboxValue(" + str(part.options_c) + ")\n}\nelse {\ndocument.getElementById(\"" + qno + lno + rno + "Answer3\").innerHTML = retrieveCheckboxValue(" + str(part.options_c) + ")\n } \nif (set" + qno + "." + lno + rno + "===3) {\ncheckboxCorrection(\"" + qno + lno + rno + "\"," + str(part.correct_c) + "," + str(wrngcb) + ")}\n} \n else { \n if (set" + qno + "." + lno + rno + "=== 0) { \n document.getElementById(\"" + qno + lno + rno + "Answer1\").innerHTML = retrieveCheckboxValue(" + str(part.options_c) + ")\n } \n else if (set" + qno + "." + lno + rno + "=== 1) { \n document.getElementById(\"" + qno + lno + rno + "Answer2\").innerHTML = retrieveCheckboxValue(" + str(part.options_c) + ")\n } \n else { \n document.getElementById(\"" + qno + lno + rno + "Answer3\").innerHTML = retrieveCheckboxValue(" + str(part.options_c) + ")\n}\n};"
					worksheet = worksheet + "<div id=\"" + qno + lno + rno + "\">" + allans + "</div>"
					endtbl = endtbl + "\n<tr>\n<td style=\"border: 2pt black solid\">" + qno + lno + ". " + rno + ".</td>\n<td style=\"border: 2pt black solid\">" + str(part.correct_c) + "</td>\n<td style=\"border: 2pt black solid\"><div id=\"" + qno + lno + rno + "Answer1\"></div><div id=\"" + qno + lno + rno + "Answer2\"></div><div id=\"" + qno + lno + rno + "Answer3\"></div></td>\n<td style=\"border: 2pt black solid\"><div id=\"" + qno + lno + rno + "Tries\"></div></td>\n<td style=\"border: 2pt black solid\">"
					disset = ""
					for item in part.options_c:
						disset = disset + "\ndocument.getElementById(\"" + item + "\").disabled=true;"
					disabl = disabl + disset
					if lno == "a" and rno == "i":
						endtbl = endtbl + "<div id=\"" + qno + "Time\"></div></td>\n<tr>"
						contfn = contfn + "\ndocument.getElementById(\"" + qno + "Time\").innerHTML = tim" + qno + ";"
					else:
						endtbl = endtbl + "</td>\n</tr>"
					endfn = endfn + "\ndocument.getElementById(\"" + qno + lno + rno + "Tries\").innerHTML=set" + qno + "." + lno + rno + ";"
			worksheet = worksheet + "</p>"
		if int(qno) < len(list(wks.questions)):
			chkcpl = chkcpl + "0) {\n alert(\"It appears you have left at least one of these fields blank. Please remedy this immediately.\");\n}"
			contif = contif + "1) {\n document.getElementById(\"question" + str(int(qno)+1) + "\").style.display = \"\";\n document.getElementById(\"button" + qno + "\").style.display = \"none\";\n" + disabl + "\ntim" + str(int(qno)+1) + "= 0;\n\nfunction time" + str(int(qno)+1) + "() {\nif (yestim" + str(int(qno)+1) + "){\ntim" + str(int(qno)+1) + " = tim" + str(int(qno)+1) + " + 1;\nt = setTimeout(function() {time" + str(int(qno)+1) + "()},1000);\n}\n};\nvar yestim" + str(int(qno)+1) + " = 1;\ntime" + str(int(qno)+1) + "();\n}"
			varset = varset + "}; \n"
			contfn = contfn + "\n" + chkans + "\n" + chkcpl + "\n" + ctr + "\n" + contif + "\n" + ctwrng
			worksheet = worksheet + "\n<script type=\"text/javascript\">" + varset + contfn + "};\n</script>\n" + dragoon_link + "\n<br><button id=\"button" + qno + "\" onClick=\"cont" + qno + "();\">Continue</button>\n<div id=\"question" + str(int(qno)+1) + "\" style=\"display: none\">"
			divset = divset + "</div>"
		else:
			varset = varset + "}; \n"
			chkcpl = chkcpl + "0) {\n alert(\"It appears you have left at least one of these fields blank. Please remedy this immediately.\");\n}"
			contif = contif + "1) {\n document.getElementById(\"question" + str(int(qno)+1) + "\").style.display = \"\";\n document.getElementById(\"button" + qno + "\").style.display = \"none\";\n" + disabl + "\ndisplayAnswers();\n}"
			contfn = contfn + "\n" + chkans + "\n" + chkcpl + "\n" + ctr + "\n" + contif + "\n" + ctwrng
			worksheet = worksheet + "\n<script type=\"text/javascript\">" + varset + contfn + "};\n</script>\n" + dragoon_link + "\n<br><button id=\"button" + qno + "\" onClick=\"cont" + qno + "();\">Continue</button>\n<div id=\"question" + str(int(qno)+1) + "\" style=\"display: none\">"
			divset = divset + "</div>"
	endtbl = endtbl + "\n</tbody>\n</table>\n</div>"
	endfn = endfn + "\n};\n</script>"
	worksheet = worksheet + divset + endtbl + endfn + "</body></html>"
	open(docname,"w").write(worksheet)

######################
## Construct an example:
	
#with open("blood_glucose.json","w") as outfile:
	#json.dump(wk1,outfile,cls = CustomTypeEncoder, indent = 4)

def testload():
	with open("Completed Worksheets/Isle Royale/isle_royale.json","r") as outfile:
		wksht_dct = json.load(outfile)
		return CustomTypeDecoder(wksht_dct)
