DragoonWorksheets
=================

Webified versions of Dragoon worksheets

Edited by Mackenzie

###Introduction

The worksheet generator is divided into two parts. The first part defines the classes for the components of the worksheet, and the second part contains the functions used in storing the worksheet object as a JSON, retrieving the worksheet object from a JSON, and creating a worksheet using the worksheet object. It is a Python file; thus, in order to run it, you first need to download Python, which can be done from [this webpage](https://www.python.org/downloads/). Since the program is written using Python 3, it would be best to download that version. To begin a worksheet, open `worksheet_generator2.py` in the Python IDLE.

Start by creating an instance of the class `Worksheet`. To create an instance of a class, type: [name] = [class](\[arguments\]). For example, typing, `wkst = Worksheet("Intro_Worksheet")` will create an object of class `Worksheet` with the name `wkst` and with `"Intro_Worksheet"` as its only argument. To add contents to the worksheet, create instances of the classes listed below.

Once the worksheet is complete, convert it into a JSON file using the `generateJSON` function to save it. JSON is a way of storing objects so that both humans and computers can easily read them. This step is not necessary for creating a worksheet, but it allows for editing of the content of the worksheet without creating a worksheet object from scratch.

From this point, you can generate a [worksheet](worksheet.md) using the `generateHTMLWorksheet` function. If the worksheet object is still open, the function can take its name as an argument. If the worksheet object has been converted to a JSON file, this function can take the function `loadWorksheet` as an argument, where the argument for `loadWorksheet` is the name of the JSON file (including ".json").

###Classes

**Worksheet**

Every worksheet object created by the generator has three parts: a filename, a list of questions, and a list of loose content. The filename is for the HTML file that will eventually be created. It is given to the worksheet object as an argument for the initialization function and must be in quotes. For example, typing, `wkst = Worksheet(“Intro_Worksheet”)` will create a worksheet object called “wkst” with the HTML filename “Intro_Worksheet”. You do not need to end the filename with “.html” because the generator adds that automatically. Every time “wkst” is entered as the argument for the initialization function of an object of class “LsText”, “LsImage”, or “Question”, that object will be appended to one of wkst’s lists.

**LsText**

The class “LsText” is for text that is not part of any particular question, for example, introductory text that comes before the first question. Loose text is placed in the document according to the question number, which is the number of the question that the text will precede. Loose elements, both text and pictures, are placed onto the same list, so multiple elements preceding the same question will appear on the document in the order in which they were created. Loose elements will be appended to their worksheets’ “loose” lists.

The argument for the initialization function for LsText objects is the name of the worksheet to which it is to be appended. For example, typing, `LsText(wkst)` will create a loose-text object that is appended to wkst’s “loose” list. Upon creating an instance of class “LsText”, you will be prompted for the number of the question it precedes. Enter an integer. Next, you will be prompted for the actual text to be placed before the question. When the worksheet is being generated, this text will be inserted directly into the body of the HTML document, so any tags or coded characters will be displayed on the worksheet as they would be in any HTML document.

**LsImage**

The class “LsImage” is for images that are not part of any particular question, for example, introductory content that comes before the first question. Loose images are placed in the document according to the question numbers, which are the numbers of the questions that the loose images will precede. Loose elements, both text and pictures, are placed onto the same list, so multiple elements preceding the same question will appear on the document in the order in which they were created. Loose elements will be appended to their worksheets’ “loose” lists.

The argument for the initialization function for LsImage objects is the name of the worksheet to which it is to be appended. For example, typing, `LsImage(wkst)` will create a loose-image object that is appended to wkst’s “loose” list. Upon creating an instance of class “LsImage”, you will be prompted for the number of the question it precedes. Enter an integer. Next, you will be prompted for the file and folder name of the image to be inserted. Enter this information in the same format as the prompt, i.e., the folder name, followed by a slash, followed by the file name.

**Question**

The class “Question” is for the individual questions in the worksheet. At the end of each question, the students’ answers are checked, and the student cannot continue unless the all parts of the question are complete and the answers are correct. Every question has two parts: the subheading and a list of sections.

The argument for the initialization function for Question objects is the name of the worksheet to which it is being appended. For example, typing, `qs1 = Question(wkst)` will create a question object that is appended to wkst’s “questions” list. Upon creating an instance of class “Question”, you will be prompted for the subheading. This will appear at the top of the question and will be larger than the rest of the text, so keep the subheading short. Entering the name of the question as the argument for the initialization function for a section will append that section to that question’s list.

**Section**

Each section will start on a new line, but the elements inside the sections will not, unless they are images. The argument for the initialization function for Section objects is the name of the question. For example, typing, `scta = Section(qs1)` will create a section object that is appended to qs1’s “sections” list. Creating an instance of class “Section” does not make the program prompt you for any more information because each section only has one element, which is a list of content. For all of the classes listed below, entering the name of the section as the argument for the initialization function will append it to this list.

**Text**

Each object of class “Text” has only one part, and that is the text itself. The text entered in response to the “Text: ” prompt will not necessarily start on a new line unless it is the first element in a section. However, the text is inserted directly into the worksheet document, so HTML tags and coded characters in the response will ultimately show as they would in any HTML document.

**Image**

Each object of class “Image” only has one part, and that is the filename of the image. Upon creating an instance of class “Image”, you will be prompted for the names of the folder and file. Enter this information in the same format as the prompt, i.e., the folder name, followed by a slash, followed by the file name. Each image will start on a new line, as will the content immediately following the image.

**Dragoon**

Each object of class “Dragoon” has two parts: the problem name and the mode. Upon creating an instance of the class “Dragoon”, you will be prompted for the problem name and the mode. It doesn’t matter which letters are capitalized in the entry for mode, since the program capitalizes all of them automatically.

**Dropdown**

Upon creating an instance of the the class “Dropdown”, you will be prompted for answers. Type in all the possible answers from which the user will choose, and separate them with commas. you will then be prompted for the right answer, which you should write exactly the way it was written when entering the options. If it is different from each of the elements in the list of possible answers, the program will not accept it and will ask for another one.

**Table**

Each object of class “Table” has two parts: the header and the body. The header is a list, and the body is a list of lists. As you type in each line, the line, which is itself a list, gets appended to the list of lines. Upon creating an instance of the class “Table”, you will be prompted to submit a header by typing every category name, separated by commas. Upon submitting the header, the user will be asked for the content of the first line of the rest of the table. This is submitted the same way as is the header, except, if one of the items in the list is the word “dropdown,” you will be prompted for all the content in that particular cell. Type it as a list of dropdown boxes and text, where “dropdown” is again a placeholder for a dropdown box. For example, if a cell contains the following: “REE = [dropdown] - [dropdown] + [dropdown]”, you should enter, “REE = ,dropdown, - ,dropdown, + ,dropdown”. Of course, if the cell contains only one dropdown box and no text, you should just enter, “dropdown”. Then, you will be prompted to provide the possible answers and the correct answer in the same manner as in creating the dropdown boxes, which was described earlier. If there are multiple dropdown boxes, after completing the first dropdown box, you will immediately be prompted for the answers to the rest in the order in which they were created. The program will continue to prompt you for more lines of the table until you type, “end” as a response.

**Textbox**

Large text boxes are for long student responses. Each object of class “Textbox” has only one part, and this is the example of the right answer. This is not shown to the student. Because these relatively long passages of text would be impractical to grade automatically, the boxes need only to be completed to allow the student to move on to the next question. The student’s response is sent with the example response to the teacher for comparison at the end. Upon creating an instance of the class “Textbox”, you will be prompted for an example of the right answer. This will not be shown to the student; it will be written in the table of answers at the end so the grader can tell what the answer was supposed to say.

**Checkbox**

Each checkbox object has two parts: the list of possible answers and the list of correct answers. It is similar in this regard to the dropdown boxes, except that the dropdown boxes can only have one right answer. Upon creating an instance of the class “Checkbox,” you will be asked for a list of possible answers and then for a list of correct answers. If one of the given correct answers is not in the list of possible answers, the program will not accept it, and you will be asked to type in a new list of correct answers until each of the correct answers is on the list of possible answers.

###Functions

**generateHTMLWorksheet**

“generateHTMLWorksheet” is a function that takes the name of the worksheet as an argument. It takes all the information you gave about the questions in the worksheet and organizes it into an HTML file with the name given as the argument for the initialization function for the worksheet object. If the object has been converted into a JSON, the function will accept the function “loadWorksheet” as an argument.

**generateJSON**

“generateJSON” is a function that takes the name of the worksheet and the JSON file name as arguments. In this case, the file name does need to end with “.json”. It generates a JSON of the worksheet object named with the filename given.

**loadWorksheet**

“loadWorksheet” is a function that takes the name of the JSON file as an argument. It loads the worksheet object saved as the JSON file. If you assign a name to it, you can add questions and loose content to the worksheet and then save it again as a new JSON, but you cannot add sections to existing questions or add parts to existing sections because the names of questions and sections are not saved.
