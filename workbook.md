Dragoon HTML Workbooks
=======================

##JavaScript

###Head

At the head of the workbook, there is a section in JavaScript that contains, in this order:
* The definition of the function "openDragoonProblem", which is called whenever an "Open Dragoon" button is pressed in the body of the workbook: The only argument that this function takes is the Dragoon problem's number. This number determines the problem that is opened and its mode. It takes the username from the text box at the top of the workbook and opens the problem under that username. If a section is mentioned in the workbook's URL, it uses that section. If there is no section mentioned in the URL, it sets the section to "public-workbook".
* The definition of the function "openDragoonProblem", which is called whenever an "Open Dragoon" button is pressed in the body of the workbook
* The definition of the function "checkAnswers", which turns the background of a given dropdown box green and returns true if the answer is correct and turns it red and returns false if the answer is incorrect
* The definition of the function "checkTextbox", which turns the background of a given large text box green and returns true if there is any content at all in the box and turns it red and returns false if there is no content
* The definition of the function "checkbox", which turns the background of a given set of checkboxes green and returns true if the answer is correct and turns it red and returns false if the answerr is incorrect
* The definition of the function "checkboxCorrection", which changes the answer submitted for a given checkbox to the correct answer
* The definition of the function "retrieveCheckboxValue", which returns the answer that the student has given for a given checkbox
* The function "time1", which starts the timer for the first question
* The definition of the function "checkCompletion", which returns true if a given Dragoon problem is complete


###Username

After the script at the beginning, there is a text box where the user can enter a username and a button labeled, "Start Workbook". Beneath that, there is a section in JavaScript that contains an if statement and a function. The if statement takes the username and section from the URL if they are in the URL. It then disables the username field, hides the button, and shows the first question of the workbook.

The function is called when the user clicks on the "Start Workbook" button. If there is nothing written in the username box, or if the username is longer than thirty characters, when the button is pressed, it sends an alert to remind the user to enter a username between one and thirty characters long and turns the box red. If the username is valid, it disables the username field, hides the button, shows the first question of the workbook, and returns the box's color to white if it had been red.

###Questions

Each Dragoon HTML workbook is divided into questions. A student cannot move on to a new question unless every part of the current question is completed properly. After the text of each question, there is a JavaScript program, which contains, in this order:
* A set of variables, one for each problem, that are used to count how many times the student answers it incorrectly
* A function that is called when the "Continue" button is pressed
  * A reassignment of the variable `yestim[n]` to zero, which stops the timer that was started with the opening of the workbook or at the end of the last question
  * The assignment of the variable in the end table that records the time to the value of the timer
  * Functions that turn the correct answers green and the incorrect answers red
  * An if statement that sends an alert to the student if one of the answers is not completed
  * An if statement for each dropdown box, large textbox, and checkbox that adds one to the aforementioned counting variable if it is answered incorrectly
  * An if statement that gets rid of the button, shows the next question, freezes the elements, and starts the timer for the next question if every element is completed correctly or the student has run out of tries
  * An if statement that writes all of the student's answers in the results table and changes an element's answer to the correct answer and turns it yellow if it was answered incorrectly three times
