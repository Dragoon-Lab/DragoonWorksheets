import json
class Worksheet:
	def __init__(self, filename):
		self.name = filename
		self.questions = []#list of questions
	def jsonable(self):
		return self.__dict__
class Question:
	def __init__ (self,wkst):
		self.gen = input ("General description: ")
		self.sections = []
		wkst.questions.append(self)
	def jsonable(self):
		return self.__dict__
		
class Section:
	def __init__ (self,qstn):
		self.content = []#list of text,images,dropdown,table
		qstn.sections.append(self)
	def jsonable(self):
		return self.__dict__
		
class Table:
	def __init__(self,sect):
		self.header = input ("Header: ").split(",")
		self.rows = []
		line = input("Line: ").split(",")
		while not "end" in line:
			for item in line:
				if item == "dropdown":
					ans = input ("Answers: ").split(",")
					rta = input ("Right answer: ")
					if not rta in ans:
						print("Please choose one of the given answers as the right answer.")
						rta = input ("Right answer: ")
					print (ans) 	
			self.rows.append(line)			
			line = input ("Line: ").split(",")			
		sect.content.append(self)				
							
	def jsonable(self):
		return self.__dict__
		
class Dropdown:
	def __init__(self,sect):
		self.options = input ("Answers: ").split(",")
		self.correct = input ("Right answer: ")
		if not self.correct in self.options:
			print("Please choose one of the given answers as the right answer.")
			self.correct = input ("Right answer: ")
		sect.content.append(self)	
	def jsonable(self):
		return self.__dict__
	
def getJsonable(obj):
    if hasattr(obj, 'jsonable'):
        return obj.jsonable()
    else:
        raise (TypeError, 'Object of type %s with value of %s is not JSON serializable')

######################
# Generator functions

		

