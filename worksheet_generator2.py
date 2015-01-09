import json
class Worksheet:
	def __init__(self, filename):
		self.name = filename
		self.questions = []#list of questions
	def jsonable(self):
		return self.__dict__
class Question:
	def __init__ (self):
		self.gen = input ("General description: ")
		self.sections = []
	def jsonable(self):
		return self.__dict__
		
class Section:
	def __init__ (self):
		self.content = []#list of text,images,dropdown,table
	def jsonable(self):
		return self.__dict__
		
class Table:
	def __init__(self):
		self.header = input ("Header: ")
		self.rows = []#list of lists ; one list per row inside the row: strings and dropdowns
	def jsonable(self):
		return self.__dict__
		
class Dropdown:
	def __init__(self):
		self.options = []
		self.correct = ""
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
	pass

		
######################
## Construct an example:

wk1 = Worksheet("testworksheet")

#wk1.questions.append(qstn1)  
generateHTMLWorksheet(wk1)
	
#with open("worksheet.json","w") as outfile:
	#json.dump(wk1,outfile,default = getJsonable, indent = 4)