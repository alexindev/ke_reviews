'use strict';

document.querySelector('.custom-file-input').addEventListener('change', function(e) {
  var fileName = e.target.files[0].name;
  var label = document.querySelector('.custom-file-label');
  label.innerText = fileName;
});