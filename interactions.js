// Script to open and close sidebar
function w3_open() {
    document.getElementById("mySidebar").style.display = "block";
    document.getElementById("myOverlay").style.display = "block";
}

function w3_close() {
    document.getElementById("mySidebar").style.display = "none";
    document.getElementById("myOverlay").style.display = "none";
}



// Script to show photo grids
function hideAllPhotoGrid(){
    document.getElementById("firstPage").style.display = "none";
    document.getElementById("secondPage").style.display = "none";
}

function showPhotoGrid(pg){
    hideAllPhotoGrid();
    if (pg == 1){
        document.getElementById("firstPage").style.display = "block";
    }
    else if (pg == 2){
        document.getElementById("secondPage").style.display = "block";
    }
}

let goToFirstPage = document.querySelectorAll(".goToFirstPage");
for (let i = 0; i < goToFirstPage.length; i++){
    goToFirstPage[i].addEventListener("click", function(){
        let pg = 1;
        showPhotoGrid(pg);
    })
}

let goToSecondPage = document.querySelectorAll(".goToSecondPage");
for (let i = 0; i < goToSecondPage.length; i++){
    goToSecondPage[i].addEventListener("click", function(){
        let pg = 2;
        showPhotoGrid(pg);
    })
}


// Slideshow (精彩回顧)
var slideIndex = 1;
showDivs(slideIndex);

function plusDivs(n) {
  showDivs(slideIndex += n);
}

function currentDiv(n) {
  showDivs(slideIndex = n);
}

function showDivs(n) {
  var i;
  var x = document.getElementsByClassName("mySlides");
  var dots = document.getElementsByClassName("demodots");
  if (n > x.length) {slideIndex = 1}
  if (n < 1) {slideIndex = x.length} ;
  for (i = 0; i < x.length; i++) {
    x[i].style.display = "none";
  }
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" w3-white", "");
  }
  x[slideIndex-1].style.display = "block";
  dots[slideIndex-1].className += " w3-white";
}

