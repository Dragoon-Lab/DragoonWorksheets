worksheet = "<!DOCTYPE html>\n<html>\n<head>\n<title>Dragoon Worksheet 1</title>\n<script type=\"text/javascript\">\nfunction checkAnswers(inputId, rightAnswer) {\nif (document.getElementById(inputId).value===rightAnswer) {\ndocument.getElementById(inputId).style.background=\"#66FF33\";\nreturn true;\n}\nelse {\ndocument.getElementById(inputId).style.background=\"#FF3333\";\nreturn false;\n}\n};\nvar tim1 = 0;\nfunction time1 () {\nif (yestim1=1){\ntim1 = tim1 + 1;\nt = setTimeout(function() {time1()},1000);\n}\n};\nvar yestim1 = 1;\ntime1();\n</script>\n</head>\n<body>"
divset = ""
endtbl = "<div id=\"resultsTable\" style=\"display:none\">\n<table>\n<thead>\n<td style=\"border: 2pt black solid\">Question</td>\n<td style=\"border: 2pt black solid\">Correct Answer</td>\n<td style=\"border: 2pt black solid\">Student Answers</td>\n<td style=\"border: 2pt black solid\">Number of Tries</td>\n<td style=\"border: 2pt black solid\">Time for Entire Question (s)</td>\n</thead>\n<tbody>"
endfn = "<script type=\"text/javascript\">\nfunction displayAnswers () {\ndocument.getElementById(\"resultsTable\").style.display=\"\""
qno = 0
alph = [0,"a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
rnum = [0,"i","ii","iii","iv","v","vi","vii","viii","ix","x","xi","xii","xiii","xiv","xv","xvi","xvii","xviii","xix","xx","xxi","xxii","xxiii","xxiv","xxv"]
def newWorksheet ():
		global docname
		docname = input ("Document name: ") + ".html"
newWorksheet ()		
def newQuestion ():
	global qno
	qno = str(int(qno)+1)
	global lno
	lno = 0
	global gen
	gen = input ("General description: ")
	global contfn
	contfn = "function cont" + qno + "() {\nvar yestim" + qno + " = 0;\ndocument.getElementById(\"" + qno + "Time\").innerHTML = tim" + qno + ";"
	global chkans
	chkans = ""
	global chkcpl
	chkcpl = "if ("
	global contif
	contif = "if ("
	global ctwrng
	ctwrng = ""
	global ctr
	ctr = ""
	global varset
	varset = "var set" + str(qno) + " = {"
	global worksheet
	worksheet = worksheet + "\n<h3>Question " + qno + "</h3>\n<p>" + gen + "</p>"
def text():
	global worksheet
	lstext = input ("Text: ")
	worksheet = worksheet + "\n<p>" + lstext + "</p>"
def image ():
	global worksheet
	imfile = input ("File folder/name: ")
	worksheet = worksheet + "\n<img src=\"" + imfile + ".JPG\"/>"
def newSection ():
	global lno
	lno = lno + 1
	global let
	global rta
	global allans
	let = alph[lno]
	global dno
	dno = 0
	global worksheet
	worksheet = worksheet + "\n<p>" + qno + let + ". "
	add = input ("Add: ")
	while not add == "end":
		if add == "text":
			global txt
			txt = input ("Text: ")
			worksheet = worksheet + txt
			add = input ("Add: ")
		elif add == "dropdown":
			global dno
			dno = dno + 1
			rno = rnum[dno]
			ans = input ("Answers: ").split(",")
			rta = input ("Right answer: ")
			if not rta in ans:
				print("Please choose one of the given answers as the right answer.")
				rta = input ("Right answer: ")
			global allans	
			allans = ""
			for item in ans:
				item = "\n<option>" + str(item) + "</option>"
				global allans
				allans = allans + item	
			global varset
			varset = varset + "\n" + let + rno + ":0,"
			global chkans
			chkans = chkans + "checkAnswers(\"" + qno + let + rno + "\", \"" + rta + "\");"
			global chkcpl
			chkcpl = chkcpl + "document.getElementById(\"" + qno + let + rno + "\").value===\"\" ||"
			global ctr
			ctr = ctr + "if (!checkAnswers(\"" + qno + let + rno + "\", \"" + rta + "\")) { \n set" + qno + "." + let + rno + " = set" + qno + "." + let + rno + " + 1;}"
			global contif
			contif = contif + "(checkAnswers(\"" + qno + let + rno + "\", \"" + rta + "\") || set" + qno + "." + let + rno + "===3) &&"
			global ctwrng
			ctwrng = ctwrng + "\nif (!checkAnswers(\"" + qno + let + rno + "\", \"" + rta + "\")) {\nif (set" + qno + "." + let + rno + "===3) {\ndocument.getElementById(\"" + qno + let + rno + "\").value=\"" + rta + "\";\ndocument.getElementById(\"" + qno + let + rno + "\").style.background=\"#FFFF00\"}\nif (set" + qno + "." + let + rno + "=== 1) { \n document.getElementById(\"" + qno + let + rno + "Answer1\").innerHTML = \"; \" + document.getElementById(\"" + qno + let + rno + "\").value \n } \n else if (set" + qno + "." + let + rno + "=== 2) { \n document.getElementById(\"" + qno + let + rno + "Answer2\").innerHTML = \"; \" + document.getElementById(\"" + qno + let + rno + "\").value \n } \n else { \n document.getElementById(\"" + qno + let + rno + "Answer3\").innerHTML = \"; \" + document.getElementById(\"" + qno + let + rno + "\").value \n } \n } \n else { \n if (set" + qno + "." + let + rno + "=== 0) { \n document.getElementById(\"" + qno + let + rno + "Answer1\").innerHTML = \"; \" + document.getElementById(\"" + qno + let + rno + "\").value \n } \n else if (set" + qno + "." + let + rno + "=== 1) { \n document.getElementById(\"" + qno + let + rno + "Answer2\").innerHTML = \"; \" + document.getElementById(\"" + qno + let + rno + "\").value \n } \n else { \n document.getElementById(\"" + qno + let + rno + "Answer3\").innerHTML = \"; \" + document.getElementById(\"" + qno + let + rno + "\").value\n}\n};"
			global worksheet
			worksheet = worksheet + "<select id=\"" + qno + let + rno + "\">\n<option></option>" + allans + "</select>"
			global endtbl
			endtbl = endtbl + "\n<tr>\n<td style=\"border: 2pt black solid\">" + qno + let + ". " + rno + ".</td>\n<td style=\"border: 2pt black solid\">" + rta + "</td>\n<td style=\"border: 2pt black solid\"><div id=\"" + qno + let + rno + "Answer1\"></div><div id=\"" + qno + let + rno + "Answer2\"></div><div id=\"" + qno + let + rno + "Answer3\"></div></td>\n<td style=\"border: 2pt black solid\"><div id=\"" + qno + let + rno + "Tries\"></div></td>\n<td style=\"border: 2pt black solid\">"
			if let == "a" and rno == "i":
				endtbl = endtbl + "<div id=\"" + qno + "Time\"></div></td>\n<tr>"
			else:
				endtbl = endtbl + "</td>\n</tr>"
			global endfn
			endfn = endfn + "\ndocument.getElementById(\"" + qno + let + rno + "Tries\").innerHTML=set" + qno + "." + let + rno + ";"
			add = input ("Add: ")
		elif add == "table":
			head = input ("Table head: ").split(",")
			global allhead
			allhead = ""
			global allbody
			allbody = ""
			for item in head:
				item = "\n<td style=\"border: 2pt black solid\">" + str(item) + "</td>"
				global allhead
				allhead = allhead + item
			global head
			line = input ("Line: ").split(",")
			while not "end" in line:
				global allline
				allline = ""
				for item in line:
					if item == "dropdown":
						global dno
						dno = dno + 1
						rno = rnum[dno]
						ans = input ("Answers: ").split(",")
						rta = input ("Right answer: ")
						if not rta in ans:
							print("Please choose one of the given answers as the right answer.")
							rta = input ("Right answer: ")
						global allans	
						allans = ""
						for item in ans:
							item = "\n<option>" + str(item) + "</option>"
							global allans
							allans = allans + item	
						global varset
						varset = varset + "\n" + let + rno + ":0,"
						global chkans
						chkans = chkans + "checkAnswers(\"" + qno + let + rno + "\", \"" + rta + "\");"
						global chkcpl
						chkcpl = chkcpl + "document.getElementById(\"" + qno + let + rno + "\").value===\"\" ||"
						global ctr
						ctr = ctr + "if (!checkAnswers(\"" + qno + let + rno + "\", \"" + rta + "\")) { \n set" + qno + "." + let + rno + " = set" + qno + "." + let + rno + " + 1;}"
						global contif
						contif = contif + "(checkAnswers(\"" + qno + let + rno + "\", \"" + rta + "\") || set" + qno + "." + let + rno + "===3) &&"
						global ctwrng
						ctwrng = ctwrng + "\nif (!checkAnswers(\"" + qno + let + rno + "\", \"" + rta + "\")) {\nif (set" + qno + "." + let + rno + "===3) {\ndocument.getElementById(\"" + qno + let + rno + "\").value=\"" + rta + "\";\ndocument.getElementById(\"" + qno + let + rno + "\").style.background=\"#FFFF00\"}\nif (set" + qno + "." + let + rno + "=== 1) { \n document.getElementById(\"" + qno + let + rno + "Answer1\").innerHTML = \"; \" + document.getElementById(\"" + qno + let + rno + "\").value \n } \n else if (set" + qno + "." + let + rno + "=== 2) { \n document.getElementById(\"" + qno + let + rno + "Answer2\").innerHTML = \"; \" + document.getElementById(\"" + qno + let + rno + "\").value \n } \n else { \n document.getElementById(\"" + qno + let + rno + "Answer3\").innerHTML = \"; \" + document.getElementById(\"" + qno + let + rno + "\").value \n } \n } \n else { \n if (set" + qno + "." + let + rno + "=== 0) { \n document.getElementById(\"" + qno + let + rno + "Answer1\").innerHTML = \"; \" + document.getElementById(\"" + qno + let + rno + "\").value \n } \n else if (set" + qno + "." + let + rno + "=== 1) { \n document.getElementById(\"" + qno + let + rno + "Answer2\").innerHTML = \"; \" + document.getElementById(\"" + qno + let + rno + "\").value \n } \n else { \n document.getElementById(\"" + qno + let + rno + "Answer3\").innerHTML = \"; \" + document.getElementById(\"" + qno + let + rno + "\").value\n}\n};"
						global allline
						allline = allline + "<td style=\"border: 2pt black solid\"><select id=\"" + qno + let + rno + "\">\n<option></option>" + allans + "</select></td>"
						global endtbl
						endtbl = endtbl + "\n<tr>\n<td style=\"border: 2pt black solid\">" + qno + let + ". " + rno + ".</td>\n<td style=\"border: 2pt black solid\">" + rta + "</td>\n<td style=\"border: 2pt black solid\"><div id=\"" + qno + let + rno + "Answer1\"></div><div id=\"" + qno + let + rno + "Answer2\"></div><div id=\"" + qno + let + rno + "Answer3\"></div></td>\n<td style=\"border: 2pt black solid\"><div id=\"" + qno + let + rno + "Tries\"></div></td>\n<td style=\"border: 2pt black solid\">"
						if let == "a" and rno == "i":
							endtbl = endtbl + "<div id=\"" + qno + "Time\"></div></td>\n<tr>"
						else:
							endtbl = endtbl + "</td>\n<tr>"
						global endfn
						endfn = endfn + "\ndocument.getElementById(\"" + qno + let + rno + "Tries\").innerHTML=set" + qno + "." + let + rno + ";"
					else:
						item = "\n<td style=\"border: 2pt black solid\">" + str(item) + "</td>"
						global allline
						allline = allline + item
				global allline
				allline = allline + "</tr>"
				global allbody
				allbody = allbody + allline
				line = input("Line: ").split(",")
			global worksheet
			worksheet = worksheet + "<table>\n<thead>" + allhead + "\n</thead>\n<tbody>" + allbody + "\n</tbody>\n</table>"
			add = input ("Add: ")
		elif add == "checkbox":
			global dno
			dno = dno + 1
			rno = rnum[dno]
			ans = input ("Answers: ").split(",")
			rta = input ("Right answers: ")
			if not rta in ans:
				print("Please choose one of the given answers as the right answer.")
				rta = input ("Right answer: ")
			global allans
			allans = ""
			for item in ans:
				item = "\n<input type=\"checkbox\" name=\"" + qno + let + rno + "\" id=\"" + str(item) + "\">" + str(item) + "<br>"
				global allans
				allans = allans + item	
			global varset
			varset = varset + "\n" + let + rno + ":0,"
			global chkans
			chkans = chkans + "if "
			global ctr
			ctr = ctr + "if (!checkAnswers(\"" + qno + let + rno + "\", \"" + rta + "\")) { \n set" + qno + "." + let + rno + " = set" + qno + "." + let + rno + " + 1;}"
			global contif
			contif = contif + "(checkAnswers(\"" + qno + let + rno + "\", \"" + rta + "\") || set" + qno + "." + let + rno + "===3) &&"
			global ctwrng
			ctwrng = ctwrng + "\nif (!checkAnswers(\"" + qno + let + rno + "\", \"" + rta + "\")) {\nif (set" + qno + "." + let + rno + "===3) {\ndocument.getElementById(\"" + qno + let + rno + "\").value=\"" + rta + "\";\ndocument.getElementById(\"" + qno + let + rno + "\").style.background=\"#FFFF00\"}\nif (set" + qno + "." + let + rno + "=== 1) { \n document.getElementById(\"" + qno + let + rno + "Answer1\").innerHTML = \"; \" + document.getElementById(\"" + qno + let + rno + "\").value \n } \n else if (set" + qno + "." + let + rno + "=== 2) { \n document.getElementById(\"" + qno + let + rno + "Answer2\").innerHTML = \"; \" + document.getElementById(\"" + qno + let + rno + "\").value \n } \n else { \n document.getElementById(\"" + qno + let + rno + "Answer3\").innerHTML = \"; \" + document.getElementById(\"" + qno + let + rno + "\").value \n } \n } \n else { \n if (set" + qno + "." + let + rno + "=== 0) { \n document.getElementById(\"" + qno + let + rno + "Answer1\").innerHTML = \"; \" + document.getElementById(\"" + qno + let + rno + "\").value \n } \n else if (set" + qno + "." + let + rno + "=== 1) { \n document.getElementById(\"" + qno + let + rno + "Answer2\").innerHTML = \"; \" + document.getElementById(\"" + qno + let + rno + "\").value \n } \n else { \n document.getElementById(\"" + qno + let + rno + "Answer3\").innerHTML = \"; \" + document.getElementById(\"" + qno + let + rno + "\").value\n}\n};"
			global worksheet
			worksheet = worksheet + allans
			global endtbl
			endtbl = endtbl + "\n<tr>\n<td style=\"border: 2pt black solid\">" + qno + let + ". " + rno + ".</td>\n<td style=\"border: 2pt black solid\">" + rta + "</td>\n<td style=\"border: 2pt black solid\"><div id=\"" + qno + let + rno + "Answer1\"></div><div id=\"" + qno + let + rno + "Answer2\"></div><div id=\"" + qno + let + rno + "Answer3\"></div></td>\n<td style=\"border: 2pt black solid\"><div id=\"" + qno + let + rno + "Tries\"></div></td>\n<td style=\"border: 2pt black solid\">"
			if let == "a" and rno == "i":
				endtbl = endtbl + "<div id=\"" + qno + "Time\"></div></td>\n<tr>"
			else:
				endtbl = endtbl + "</td>\n<tr>"
			global endfn
			endfn = endfn + "\ndocument.getElementById(\"" + qno + let + rno + "Tries\").innerHTML=set" + qno + "." + let + rno + ";"
			add = input ("Add: ")
		else:
			print ("That is not a valid input. Please write, \"text,\" \"dropdown,\" \"checkbox,\" \"table,\" or \"end\".")
			add = input ("Add: ")
def endQuestion ():
	global varset
	varset = varset + "}; \n"
	global contfn
	global chkans
	global chkcpl
	chkcpl = chkcpl + "0===1) {\n alert(\"It appears you have left at least one of these fields blank. Please remedy this immediately.\");\n}"
	global ctr
	global contif
	contif = contif + "1===1) {\n document.getElementById(\"question" + str(int(qno)+1) + "\").style.display = \"\";\n document.getElementById(\"button" + qno + "\").style.display = \"none\";\ntim" + str(int(qno)+1) + "= 0;\nfunction time" + str(int(qno)+1) + "() {\nif (yestim" + str(int(qno)+1) + "){\ntim" + str(int(qno)+1) + " = tim" + str(int(qno)+1) + " + 1;\nt = setTimeout(function() {time" + str(int(qno)+1) + "()},1000);\n}\n};\nvar yestim" + str(int(qno)+1) + " = 1;\ntime" + str(int(qno)+1) + "();\n}"
	global ctwrng
	contfn = contfn + "\n" + chkans + "\n" + chkcpl + "\n" + ctr + "\n" + contif + "\n" + ctwrng
	global worksheet
	worksheet = worksheet + "\n<script type=\"text/javascript\">" + varset + contfn + "};\n</script> \n <br><button id=\"button" + qno + "\" onClick=\"cont" + qno + "();\">Continue</button>\n<div id=\"question" + str(int(qno)+1) + "\" style=\"display: none\">"
	global divset
	divset = divset + "</div>"
def lastQuestion ():
	global varset
	varset = varset + "}; \n"
	global contfn
	global chkans
	global chkcpl
	chkcpl = chkcpl + "0===1) {\n alert(\"It appears you have left at least one of these fields blank. Please remedy this immediately.\");\n}"
	global ctr
	global contif
	contif = contif + "1===1) {\n document.getElementById(\"question" + str(int(qno)+1) + "\").style.display = \"\";\n document.getElementById(\"button" + qno + "\").style.display = \"none\";\ndisplayAnswers();\n}"
	global ctwrng
	contfn = contfn + "\n" + chkans + "\n" + chkcpl + "\n" + ctr + "\n" + contif + "\n" + ctwrng
	global worksheet
	worksheet = worksheet + "\n <script type=\"text/javascript\">" + varset + contfn + "};\n</script> \n <br><button id=\"button" + qno + "\" onClick=\"cont" + qno + "();\">Continue</button>\n<div id=\"question" + str(int(qno)+1) + "\" style=\"display: none\">"
	global divset
	divset = divset + "</div>"
def generate ():
	global endtbl
	endtbl = endtbl + "\n</tbody>\n</table>\n</div>"
	global endfn
	endfn = endfn + "\n};\n</script>"
	global worksheet
	worksheet = worksheet + divset + endtbl + endfn + "</body></html>"
	open(docname,"w").write(worksheet)
	
'''
Must get done soon:
-Test checkbox and clean up
-wrong function name for time(#); stray 1
'''	