/*---모달 공통-----*/
var modal = document.getElementById("modal-box");
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

var editButtons = document.querySelectorAll('.modal-edit');
// 각 버튼에 이벤트 리스너를 추가
editButtons.forEach(function(button) {
  button.addEventListener('click', function() {
    // id값을 가져옴
    var id = this.dataset.id;
    // 해당 id값에 해당하는 요소를 찾아 가져옴
    var lectureElement = document.querySelector('a[href="list/' + id + '"]');
    var title = lectureElement.querySelector('.lecture-title').textContent;
    var contents = lectureElement.querySelector('.lecture-text').innerHTML;
    var contentText = contents.replace(/<br>/g, '\n');
    var image = lectureElement.querySelector('img').src;

    var form = document.querySelector('#modal-box form');
    form.action = "list/update/" + id;
    form.querySelector('input[name="title"]').value = title;
    form.querySelector('textarea[name="contents"]').value = contentText

    modal.style.display = "block";
  });
});