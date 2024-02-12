$(document).ready(function() {
  try{
    // 페이지 제목 가져옴
    var pageTitle = document.querySelector('#top-content h1').textContent;
  
    if (pageTitle){
      var menuItems = document.querySelectorAll('.menu');
      var menuTab = document.querySelector('#top-content .menu-tab');
  
      for (var i = 0; i<menuItems.length; i++){
        var menuItem = menuItems[i];
        var title = menuItem.querySelector('a').textContent;

        // 메뉴 이름이 일치하는 경우
        if (title === pageTitle){
          var submenus = menuItem.querySelectorAll('.submenu a');
      
          for(var j = 0; j < submenus.length; j++){
            var submenu = submenus[j];
            var url = submenu.href;
            
            var a = document.createElement('a');
            a.textContent = submenu.textContent;
            a.href = url;
            a.className = 'btn';

            // 임시
            console.log(j +"번째");
            console.log(window.location.href);
            console.log(url);

            // 현재 페이지와 같다면
            if(window.location.href == url){
              a.className = 'btn-active';
            }
            menuTab.appendChild(a);
          }
        }
      }
    }
  } catch(error){
    /* pass */
  }
  
  /* 서브 메뉴 */
  $('.menu-list').each(function(){
    var blind = $('#blind')
    var submenu = $(this).find('.submenu-container');
    var menu = $(this).find('.menu');

    menu.each(function(){
      $(this).hover(
        function(){
          blind.height('180px');
          submenu.height('180px');
          $(this).addClass('on');
        },
        function(){
          blind.height('0');
          submenu.height('0');
          $(this).removeClass('on');
        }
      );
    });
  });

  /* (햄버거)사이드 동작  */
  $('.burger-toggle').on('click', function() {
    var sidebar = document.getElementById('sidebar');
    var background = document.querySelector('#sidebar .background');
    var inner = document.querySelector('#sidebar .inner');

    if (sidebar.style.display === 'none'){
      sidebar.style.display = 'block'
      requestAnimationFrame(function(){
        background.style.opacity = '0.7';
      });
      setTimeout(function(){
        inner.classList.add('active');
      }, 10);
      // 스크롤 비활성화
      document.body.style.overflow = 'hidden';
    }
    else{
      background.style.opacity = '0'
      inner.classList.remove('active');
      setTimeout(function(){
        sidebar.style.display = 'none';
      }, 1000);
      // 스크롤 활성화
      document.body.style.overflow = 'auto';
    }
  });


});

/* header에 on클래스 추가 (스크롤시 변경) */
window.onscroll = function(){
  var header = document.querySelector('header');
  var scrollPosition = window.scrollY;
  
  if (scrollPosition > 50){
    header.classList.add('on');
  }
  else{
    header.classList.remove('on');
  }
}