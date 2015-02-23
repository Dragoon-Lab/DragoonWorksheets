import json
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
			self.gen = input ("General description: ")
			self.sections = []
			initializer.questions.append(self)
		elif isinstance(initializer,str):
			self.gen = initializer
			self.sections = []
		else:
			raise Exception("Bad initializer to question")
	def from_dict(dct):
		qes = Question(dct['gen'])
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
	def __init__ (self,qstn):
		if isinstance(qstn,Question):
			self.problem = input("Problem: ")
			self.mode = input ("Mode: ").upper()
		else:
			self.problem = qstn
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
			line = input("Line: ").split(",")
			while not "end" in line:
				line2 = []
				for item in line:
					if item == "dropdown":
						item = []
						options = input ("Answers: ").split(",")
						correct = input ("Right answer: ")
						if not correct in options:
							print("Please choose one of the given answers as the right answer.")
							correct = input ("Right answer: ")
						item.append(options)
						item.append(correct)
					line2.append(item)	
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
			self.correct = input ("Right answer: ")
			if not self.correct in self.options:
				print("Please choose one of the given answers as the right answer.")
				self.correct = input ("Right answer: ")
			sect.content.append(self)
		else:#elif isinstance (sect,list):
			self.options = []
			self.correct = sect
	def from_dict(dct):
		drp = Dropdown(dct['correct'])
		drp.options = list(map(CustomTypeDecoder,dct['options']))
		return drp
		
class Text:
	def __init__ (self,sect):
		if isinstance (sect,Section):
			self.text = input("Text: ")
			sect.content.append(self)
		else:#elif isinstance (sect,list):
			self.text = sect
	def from_dict(dct):
		stx = Text(dct['text'])
		return stx

class Image:
	def __init__ (self,sect):
		if isinstance (sect,Section):
			self.image = input("Folder/file name: ")
			sect.content.append(self)
		else:#elif isinstance (sect,list):
			self.img = sect
	def from_dict(dct):
		sig = Image(dct['image'])
		return sig
		
class Checkbox:
	def __init__(self,sect):
		if isinstance (sect,Section):
			self.options_c = input ("Answers: ").split(",")
			self.correct_c = input ("Right answers: ").split(",")
			#for item in self.correct_c:
				#if not item in self.options_c:
					#print("Please choose one of the given answers as the right answer.")
					#self.correct_c = input ("Right answers: ")
			sect.content.append(self)
		else:
			self.options_c = []
			self.correct_c = sect
	def from_dict(dct):
		chk = Checkbox(dct['correct_c'])
		chk.options_c = list(map(CustomTypeDecoder,dct['options_c']))
		
