// This script should collapse the nav bar after a link has been clicked.
window.addEventListener("load", function() {
  var navbar_elements = document.querySelectorAll('nav-item');
  // Loop backwards because object property is removed each iteration
  for (var i = navbar_elements.length - 1; i >= 0; --i){
    navbar_elements[i].addEventListener('click', function(){
      console.log("Event triggered");
      navbar_elements[i].setAttribute('class', 'navbar-collapse');
    });
  }
});
