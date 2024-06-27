document.addEventListener('DOMContentLoaded', function() {
  // 체크박스와 버튼 요소를 변수에 할당
  var checkbox = document.getElementById('consent-check');
  var submitButton = document.querySelector('input[type="submit"]');

  // 초기 상태에서 버튼을 비활성화
  submitButton.disabled = true;

  // 체크박스의 상태가 변경될 때마다 호출될 함수
  checkbox.addEventListener('change', function() {
    // 체크박스가 선택되면 버튼을 활성화, 그렇지 않으면 비활성화
    submitButton.disabled = !this.checked;
  });

  // 모달부분 //
  var modal = document.getElementById("modal-box");
  var modal_btn = document.getElementsByClassName("content")[0];
  var modal_span = document.getElementsByClassName("modal-close")[0];

  modal_btn.onclick = function() {
    modal.style.display = "block";
  }

  modal_span.onclick = function() {
    modal.style.display = "none";
  }

});