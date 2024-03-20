/*---모달 공통-----*/
var modal = document.getElementById("modal-box");
var modal_btn = document.getElementById("modal-open");
var modal_span = document.getElementsByClassName("modal-close")[0];
var form = document.querySelector('#modal-box form');
var imgElement = form.querySelector('.embed-img');
var containerImg = document.getElementsByClassName("container-img")[0];

modal_btn.onclick = function() {
  if (containerImg){
    containerImg.style.display = 'none';
  }
  modal.style.display = "block";
}
modal_span.onclick = function() {
  modal.style.display = "none";
  // 초기화
  form.removeAttribute('action');
  if(form.querySelector('input[name="title"]')){
    form.querySelector('input[name="title"]').value = '';
  }
  if(form.querySelector('input[name="name"]')){
    form.querySelector('input[name="name"]').value = '';
  }
  if(form.querySelector('textarea[name="contents"]')){
    form.querySelector('textarea[name="contents"]').value = '';
  }
  if(imgElement){
    imgElement.removeAttribute('alt');
    imgElement.removeAttribute('src');
  }
}

// 주요강의
var editButtons = document.querySelectorAll('.lecture-edit');
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
    var image = lectureElement.querySelector('img').dataset.src;

    form.action = "list/update/" + id;
    form.querySelector('input[name="title"]').value = title;
    form.querySelector('textarea[name="contents"]').value = contentText
    
    // 이미지 src 설정
    imgElement.src = image;
    imgElement.alt = title;

    var inputCheck = form.querySelector('.hidden-checkbox');
    inputCheck.value = id;

    containerImg.removeAttribute('style');

    modal.style.display = "block";
  });
});

// 강사소개
var editButtons = document.querySelectorAll('.instrs-edit');
// 각 버튼에 이벤트 리스너를 추가
editButtons.forEach(function(button) {
  button.addEventListener('click', function() {
    var id = this.dataset.id;
    console.log(id);
    // 부모 클래스를 가져옴
    var parent = this.parentNode;
    var name = parent.querySelector('.instrs-name').textContent;
    var contents = parent.querySelector('.instrs-content').innerHTML;
    var contentText = contents.replace(/<br>/g, '\n');
    var image = parent.querySelector('img').dataset.src;

    form.action = "update/" + id;
    form.querySelector('input[name="name"]').value = name;
    form.querySelector('textarea[name="contents"]').value = contentText
    
    // 이미지 src 설정
    imgElement.src = image;
    imgElement.alt = name;

    var inputCheck = form.querySelector('.hidden-checkbox');
    inputCheck.value = id;

    containerImg.removeAttribute('style');

    modal.style.display = "block";
  });
});