const timer = document.querySelector('.countdown');
const minutes = document.querySelector('.minutes');
const seconds = document.querySelector('.seconds');
const message = document.querySelector('.message');

const plus = document.querySelector('.plus');
const minus = document.querySelector('.minus');
const start_stop = document.querySelector('.start-stop');


let countSec = 0;
let countMin = 0;
let timer_is_stop = 1;

const updateText = () =>{
    minutes.innerHTML = (0 + String(countMin)).slice(-2);
    seconds.innerHTML = (0 + String(countSec)).slice(-2);
}
updateText();

const countDown = () => {
    let total = countSec + countMin * 60;
    const timeinterval = setTimeout(countDown, 1000);
    if (timer_is_stop == 1) {
        clearTimeout(timeinterval)
    } else {
        if (total <= 0) {
            clearInterval(timeinterval);
            timer.style.display = 'none';
            message.innerHTML = '<p>I am done...</p>'
            start_stop.style.backgroundColor = 'yellow'
            start_stop.innerHTML = 'reset'
        }
        if(countSec > 0) {
            countSec--;
        } else {
            countSec = 59;
            countMin--;
        }
        updateText();
    }
}

plus.onclick = () =>{
    if (document.querySelector('input[name="rad_units"]:checked').value == "minutes") {
        if(countMin < 59) {
            ++countMin;
        }
    } else {
        if(countSec < 59) {
            ++countSec;
        } else {
            countSec = 0;
            if (countMin < 59) {
                ++countMin;
            }
        }
    }
    updateText()
}

minus.onclick = () =>{
    if (document.querySelector('input[name="rad_units"]:checked').value == "minutes") {
        if(countMin > 0) {
            --countMin;
        }
    } else {
        if(countMin <= 0 && countSec===0){
            countSec = 0;
            countMin = 0;
            return;
        }
        if(countSec > 0) {
            --countSec;
        } else {
            countSec = 59;
            --countMin;
        }
    }
    updateText();
}

start_stop.onclick = () => {
  if (start_stop.innerHTML == 'reset') {
    window.location.reload()
  }
    if (timer_is_stop == 1) {
        timer_is_stop = 0
        start_stop.innerHTML = 'pause'
        start_stop.style.backgroundColor = 'orange'
    } else {
        timer_is_stop = 1
        start_stop.innerHTML = 'continue'
        start_stop.style.backgroundColor = 'green'
    }
    countDown();
}

