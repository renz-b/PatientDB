const fadeElems = document.querySelectorAll('.has-fade');
const header = document.querySelector(".header");
const overlay = document.querySelector(".overlay");
const body = document.querySelector("body");

btnHamburger.addEventListener("click", function(){

    if(header.classList.contains("open")){
        body.classList.remove("noscroll");
        header.classList.remove("open");
        fadeElems.forEach(function(element){
            element.classList.remove("fade-in");
            element.classList.add("fade-out");            
        });

    } else {
        body.classList.add("noscroll");
        header.classList.add("open");
        fadeElems.forEach(function(element){
            element.classList.remove("fade-out");
            element.classList.add("fade-in");
        });

    }
})

function textAreaAdjust(element) {
    element.style.height = "auto";
    element.style.height = (10+element.scrollHeight)+"px";
}