TYPES = { 'Worksheet': Worksheet,
		  'LsText': LsText,
		  'LsImage': LsImage,
          'Question': Question,
		  'Dragoon': Dragoon,
		  'Section': Section,
		  'Table': Table,
		  'Dropdown': Dropdown,
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
	worksheet = "<!DOCTYPE html>\n<html>\n<head>\n<title>Dragoon Worksheet</title>\n<script type=\"text/javascript\">\nfunction\nopenDragoonProblem(num){\nvar u = document.getElementById(\"user\").value;\nvar s = document.getElementById(\"section\").value;\nvar problemID = \"problem\" + num.toString();\nvar p = document.getElementById(problemID).value;\nvar modeID = \"mode\" + num.toString();\nvar m = document.getElementById(modeID).value;\nvar urlString = \"http://dragoon.asu.edu/demo/index.html?u=\"+u+\"&m=\"+m+\"&p=\"+p+\"&s=\"+s;\nwindow.open(urlString);\n}\nfunction checkAnswers(inputId, rightAnswer)\n{\nif(document.getElementById(inputId).value===rightAnswer) {\ndocument.getElementById(inputId).style.background=\"#66FF33\";\nreturn true;\n}\nelse\n{\ndocument.getElementById(inputId).style.background=\"#FF3333\";\nreturn false;\n}\n};\n\nvar tim1 = 0;\nfunction time1 () {\nif (yestim1=1){\ntim1 = tim1 + 1;\nt = setTimeout(function() {time1()},1000);\n}\n};\nvar yestim1 = 1;\ntime1();\nfunction checkCompletion(num){\n// id is the id of the continue button or I just need a the number of the question i.e. if its cont1 just send me 1 and it will do\nvar u = document.getElementById(\"user\").value;\nvar s = document.getElementById(\"section\").value;\nvar problemID = \"problem\" + num.toString();\nvar p = document.getElementById(problemID).value;\nvar modeID = \"mode\" + num.toString();\nvar m = document.getElementById(modeID).value;\nvar xmlHTTP = new XMLHttpRequest();\nvar userObject;\nxmlHTTP.onreadystatechange = function(){\nif(xmlHTTP.readyState == 4 && xmlHTTP.status == 200){\nuserObject = JSON.parse(xmlHTTP.responseText);\n}\n}\nvar url = \"../demo/log/dashboard_js.php?m=\"+m+\"&u=\"+u+\"&s=\"+s+\"&p=\"+p;\n//var url = \"log/dashboard_js.php?m=\"+m+\"&u=\"+u+\"&s=\"+s+\"&p=\"+p;\nxmlHTTP.open(\"GET\", url, false);\nxmlHTTP.send();\nvar id = \"dragoonErrorMessage\" + num.toString();\nvar result = false;\n if(userObject != null){\nresult = userObject[0].problemComplete;\n}\nif(result) {\ndocument.getElementById(id).style.display = \"none\";\n} else {\ndocument.getElementById(id).style.display = \"\";\n}\nreturn result;\n}</script>\n</head>\n<body>\n<label>Username :</label>&nbsp;<input type=\"text\" name=\"user\" id=\"user\">\n<input type=\"hidden\" name=\"section\" id=\"section\" value=\"public-worksheet\">"
	divset = "\n"
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
					worksheet = worksheet + "\n<img src =\"" + lse.img + ".JPG\"/>"
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
		worksheet = worksheet + "\n<h3>Question " + qno + "</h3>\n<p>" + ques.gen + "</p>"
		alphindex = 0
		for sect in ques.sections:
			if sect.__class__.__name__ == "Dragoon":
				dragoon_link = "<input type=\"hidden\" name=\"problem" + qno + "\" id=\"problem" + qno + "\" value=\"" + sect.problem + "\">\n<input type=\"hidden\" name=\"mode" + qno + "\" id=\"mode" + qno + "\" value=\"" + sect.mode + "\">\n<br><button id=\"dragoonButton" + qno + "\" onClick=\"openDragoonProblem(" + qno + ");\">Open Dragoon</button>\n<div id=\"dragoonErrorMessage" + qno + "\" style=\"color:red;display:none\"><p>Your Dragoon problem is incomplete!  Please make sure your nodes are finished (i.e. have solid borders) and that you can view the model's graph and table of values.</p></div>"
				contif = contif + "checkCompletion(" + qno + ") && "
			else:
				lno = alph[alphindex]
				alphindex = alphindex + 1
				worksheet = worksheet + "\n<p>" + qno + lno + ". "
				romannum = 0
				for part in sect.content:
					if part.__class__.__name__ == "Dropdown":
						rno = rnum[romannum]
						romannum = romannum + 1
						allans = ""
						for item in part.options:
							item = "\n<option>" + str(item) + "</option>"
							allans = allans + item
						varset = varset + "\n" + lno + rno + ":0,"
						chkans = chkans + "checkAnswers(\"" + qno + lno + rno + "\", \"" + part.correct + "\");"
						chkcpl = chkcpl + "document.getElementById(\"" + qno + lno + rno + "\").value===\"\" ||"
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
					elif part.__class__.__name__ == "Table":
						global allhead
						allhead = ""
						global allbody
						allbody = ""
						allline = ""
						for item in part.header:
							item = "\n<td style=\"border: 2pt black solid\"><b>" + str(item) + "</b></td>"
							allhead = allhead + item
						for body in part.rows:
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
									chkcpl = chkcpl + "document.getElementById(\"" + qno + lno + rno + "\").value===\"\" ||"
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
							#line = input("Line: ").split(",")
						worksheet = worksheet + "<table>\n<thead>" + allhead + "\n</thead>\n<tbody>" + allbody + "\n</tbody>\n</table>"
					elif part.__class__.__name__ == "Text":
						worksheet = worksheet + "\n" + part.text + ""
					elif part.__class__.__name__ == "Image":
						worksheet = worksheet + "\n<img src =\"" + part.img + ".JPG\"/>"
					'''elif part.__class__.__name__ == "Checkbox":
					
					--Turn green if correct
					--Allow worksheet to move forward if correct
					--Count wrong
					--Turn yellow and change answer if wrong 3X
					--Send wrong answers to end table (as list of as true/false individually?)
					--Send message if incomplete?
						rno = rnum[romannum]
						romannum = romannum + 1
						allans = ""
						for item in part.options_c:
							item = "\n<input type=\"checkbox\" name=\"" + qno + lno + rno + "\" id=\"" + str(item) + "\">" + str(item) + "<br>"
							allans = allans + item
							chkbox = "1"
						for item in part.correct_c:
							item = "\n(document.getElementById(\"" + qno + lno + rno + "\")"
							chkbox = chkbox + " && " + item
						varset = varset + "\n" + lno + rno + ":0,"'''
					worksheet = worksheet + "</p>"
		if int(qno) < len(list(wks.questions)):
			varset = varset + "}; \n"
			chkcpl = chkcpl + "0) {\n alert(\"It appears you have left at least one of these fields blank. Please remedy this immediately.\");\n}"
			contif = contif + "1) {\n document.getElementById(\"question" + str(int(qno)+1) + "\").style.display = \"\";\n document.getElementById(\"button" + qno + "\").style.display = \"none\";\n" + disabl + "\ntim" + str(int(qno)+1) + "= 0;\n\nfunction time" + str(int(qno)+1) + "() {\nif (yestim" + str(int(qno)+1) + "){\ntim" + str(int(qno)+1) + " = tim" + str(int(qno)+1) + " + 1;\nt = setTimeout(function() {time" + str(int(qno)+1) + "()},1000);\n}\n};\nvar yestim" + str(int(qno)+1) + " = 1;\ntime" + str(int(qno)+1) + "();\n}"
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
	
#with open("energy_balance.json","w") as outfile:
	#json.dump(wk1,outfile,cls = CustomTypeEncoder, indent = 4)

def testload():
	with open("energy_balance.json","r") as outfile:
		wksht_dct = json.load(outfile)
		return CustomTypeDecoder(wksht_dct)
		
'''Tasks:
--Add ability to do checkboxes
--Add ability to do text boxes
--Construct JSONs for remaining worksheets'''