def generateHTMLWorksheet(wks):
	# Converts Worksheet object, "wks" into an html/javascript file
	worksheet = "<!DOCTYPE html>\n<html>\n<head>\n<title>Dragoon Worksheet 1</title>\n<script type=\"text/javascript\">\nfunction checkAnswers(inputId, rightAnswer) {\nif (document.getElementById(inputId).value===rightAnswer) {\ndocument.getElementById(inputId).style.background=\"#66FF33\";\nreturn true;\n}\nelse {\ndocument.getElementById(inputId).style.background=\"#FF3333\";\nreturn false;\n}\n};\nvar tim1 = 0;\nfunction time1 () {\nif (yestim1=1){\ntim1 = tim1 + 1;\nt = setTimeout(function() {time1()},1000);\n}\n};\nvar yestim1 = 1;\ntime1();\n</script>\n</head>\n<body>"
	alph = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
	rnum = ["i","ii","iii","iv","v","vi","vii","viii","ix","x","xi","xii","xiii","xiv","xv","xvi","xvii","xviii","xix","xx","xxi","xxii","xxiii","xxiv","xxv"]
	for item in wks.questions:#These items are questions.
		ques = item
		qno = str(wks.index(ques) + 1)
		contfn = "function cont" + qno + "() {\nvar yestim" + qno + " = 0;\ndocument.getElementById(\"" + qno + "Time\").innerHTML = tim" + qno + ";"
		chkans = ""
		chkcpl = "if ("
		contif = "if ("
		ctwrng = ""
		ctr = ""
		varset = "var set" + str(qno) + " = {"
		worksheet = worksheet + "\n<h3>Question " + qno + "</h3>\n<p>" + gen + "</p>"
		for item in ques:#These items are sections.
			sect = item
			lno = alph[ques.index(sect)]
			worksheet = worksheet + "\n<p>" + qno + lno + ". "
			for item in sect:#These items are parts.
				part = item
				rno = rnum[sect.index(part)]
				if part.__class__.__name__ == "Dropdown":
					allans = ""
					for item in part.options:
						item = "\n<option>" + str(item) + "</option>"
						allans = allans + item
					varset = varset + "\n" + lno + rno + ":0,"
					chkans = chkans + "checkAnswers(\"" + qno + lno + rno + "\", \"" + item.correct + "\");"
					chkcpl = chkcpl + "document.getElementById(\"" + qno + lno + rno + "\").value===\"\" ||"
					ctr = ctr + "if (!checkAnswers(\"" + qno + lno + rno + "\", \"" + rta + "\")) { \n set" + qno + "." + lno + rno + " = set" + qno + "." + lno + rno + " + 1;}"
					contif = contif + "(checkAnswers(\"" + qno + lno + rno + "\", \"" + rta + "\") || set" + qno + "." + lno + rno + "===3) &&"
					ctwrng = ctwrng + "\nif (!checkAnswers(\"" + qno + lno + rno + "\", \"" + rta + "\")) {\nif (set" + qno + "." + lno + rno + "===3) {\ndocument.getElementById(\"" + qno + lno + rno + "\").value=\"" + rta + "\";\ndocument.getElementById(\"" + qno + lno + rno + "\").style.background=\"#FFFF00\"}\nif (set" + qno + "." + lno + rno + "=== 1) { \n document.getElementById(\"" + qno + lno + rno + "Answer1\").innerHTML = \"; \" + document.getElementById(\"" + qno + lno + rno + "\").value \n } \n else if (set" + qno + "." + lno + rno + "=== 2) { \n document.getElementById(\"" + qno + lno + rno + "Answer2\").innerHTML = \"; \" + document.getElementById(\"" + qno + lno + rno + "\").value \n } \n else { \n document.getElementById(\"" + qno + lno + rno + "Answer3\").innerHTML = \"; \" + document.getElementById(\"" + qno + lno + rno + "\").value \n } \n } \n else { \n if (set" + qno + "." + lno + rno + "=== 0) { \n document.getElementById(\"" + qno + lno + rno + "Answer1\").innerHTML = \"; \" + document.getElementById(\"" + qno + lno + rno + "\").value \n } \n else if (set" + qno + "." + lno + rno + "=== 1) { \n document.getElementById(\"" + qno + lno + rno + "Answer2\").innerHTML = \"; \" + document.getElementById(\"" + qno + lno + rno + "\").value \n } \n else { \n document.getElementById(\"" + qno + lno + rno + "Answer3\").innerHTML = \"; \" + document.getElementById(\"" + qno + lno + rno + "\").value\n}\n};"
					worksheet = worksheet + "<select id=\"" + qno + lno + rno + "\">\n<option></option>" + allans + "</select>"
					endtbl = endtbl + "\n<tr>\n<td style=\"border: 2pt black solid\">" + qno + lno + ". " + rno + ".</td>\n<td style=\"border: 2pt black solid\">" + rta + "</td>\n<td style=\"border: 2pt black solid\"><div id=\"" + qno + lno + rno + "Answer1\"></div><div id=\"" + qno + lno + rno + "Answer2\"></div><div id=\"" + qno + lno + rno + "Answer3\"></div></td>\n<td style=\"border: 2pt black solid\"><div id=\"" + qno + lno + rno + "Tries\"></div></td>\n<td style=\"border: 2pt black solid\">"
					if lno == "a" and rno == "i":
						endtbl = endtbl + "<div id=\"" + qno + "Time\"></div></td>\n<tr>"
					else:
						endtbl = endtbl + "</td>\n</tr>"
					endfn = endfn + "\ndocument.getElementById(\"" + qno + let + rno + "Tries\").innerHTML=set" + qno + "." + let + rno + ";"
				elif part.__class__.__name__ == "Table":
					pass

		
######################
## Construct an example:

wk1 = Worksheet("testworksheet")

#wk1.questions.append(qstn1)  
generateHTMLWorksheet(wk1)
	
#with open("worksheet.json","w") as outfile:
	#json.dump(wk1,outfile,default = getJsonable, indent = 4)

#How would I be able to add loose text and pictures?	