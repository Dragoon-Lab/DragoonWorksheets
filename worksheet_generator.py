worksheet = "<!DOCTYPE html>\n<html>\n<head>\n<title>Dragoon Worksheet 1</title>\n<script type=\"text/javascript\">\nfunction checkAnswers(inputId, rightAnswer) {\nif (document.getElementById(inputId).value===rightAnswer) {\ndocument.getElementById(inputId).style.background=\"#66FF33\";\nreturn true;\n}\nelse {\ndocument.getElementById(inputId).style.background=\"#FF3333\";\nreturn false;\n}\n};\n</script>\n</head>\n<body>"
divset = ""
def newWorksheet ():
		global docname
		docname = input ("Document name: ") + ".html"
newWorksheet ()		
class Problem:
	def newQuestion ():
		global qno
		qno = str(input ("Question number: "))
		global gen
		gen = input ("General description: ")
		global contfn
		contfn = "function cont" + qno + "() {"
		global chkans
		chkans = ""
		global chkcpl
		chkcpl = "if ("
		global contif
		contif = "if ("
		global ctwrng
		ctwrng = ""
		global varset
		varset = "var set" + str(qno) + " = {"
		global worksheet
		worksheet = worksheet + "\n<h3>Question " + qno + "</h3>\n<p>" + gen + "</p>"
	def newSection ():
		global let
		global rta
		global allans
		let = input ("Letter: ")
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
				dno = input ("Number within section (lower case Roman numeral): ")
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
				varset = varset + "\n" + let + dno + ":0,"
				global chkans
				chkans = chkans + "checkAnswers(\"" + qno + let + dno + "\", \"" + rta + "\");"
				global chkcpl
				chkcpl = chkcpl + "document.getElementById(\"" + qno + let + dno + "\").value===\"\" ||"
				global contif
				contif = contif + "(checkAnswers(\"" + qno + let + dno + "\", \"" + rta + "\") || set" + qno + "." + let + dno + "===3) &&"
				global ctwrng
				ctwrng = ctwrng + "if (!checkAnswers(\"" + qno + let + dno + "\", \"" + rta + "\")) { \n set" + qno + "." + let + dno + " = set" + qno + "." + let + dno + " + 1; \n if (set" + qno + "." + let + dno + "=== 1) { \n document.getElementById(\"" + qno + let + dno + "Answer1\").innerHTML = \"; \" + document.getElementById(\"" + qno + let + dno + "\").value \n } \n else if (set" + qno + "." + let + dno + "=== 2) { \n document.getElementById(\"" + qno + let + dno + "Answer2\").innerHTML = \"; \" + document.getElementById(\"" + qno + let + dno + "\").value \n } \n else { \n document.getElementById(\"" + qno + let + dno + "Answer3\").innerHTML = \"; \" + document.getElementById(\"" + qno + let + dno + "\").value \n } \n } \n else { \n if (set" + qno + "." + let + dno + "=== 0) { \n document.getElementById(\"" + qno + let + dno + "Answer1\").innerHTML = \"; \" + document.getElementById(\"" + qno + let + dno + "\").value \n } \n else if (set" + qno + "." + let + dno + "=== 1) { \n document.getElementById(\"" + qno + let + dno + "Answer2\").innerHTML = \"; \" + document.getElementById(\"" + qno + let + dno + "\").value \n } \n else { \n document.getElementById(\"" + qno + let + dno + "Answer3\").innerHTML = \"; \" + document.getElementById(\"" + qno + let + dno + "\").value \n }"
				global worksheet
				worksheet = worksheet + "<select id=\"" + qno + let + dno + "\">\n<option></option>" + allans + "</select>"
				add = input ("Add: ")
			elif add == "table":
				head = input ("Table head: ").split(",")
				global allhead
				allhead = ""
				global allbody
				allbody = ""
				for item in head:
					item = "\n<td>" + str(item) + "</td>"
					global allhead
					allhead = allhead + item
				global head
				line = input ("Line: ").split(",")
				global allline
				allline = "<tr>"
				while not line == "end":
					for item in line:
						if item == "dropdown":
							dno = input ("Number within section (lower case Roman numeral): ")
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
							varset = varset + "\n" + let + dno + ":0,"
							global chkans
							chkans = chkans + "checkAnswers(\"" + qno + let + dno + "\", \"" + rta + "\");"
							global chkcpl
							chkcpl = chkcpl + "document.getElementById(\"" + qno + let + dno + "\").value===\"\" ||"
							global contif
							contif = contif + "(checkAnswers(\"" + qno + let + dno + "\", \"" + rta + "\") || set" + qno + "." + let + dno + "===3) &&"
							global ctwrng
							ctwrng = ctwrng + "if (!checkAnswers(\"" + qno + let + dno + "\", \"" + rta + "\")) { \n set" + qno + "." + let + dno + " = set" + qno + "." + let + dno + " + 1; \n if (set" + qno + "." + let + dno + "=== 1) { \n document.getElementById(\"" + qno + let + dno + "Answer1\").innerHTML = \"; \" + document.getElementById(\"" + qno + let + dno + "\").value \n } \n else if (set" + qno + "." + let + dno + "=== 2) { \n document.getElementById(\"" + qno + let + dno + "Answer2\").innerHTML = \"; \" + document.getElementById(\"" + qno + let + dno + "\").value \n } \n else { \n document.getElementById(\"" + qno + let + dno + "Answer3\").innerHTML = \"; \" + document.getElementById(\"" + qno + let + dno + "\").value \n } \n } \n else { \n if (set" + qno + "." + let + dno + "=== 0) { \n document.getElementById(\"" + qno + let + dno + "Answer1\").innerHTML = \"; \" + document.getElementById(\"" + qno + let + dno + "\").value \n } \n else if (set" + qno + "." + let + dno + "=== 1) { \n document.getElementById(\"" + qno + let + dno + "Answer2\").innerHTML = \"; \" + document.getElementById(\"" + qno + let + dno + "\").value \n } \n else { \n document.getElementById(\"" + qno + let + dno + "Answer3\").innerHTML = \"; \" + document.getElementById(\"" + qno + let + dno + "\").value \n }"
							global allline
							allline = allline + "<td><select id=\"" + qno + let + dno + "\">\n<option></option>" + allans + "</select></td>"
						else:
							item = "\n<td>" + str(item) + "</td>"
							global allline
							allline = allline + item
					global allline
					allline = allline + "</tr>"
					global allbody
					allbody = allbody + allline
					line = input("Line: ")
				global worksheet
				worksheet = worksheet + "<table>\n<thead>" + allhead + "\n</thead>\n<tbody>" + allbody + "\n</tbody>\n</table>"
				add = input ("Add: ")
			elif add == "checkbox":
				dno = input ("Number within section (lower case Roman numeral): ")
				ans = input ("Answers: ").split(",")
				rta = input ("Right answer: ")
				if not rta in ans:
					print("Please choose one of the given answers as the right answer.")
					rta = input ("Right answer: ")
				global allans	
				allans = ""
				for item in ans:
					item = "\n<input type=\"checkbox\" id=\"" + qno + let + dno + "\" value=\"" + str(item) + "\">" + str(item) + "<br>"
					global allans
					allans = allans + item	
				global varset
				varset = varset + "\n" + let + dno + ":0,"
				global chkans
				chkans = chkans + "checkAnswers(\"" + qno + let + dno + "\", \"" + rta + "\");"
				global chkcpl
				chkcpl = chkcpl + "document.getElementById(\"" + qno + let + dno + "\").value===\"\" ||"
				global contif
				contif = contif + "(checkAnswers(\"" + qno + let + dno + "\", \"" + rta + "\") || set" + qno + "." + let + dno + "===3) &&"
				global ctwrng
				ctwrng = ctwrng + "if (!checkAnswers(\"" + qno + let + dno + "\", \"" + rta + "\")) { \n set" + qno + "." + let + dno + " = set" + qno + "." + let + dno + " + 1; \n if (set" + qno + "." + let + dno + "=== 1) { \n document.getElementById(\"" + qno + let + dno + "Answer1\").innerHTML = \"; \" + document.getElementById(\"" + qno + let + dno + "\").value \n } \n else if (set" + qno + "." + let + dno + "=== 2) { \n document.getElementById(\"" + qno + let + dno + "Answer2\").innerHTML = \"; \" + document.getElementById(\"" + qno + let + dno + "\").value \n } \n else { \n document.getElementById(\"" + qno + let + dno + "Answer3\").innerHTML = \"; \" + document.getElementById(\"" + qno + let + dno + "\").value \n } \n } \n else { \n if (set" + qno + "." + let + dno + "=== 0) { \n document.getElementById(\"" + qno + let + dno + "Answer1\").innerHTML = \"; \" + document.getElementById(\"" + qno + let + dno + "\").value \n } \n else if (set" + qno + "." + let + dno + "=== 1) { \n document.getElementById(\"" + qno + let + dno + "Answer2\").innerHTML = \"; \" + document.getElementById(\"" + qno + let + dno + "\").value \n } \n else { \n document.getElementById(\"" + qno + let + dno + "Answer3\").innerHTML = \"; \" + document.getElementById(\"" + qno + let + dno + "\").value \n }"
				global worksheet
				worksheet = worksheet + "<select id=\"" + qno + let + dno + "\">\n<option></option>" + allans + "</select>"
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
		global contif
		contif = contif + "1===1) {\n document.getElementById(\"question" + str(int(qno)+1) + "\").style.display = \"\";\n document.getElementById(\"button" + qno + "\{).style.display = \"none\";\n}"
		global ctwrng
		contfn = contfn + "\n" + chkans + "\n" + chkcpl + "\n" + contif + "\n" + ctwrng + "};"
		global worksheet
		worksheet = worksheet + "\n <script type=\"text/javascript\">" + varset + contfn + "</script> \n <button id=\"button" + qno + "\" onClick=\"cont" + qno + "();\">Question " + str(int(qno)+1) + "</button><div id=\"question" + str(int(qno)+1) + "\" style=\"display: none\">"
		global divset
		divset = divset + "</div>"
	def generate ():
		global worksheet
		worksheet = worksheet + divset + "</body></html>"
		open(docname,"w").write(worksheet)