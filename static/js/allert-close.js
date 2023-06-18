'use strict';

document.addEventListener("DOMContentLoaded", function() {
  var closeButton = document.querySelector(".alert .close");
  closeButton.addEventListener("click", function() {
    var alertElement = this.parentNode;
    alertElement.parentNode.removeChild(alertElement);
  });
});