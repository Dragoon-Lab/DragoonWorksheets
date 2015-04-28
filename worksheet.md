Dragoon HTML Worksheets
=======================

###Questions (not yet presentable)

Each Dragoon HTML worksheet is divided into questions. A student cannot move on to a new question unless every part of the current question is completed properly. Every question is followed by a JavaScript program, which contains, in this order:
* A set of variables, one for each problem, that are used to count how many times the student answers that particular question incorrectly
* A function that is called when the "Continue" button is pressed
  *A reassignment of the variable `yestim[n]` to zero, which stops the timer that was started with the opening of the worksheet or at the end of the last question
  *The assignment of the variable in the end table that records the time to the value of the timer
  *The calling of functions that turn correctly-answered elements green and incorrectly-answered questions red
  *An if statement that sends an alert to the student if one of the answers is not completed
  *An if statement for each dropdown box, large textbox, and checkbox that adds one to the aforementioned counting variable if it is answered incorrectly
  *An if statement that gets rid of the button, shows the next question, freezes the elements, and starts the timer for the next question if every element is completed correctly or the student has run out of tries
  *An if statement that writes all of the student's answers in the results table and changes an element's answer to the correct answer and turns it yellow if it was answered incorrectly three times
  