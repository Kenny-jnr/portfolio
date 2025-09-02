// First characteristics of making the keys letters show when I hover over the piano.

// Get the piano element
const piano = document.getElementById("piano"); // gets the piano element
const keys = piano.querySelectorAll(".key"); //gets all the keys element

// Show letter when mouse over
function showNotes() {
  keys.forEach((key) => {
    // loops through each key and displays the letter
    key.style.color = key.classList.contains("white") ? "black" : "white"; // shows color based on if the key is white or black
  });
  piano.style.cursor = "none"; // hides cursor
}

// Hide letter when mouse out
function hideNotes() {
  keys.forEach((key) => {
    key.style.color = "transparent"; // makes all the letters transparent when mouse is out
  });
}

// Add event listeners
piano.addEventListener("mouseover", showNotes);
piano.addEventListener("mouseout", hideNotes);

// Map key letters to their respective key divs
const keyMap = {
  A: ".key.white:nth-child(1)", // A key (white)
  W: ".key.black:nth-child(2)", // W key (black)
  S: ".key.white:nth-child(3)", // S key (white)
  E: ".key.black:nth-child(4)", // E key (black)
  D: ".key.white:nth-child(5)", // D key (white)
  F: ".key.white:nth-child(6)", // F key (white)
  T: ".key.black:nth-child(7)", // T key (black)
  G: ".key.white:nth-child(8)", // G key (white)
  Y: ".key.black:nth-child(9)", // Y key (black)
  H: ".key.white:nth-child(10)", // H key (white)
  U: ".key.black:nth-child(11)", // U key (black)
  J: ".key.white:nth-child(12)", // J key (white)
  K: ".key.white:nth-child(13)", // K key (white)
  O: ".key.black:nth-child(14)", // O key (black)
  L: ".key.white:nth-child(15)", // L key (white)
  P: ".key.black:nth-child(16)", // P key (black)
  ";": ".key.white:nth-child(17)", // ; key (white)
};

// mapping of the keycode to an external audio url
const sound = {
  A: "http://carolinegabriel.com/demo/js-keyboard/sounds/040.wav",
  W: "http://carolinegabriel.com/demo/js-keyboard/sounds/041.wav",
  S: "http://carolinegabriel.com/demo/js-keyboard/sounds/042.wav",
  E: "http://carolinegabriel.com/demo/js-keyboard/sounds/043.wav",
  D: "http://carolinegabriel.com/demo/js-keyboard/sounds/044.wav",
  F: "http://carolinegabriel.com/demo/js-keyboard/sounds/045.wav",
  T: "http://carolinegabriel.com/demo/js-keyboard/sounds/046.wav",
  G: "http://carolinegabriel.com/demo/js-keyboard/sounds/047.wav",
  Y: "http://carolinegabriel.com/demo/js-keyboard/sounds/048.wav",
  H: "http://carolinegabriel.com/demo/js-keyboard/sounds/049.wav",
  U: "http://carolinegabriel.com/demo/js-keyboard/sounds/050.wav",
  J: "http://carolinegabriel.com/demo/js-keyboard/sounds/051.wav",
  K: "http://carolinegabriel.com/demo/js-keyboard/sounds/052.wav",
  O: "http://carolinegabriel.com/demo/js-keyboard/sounds/053.wav",
  L: "http://carolinegabriel.com/demo/js-keyboard/sounds/054.wav",
  P: "http://carolinegabriel.com/demo/js-keyboard/sounds/055.wav",
  ";": "http://carolinegabriel.com/demo/js-keyboard/sounds/056.wav",
};

let keySequence = []; // storing our own sequence to compare

const target = ["W", "E", "S", "E", "E", "Y", "O", "U"]; // sequence to compare to

function scaryImage() {
  // function only hit when the squence matches
  const backgrounds = document.querySelectorAll(".background"); // gets the background of the piano div
  backgrounds.forEach((background) => {
    background.style.backgroundImage =
      "url('../static/piano/images/texture.jpeg')"; // changes the background to scary image
    background.style.backgroundSize = "cover";
    background.style.backgroundPosition = "center";
    const audio = new Audio(
      "../static/piano/audio/Creepy-piano-sound-effect.mp3"
    );
    audio.play(); // plays the spooky sound
    const h1 = document.querySelector(".background h1");
    h1.innerHTML = "I have Awoken."; // changes the message to this
  });

  piano.style.opacity = 0; // hides piano
  piano.style.cursor = "default";
  document.removeEventListener("keydown", keydownView); // removes listener
}

// change color when a key is clicked on
// also plays the audio depending on what key is clicked.
function keydownView(event) {
  const keyPressed = event.key.toUpperCase(); // Get the key pressed

  if (keyMap[keyPressed]) {
    const keyDiv = piano.querySelector(keyMap[keyPressed]); // finding the div
    if (keyDiv) {
      keyDiv.style.backgroundColor = "purple"; // Changes to purple

      const audio = new Audio(sound[keyPressed]);
      audio.play(); // plays the audio mapped to it

      // inclusion of timer to give an illusion of key being clicked on.
      setTimeout(() => {
        keyDiv.style.backgroundColor = ""; // back to normal
      }, 200); // after 200ms
    }
  }

  // checking for the sequence
  console.log(keyPressed); // used for debugging
  keySequence.push(keyPressed); // add the sequence as it is pressed
  if (keySequence.length > target.length) {
    keySequence.shift(); // handling situations where the clicked keys sequence is same length as the target but not the same.
  }

  if (keySequence.join("") === target.join("")) {
    scaryImage(); // Call a function when the sequence is matched
  }
}

// Add event listener for keydown event
document.addEventListener("keydown", keydownView);
