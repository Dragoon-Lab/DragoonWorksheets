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
		wkst.loose.append(self)
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
		
TYPES = { 'Worksheet': Worksheet,
		  'LsText': LsText,
		  'LsImage': LsImage,
          'Question': Question,
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
	if len(dct) == 1:
		type_name, value = list(dct.items())[0]
		type_name = type_name.strip('_')
		if type_name in TYPES:
			return TYPES[type_name].from_dict(value)
	return dct

'''def getJsonable(obj):
	if hasattr(obj, 'jsonable'):
		return obj.jsonable()
	else:
		raise (TypeError, 'Object of type %s with value of %s is not JSON serializable')'''

######################
# Generator functions

		

def generateHTMLWorksheet(wks):
	# Converts Worksheet object, "wks" into an html/javascript file
	worksheet = "<!DOCTYPE html>\n<html>\n<head>\n<title>Dragoon Worksheet</title>\n<script type=\"text/javascript\">\nfunction checkAnswers(inputId, rightAnswer) {\nif (document.getElementById(inputId).value===rightAnswer) {\ndocument.getElementById(inputId).style.background=\"#66FF33\";\nreturn true;\n}\nelse {\ndocument.getElementById(inputId).style.background=\"#FF3333\";\nreturn false;\n}\n};\nvar tim1 = 0;\nfunction time1 () {\nif (yestim1=1){\ntim1 = tim1 + 1;\nt = setTimeout(function() {time1()},1000);\n}\n};\nvar yestim1 = 1;\ntime1();\n</script>\n</head>\n<body>"
	divset = ""
	endtbl = "<div id=\"resultsTable\" style=\"display:none\">\n<table>\n<thead>\n<td style=\"border: 2pt black solid\">Question</td>\n<td style=\"border: 2pt black solid\">Correct Answer</td>\n<td style=\"border: 2pt black solid\">Student Answers</td>\n<td style=\"border: 2pt black solid\">Number of Wrong Tries</td>\n<td style=\"border: 2pt black solid\">Time for Entire Question (s)</td>\n</thead>\n<tbody>"
	endfn = "<script type=\"text/javascript\">\nfunction displayAnswers () {\ndocument.getElementById(\"resultsTable\").style.display=\"\""
	alph = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
	rnum = ["i","ii","iii","iv","v","vi","vii","viii","ix","x","xi","xii","xiii","xiv","xv","xvi","xvii","xviii","xix","xx","xxi","xxii","xxiii","xxiv","xxv"]
	docname = wks.name + ".html"
	qno = 0
	for ques in wks.questions:
		qno = str(int(qno) + 1)
		for lse in wks.loose:
			if qno == lse.before:
				if lse.__class__.__name__ == "LsImage":
					worksheet = worksheet + "\n<img src =\"" + part.image + ".JPG\"/>"
				else:
					worksheet = worksheet + "\n<p>" + part.text + "</p>"
		contfn = "function cont" + qno + "() {\nvar yestim" + qno + " = 0;\ndocument.getElementById(\"" + qno + "Time\").innerHTML = tim" + qno + ";"
		chkans = ""
		chkcpl = "if ("
		contif = "if ("
		ctwrng = ""
		ctr = ""
		varset = "var set" + str(qno) + " = {"
		worksheet = worksheet + "\n<h3>Question " + qno + "</h3>\n<p>" + ques.gen + "</p>"
		alphindex = 0
		for sect in ques.sections:
			lno = alph[alphindex]
			alphindex = alphindex + 1
			worksheet = worksheet + "\n<p>" + qno + lno + ". "
			romannum = 0
			for part in sect.content:
				rno = rnum[romannum]
				romannum = romannum + 1
				if part.__class__.__name__ == "Dropdown":
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
					if lno == "a" and rno == "i":
						endtbl = endtbl + "<div id=\"" + qno + "Time\"></div></td>\n<tr>"
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
					#	print(head)
					#	for item in head:
						item = "\n<td style=\"border: 2pt black solid\">" + str(item) + "</td>"
						allhead = allhead + item
					for body in part.rows:
						print("row: "+str(body))
						for drdn in body:
							print("drdn: "+str(drdn))
							if isinstance(drdn, str):
								item = "\n<td style=\"border: 2pt black solid\">" + drdn + "</td>"
								allline = allline + item
							else:
								allans = ""
								rta = drdn[1]
								for choice in drdn[0]:
									option = "\n<option>" + str(choice) + "</option>"
									allans = allans + option
								varset = varset + "\n" + lno + rno + ":0,"
								chkans = chkans + "checkAnswers(\"" + qno + lno + rno + "\", \"" + rta + "\");"
								chkcpl = chkcpl + "document.getElementById(\"" + qno + lno + rno + "\").value===\"\" ||"
								ctr = ctr + "if (!checkAnswers(\"" + qno + lno + rno + "\", \"" + rta + "\")) { \n set" + qno + "." + lno + rno + " = set" + qno + "." + lno + rno + " + 1;}"
								contif = contif + "(checkAnswers(\"" + qno + lno + rno + "\", \"" + rta + "\") || set" + qno + "." + lno + rno + "===3) &&"
								ctwrng = ctwrng + "\nif (!checkAnswers(\"" + qno + lno + rno + "\", \"" + rta + "\")) {\nif (set" + qno + "." + lno + rno + "===3) {\ndocument.getElementById(\"" + qno + lno + rno + "\").value=\"" + rta + "\";\ndocument.getElementById(\"" + qno + lno + rno + "\").style.background=\"#FFFF00\"}\nif (set" + qno + "." + lno + rno + "=== 1) { \n document.getElementById(\"" + qno + lno + rno + "Answer1\").innerHTML = \"; \" + document.getElementById(\"" + qno + lno + rno + "\").value \n } \n else if (set" + qno + "." + lno + rno + "=== 2) { \n document.getElementById(\"" + qno + lno + rno + "Answer2\").innerHTML = \"; \" + document.getElementById(\"" + qno + lno + rno + "\").value \n } \n else { \n document.getElementById(\"" + qno + lno + rno + "Answer3\").innerHTML = \"; \" + document.getElementById(\"" + qno + lno + rno + "\").value \n } \n } \n else { \n if (set" + qno + "." + lno + rno + "=== 0) { \n document.getElementById(\"" + qno + lno + rno + "Answer1\").innerHTML = \"; \" + document.getElementById(\"" + qno + lno + rno + "\").value \n } \n else if (set" + qno + "." + lno + rno + "=== 1) { \n document.getElementById(\"" + qno + lno + rno + "Answer2\").innerHTML = \"; \" + document.getElementById(\"" + qno + lno + rno + "\").value \n } \n else { \n document.getElementById(\"" + qno + lno + rno + "Answer3\").innerHTML = \"; \" + document.getElementById(\"" + qno + lno + rno + "\").value\n}\n};"
								allline = allline + "<td style=\"border: 2pt black solid\"><select id=\"" + qno + lno + rno + "\">\n<option></option>" + allans + "</select></td>"
								endtbl = endtbl + "\n<tr>\n<td style=\"border: 2pt black solid\">" + qno + lno + ". " + rno + ".</td>\n<td style=\"border: 2pt black solid\">" + rta + "</td>\n<td style=\"border: 2pt black solid\"><div id=\"" + qno + lno + rno + "Answer1\"></div><div id=\"" + qno + lno + rno + "Answer2\"></div><div id=\"" + qno + lno + rno + "Answer3\"></div></td>\n<td style=\"border: 2pt black solid\"><div id=\"" + qno + lno + rno + "Tries\"></div></td>\n<td style=\"border: 2pt black solid\">"
								if lno == "a" and rno == "i":
									endtbl = endtbl + "<div id=\"" + qno + "Time\"></div></td>\n<tr>"
								else:
									endtbl = endtbl + "</td>\n</tr>"
								endfn = endfn + "\ndocument.getElementById(\"" + qno + lno + rno + "Tries\").innerHTML=set" + qno + "." + lno + rno + ";"
								rno = rnum[romannum]
								romannum = romannum + 1
								
						allline = allline + "</tr>"
					allbody = allbody + allline
						#line = input("Line: ").split(",")
					worksheet = worksheet + "<table>\n<thead>" + allhead + "\n</thead>\n<tbody>" + allbody + "\n</tbody>\n</table>"
				elif part.__class__.__name__ == "Text":
					worksheet = worksheet + "\n<p>" + part.text + "</p>"
				elif part.__class__.__name__ == "Image":
					worksheet = worksheet + "\n<img src =\"" + part.image + ".JPG\"/>"
		if int(qno) < len(list(wks.questions)):
			varset = varset + "}; \n"
			chkcpl = chkcpl + "0===1) {\n alert(\"It appears you have left at least one of these fields blank. Please remedy this immediately.\");\n}"
			contif = contif + "1===1) {\n document.getElementById(\"question" + str(int(qno)+1) + "\").style.display = \"\";\n document.getElementById(\"button" + qno + "\").style.display = \"none\";\ntim" + str(int(qno)+1) + "= 0;\nfunction time" + str(int(qno)+1) + "() {\nif (yestim" + str(int(qno)+1) + "){\ntim" + str(int(qno)+1) + " = tim" + str(int(qno)+1) + " + 1;\nt = setTimeout(function() {time" + str(int(qno)+1) + "()},1000);\n}\n};\nvar yestim" + str(int(qno)+1) + " = 1;\ntime" + str(int(qno)+1) + "();\n}"
			contfn = contfn + "\n" + chkans + "\n" + chkcpl + "\n" + ctr + "\n" + contif + "\n" + ctwrng
			worksheet = worksheet + "\n<script type=\"text/javascript\">" + varset + contfn + "};\n</script> \n <br><button id=\"button" + qno + "\" onClick=\"cont" + qno + "();\">Continue</button>\n<div id=\"question" + str(int(qno)+1) + "\" style=\"display: none\">"
			divset = divset + "</div>"
		else:
			varset = varset + "}; \n"
			chkcpl = chkcpl + "0===1) {\n alert(\"It appears you have left at least one of these fields blank. Please remedy this immediately.\");\n}"
			contif = contif + "1===1) {\n document.getElementById(\"question" + str(int(qno)+1) + "\").style.display = \"\";\n document.getElementById(\"button" + qno + "\").style.display = \"none\";\ndisplayAnswers();\n}"
			contfn = contfn + "\n" + chkans + "\n" + chkcpl + "\n" + ctr + "\n" + contif + "\n" + ctwrng
			worksheet = worksheet + "\n <script type=\"text/javascript\">" + varset + contfn + "};\n</script> \n <br><button id=\"button" + qno + "\" onClick=\"cont" + qno + "();\">Continue</button>\n<div id=\"question" + str(int(qno)+1) + "\" style=\"display: none\">"
			divset = divset + "</div>"
	endtbl = endtbl + "\n</tbody>\n</table>\n</div>"
	endfn = endfn + "\n};\n</script>"
	worksheet = worksheet + divset + endtbl + endfn + "</body></html>"
	open(docname,"w").write(worksheet)

######################
## Construct an example:
	
#with open("worksheet.json","w") as outfile:
	#json.dump(wk1,outfile,cls = CustomTypeEncoder, indent = 4)

def testload():
	with open("demo_worksheet.json","r") as outfile:
		wksht_dct = json.load(outfile)
		return CustomTypeDecoder(wksht_dct)
