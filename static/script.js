window.addEventListener("scroll", function() {
  var scrollPosition = window.scrollY || window.pageYOffset;
  var pageHeight = document.documentElement.scrollHeight - window.innerHeight;
  var scrollPercentage = (scrollPosition / pageHeight) * 100;
  var newWidth = scrollPercentage + "%";
  document.getElementById("myBar").style.width = newWidth;
});

setTimeout(function() {
  var blankPage = document.getElementById('blank-page');
  var actualSite = document.getElementById('actual-site');
  var htmlname=document.documentElement;
  var bodyname=document.body;
  blankPage.style.display = 'none';
  actualSite.style.display = 'block';
  htmlname.style.overflow='auto';
  bodyname.style.overflow='auto';
}, 1000);
var face=document.getElementById('face');
var followDiv = document.getElementById("small-cursor");
var followDiv1 = document.getElementById("big-cursor");
var isMouseMoving = false;
document.addEventListener("mousemove", function(event) {
  var x = event.clientX;
  var y = event.clientY;
  followDiv.style.transform = `translate3d(${x}px, ${y}px, 0)`;  // Offset to center the div on the cursor
  followDiv.style.visibility='visible';
  followDiv1.style.transform = `translate3d(${x-6}px, ${y-6}px, 0)`;  // Offset to center the div on the cursor
  followDiv1.style.visibility='visible';
});
function handleHover(x) {
  if(x==1){
  var cursor = document.getElementById("big-cursor");
  cursor.style.transform = 'scale(2)';
  }
  else if(x==0){
    var cursor = document.getElementById("big-cursor");
    cursor.style.transform = 'scale(0.5)';
    }
  }
class TextScramble {
  constructor(el) {
    this.el = el
    this.chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789.+_-=[];|\__<>:"'
    this.update = this.update.bind(this)
  }
  setText(newText, limit = Infinity) {
    const oldText = this.el.innerText
    const length = Math.max(oldText.length, newText.length)
    const promise = new Promise((resolve) => (this.resolve = resolve))
    this.queue = []
    for (let i = 0; i < length; i++) {
      const from = oldText[i] || ''
      const to = newText[i] || ''
      const start = Math.floor(Math.random() * 40)
      const end = start + Math.floor(Math.random() * 40)
      const char = i < limit ? this.randomChar() : '' // Added limit check
      this.queue.push({ from, to, start, end, char })
    }
    cancelAnimationFrame(this.frameRequest)
    this.frame = 0
    this.update()
    return promise
  }  
  update() {
    let output = ''
    let complete = 0
    for (let i = 0, n = this.queue.length; i < n; i++) {
      let { from, to, start, end, char } = this.queue[i]
      if (this.frame >= end) {
        complete++
        output += to
      } else if (this.frame >= start) {
        if (!char || Math.random() < 0.08) {
          char = this.randomChar()
          this.queue[i].char = char
        }
        output += `<span class="dud">${char}</span>`
      } else {
        output += from
      }
    }
    this.el.innerHTML = output
    if (complete === this.queue.length) {
      this.resolve()
    } else {
      this.frameRequest = requestAnimationFrame(this.update)
      this.frame++
    }
  }
  randomChar() {
    return this.chars[Math.floor(Math.random() * this.chars.length)]
  }
}
const phrases = [
  'Python',
  'C++',
  'SQL',
  'Javascript',
  'HTML',
  'CSS',
  'Java',
  'Matlab'
]

const el = document.querySelector('.face-glitch')
const fx = new TextScramble(el)

let counter = 0
const next = () => {
  fx.setText(phrases[counter], 5).then(() => {
    setTimeout(next, 2500)
  })
  counter = (counter + 1) % phrases.length
}


next()
const canvas = document.getElementById('graph');
const ctx = canvas.getContext('2d');

const graphWidth = canvas.width;
const graphHeight = canvas.height;
const scale = 40;
let amplitude = 0; // Updated dynamically based on vertical cursor movement
let frequency = 0; // Updated dynamically based on horizontal cursor movement
let phase = 0;

const circleRadius = 30;
let circleCenterX = circleRadius + 10; // Initial X position of the circle center
let circleCenterY = graphHeight / 2; // Y position of the circle center
let rotationAngle = 0;

function clearCanvas() {
    ctx.clearRect(0, 0, graphWidth, graphHeight);
}

function drawSineGraph() {
    clearCanvas();
  
    ctx.beginPath();
    ctx.strokeStyle = 'white';
    ctx.lineWidth = 2;
    for (let x = 0; x < graphWidth; x++) {
        const radians = (x / scale) * frequency + phase;
        const y = (Math.sin(radians) * amplitude) + graphHeight / 2;
        if (x === 0) {
            ctx.moveTo(x, y);
        } else {
            ctx.lineTo(x, y);
        }
    }
    ctx.stroke();

    phase += 0.03;
}

function updateAmplitude(e) {
    const maxAmplitude = graphHeight / 2;
    const cursorY = e.clientY - canvas.offsetTop;
    amplitude = (maxAmplitude / (graphHeight / 2)) * (cursorY / 9);
}

function updateFrequency(e) {
    const maxFrequency = 11;
    const cursorX = e.clientX - canvas.offsetLeft;
    frequency = (maxFrequency / (graphWidth / 2)) * (cursorX / 10);
}
face=document.getElementById('face');
if (window.innerWidth <= 600) {
  // Mobile screen
  amplitude = 15; // Set a fixed amplitude for mobile screens
  frequency = 2; // Set a fixed frequency for mobile screens
} 
else{
face.addEventListener('mousemove', function(e) {
    updateAmplitude(e);
    updateFrequency(e);
});
}
function animate() {
    drawSineGraph();

    requestAnimationFrame(animate);
}

