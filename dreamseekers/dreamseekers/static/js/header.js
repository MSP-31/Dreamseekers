$(document).ready(function() {
  /* 햄버거 버튼 동작  */
  $('.burger-toggle').on('click', function() {
    var sidebar = document.getElementById("sidebar");
    var background = document.querySelector('#sidebar .background');
    var inner = document.querySelector('#sidebar .inner');

    if (sidebar.style.display === "none"){
      sidebar.style.display = "block"
      requestAnimationFrame(function(){
        background.style.opacity = "0.7";
      });
      setTimeout(function(){
        inner.classList.add('active');
      }, 10);
      // 스크롤 비활성화
      document.body.style.overflow = "hidden";
    }
    else{
      background.style.opacity = "0"
      inner.classList.remove('active');
      setTimeout(function(){
        sidebar.style.display = "none";
      }, 1000);
      // 스크롤 활성화
      document.body.style.overflow = "auto";
    }
  });
});

/* header에 on클래스 추가 (스크롤시 색 변경) */
window.onscroll = function(){
  var header = document.querySelector('header');
  var scrollPosition = window.scrollY;
  
  if (scrollPosition > 50){
    header.classList.add('on');
  } else{
    header.classList.remove('on');
  }
}