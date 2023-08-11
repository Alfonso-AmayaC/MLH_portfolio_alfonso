let currentElement;
const aboutme = document.getElementById('aboutme');
const navbar = document.getElementById('navbar');
const work = document.getElementById('work');
const education = document.getElementById('education');
const hobbies = document.getElementById('hobbies');
const places = document.getElementById('places');
const timeline = document.getElementById('timeline');

const aboutmePosition = parseInt(aboutme.getBoundingClientRect().top);
const workPosition = parseInt(work.getBoundingClientRect().top);
const educationPosition = parseInt(education.getBoundingClientRect().top);
const hobbiesPosition = parseInt(hobbies.getBoundingClientRect().top);
const placesPosition = parseInt(places.getBoundingClientRect().top);
const timelinePosition = parseInt(timeline.getBoundingClientRect().top);

const classes = ['border-b-4', 'border-sky-300'];

const updateMenu = () => {
    const topPosition = parseInt(scrollY);

    if (topPosition >= 0 && ( topPosition > aboutmePosition && topPosition < workPosition))
        updateElement(navbar.children[0]);
    else if ( topPosition >= workPosition && topPosition < educationPosition)
        updateElement(navbar.children[1]);
    else if ( topPosition >= educationPosition && topPosition < hobbiesPosition)           
        updateElement(navbar.children[2]);
    else if ( topPosition >= hobbiesPosition && topPosition < placesPosition)
        updateElement(navbar.children[3]);
    else if ( topPosition >= placesPosition && topPosition < timelinePosition)
        updateElement(navbar.children[4]);
    else if ( (topPosition + 5) >= timelinePosition)
        updateElement(navbar.children[5]);
}

const updateElement = (element) => {

    if (currentElement == element) return;
    
    if (currentElement) {
        currentElement.classList.remove(...classes);
        currentElement = element;
    } else {
        currentElement = element;
    }

    currentElement.classList.add(...classes);
}

onscroll = () => {
    updateMenu();
}