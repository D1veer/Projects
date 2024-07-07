// make a random number between 1 and 100
var randomNumber = Math.floor(Math.random() * 100) + 1;
// make a guess
var guess = prompt("Guess a number between 1 and 100");
// check if the guess is correct
if (guess == randomNumber) {
  alert("You guessed the number!");
}
else if (guess < randomNumber) {
  alert("Too low!");
}
else {
  alert("Too high!");
}
// end of program