animate();
const jobTitles = document.getElementsByClassName('job-heading');
const jobImages = document.getElementsByClassName('job-image');
const jobDeets = document.getElementsByClassName('job-deets');
const imageLink = document.getElementsByClassName('link-image');
const imageLink1 = document.getElementsByClassName('link-image-1');
const imageLink2 = document.getElementsByClassName('link-image-2');
const imageLink3 = document.getElementsByClassName('link-image-3');

const elementState = [];

function toggleDisplayPC(i) {
  if (elementState[i]) {
    jobTitles[i].style.backgroundPosition = '';
    jobTitles[i].style.color = '';
    jobDeets[i].style.display = 'none';

    for (let j = 0; j < imageLink.length; j++) {
      imageLink[j].style.display = 'none';
    }
  } else {
    jobTitles[i].style.backgroundPosition = 'left';
    jobTitles[i].style.color = 'black';
    jobDeets[i].style.display = 'block';

    if (i === 0) {
      for (let j = 0; j < imageLink1.length; j++) {
        imageLink1[j].style.display = 'block';
      }
    } else if (i === 1) {
      for (let j = 0; j < imageLink2.length; j++) {
        imageLink2[j].style.display = 'block';
      }
    } else if (i === 2) {
      for (let j = 0; j < imageLink3.length; j++) {
        imageLink3[j].style.display = 'block';
      }
    }
  }

  // Invert the state
  elementState[i] = !elementState[i];
}

function toggleDisplayMobile(i) {
  if (elementState[i]) {
    jobTitles[i].style.backgroundPosition = '';
    jobTitles[i].style.color = '';
    jobDeets[i].style.display = 'none';
    jobImages[i].style.width = "250px";
    jobImages[i].style.height = "125px";
    jobImages[i].style.backgroundColor = "none";
    jobImages[i].style.boxShadow = "10px 10px rgba(255, 255, 255, 0.148);";
    if(i==0){
      jobImages[i].style.backgroundImage = "url('static/ticketbooking\ app.png')";
    }
    else if(i==1){
      jobImages[i].style.backgroundImage = "url('static/sentiment-analysis.png')";
    }
    else if(i==2){
      jobImages[i].style.backgroundImage = "url('static/portfolio.png')";
    }
    for (let j = 0; j < imageLink.length; j++) {
      imageLink[j].style.display = 'none';
    }
  } else {
    jobTitles[i].style.backgroundPosition = 'left';
    jobTitles[i].style.color = 'black';
    jobDeets[i].style.display = 'block';
    jobImages[i].style.width = "270px";
    jobImages[i].style.height = "130px";
    jobImages[i].style.backgroundImage = "none";
    jobImages[i].style.backgroundColor = "white";
    jobImages[i].style.boxShadow = "10px 10px rgba(255, 255, 255, 0.604)";
    if (i === 0) {
      for (let j = 0; j < imageLink1.length; j++) {
        imageLink1[j].style.display = 'block';
      }
    } else if (i === 1) {
      for (let j = 0; j < imageLink2.length; j++) {
        imageLink2[j].style.display = 'block';
      }
    } else if (i === 2) {
      for (let j = 0; j < imageLink3.length; j++) {
        imageLink3[j].style.display = 'block';
      }
    }
  }

  // Invert the state
  elementState[i] = !elementState[i];
}
// Initialize the element state to false (not toggled)
for (let i = 0; i < jobImages.length; i++) {
  elementState[i] = false;
}

// Mouse events
for (let i = 0; i < jobImages.length; i++) {
  jobImages[i].addEventListener('mouseover', function () {
    toggleDisplayPC(i);
  });

  jobImages[i].addEventListener('mouseout', function () {
    toggleDisplayPC(i);
  });
}

// Touch events for mobile devices
for (let i = 0; i < jobImages.length; i++) {
  jobImages[i].addEventListener('touchstart', function (event) {
    // Prevents triggering both touch and mouse events simultaneously
    event.preventDefault();
    toggleDisplayMobile(i);
  });
}

const menuButton = document.getElementById('menuButton');
const menuOverlay = document.getElementById('menuOverlay');
const menuContent = document.getElementById('menuContent');
const smallLine = document.getElementsByClassName('small-line');
let isMenuOpen = false;

menuButton.addEventListener('click', () => {
  if (isMenuOpen) {
    menuContent.style.transform = 'translateX(100%)';
    for (let i=0; i<smallLine.length; i++){
      if(i==0){
      smallLine[i].style.transform = 'rotate(0deg) translateY(0px) ';
      }
      if(i==1){
        smallLine[i].style.display='';
      }
      if(i==2){
        smallLine[i].style.transform = 'rotate(0deg) translateY(0px)';
        }
    }
    setTimeout(() => {
      menuOverlay.style.display = 'none';
    }, 300);
  } else {
    menuOverlay.style.display = 'block';
    setTimeout(() => {
      menuContent.style.transform = 'translateX(0)';
      for (let i=0; i<smallLine.length; i++){
        if(i==0){
        smallLine[i].style.transform = 'rotate(45deg) translateY(8px) ';
        }
        if(i==1){
          smallLine[i].style.display='none';
        }
        if(i==2){
          smallLine[i].style.transform = 'rotate(-45deg) translateY(-8px)';
          }
      }
    }, 10);
  }

  isMenuOpen = !isMenuOpen;
});

menuOverlay.addEventListener('click', () => {
  menuContent.style.transform = 'translateX(100%)';
  setTimeout(() => {
    menuOverlay.style.display = 'none';
  }, 300);

  isMenuOpen = false;
});

console.log("I'm Running.")