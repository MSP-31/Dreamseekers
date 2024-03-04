/*---모달 공통-----*/
var modal = document.getElementById("instrs-modal");
var modal_btn = document.getElementById("modal-open");
var modal_span = document.getElementsByClassName("modal-close")[0];
modal_btn.onclick = function() {
  modal.style.display = "block";
}
modal_span.onclick = function() {
  modal.style.display = "none";
}
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}