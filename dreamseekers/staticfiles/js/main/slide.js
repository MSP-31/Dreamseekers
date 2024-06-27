// 이미지 끌림 방지
document.querySelectorAll('.slide-img').forEach(function(image) {
    image.addEventListener('dragstart', function(event){
        event.preventDefault();
    })
})

$(document).ready(function() {
    
    /** 모든 슬라이드 요소 */
    var items = $('.slide-item')
    /** 슬라이드 총 개수 */
    var itemAmt = items.length;
    /** 현재 슬라이드를 나타냄 */
    var currentIndex = 0;
    var autoSlide;

    // 첫 번째 슬라이드만 보이도록 설정
    items.hide();
    items.eq(currentIndex).show();

    startSlideShow();

    // 네비게이션 생성
    for(var i = 0; i < itemAmt; i++){
       var navBtn = $('<li></li>');
       navBtn.on('click',(function(index){
            return function(){
                // 현재 페이지와 클릭한 페이지가 같을때
                if(currentIndex === index){
                    // 수행시간만 초기화
                    clearInterval(autoSlide);
                    startSlideShow();
                } else{ // 기존 동작 수행
                    clearInterval(autoSlide);
                    currentIndex = index;
                    cycleItem();
                    startSlideShow();
                }
            };
       })(i));
       $('.slide-pagination').append(navBtn);
    }

    // 첫번째 네비게이션 활성화
    $('.slide-pagination li').first().addClass('active');
    
    /** 선택된 슬라이드를 보여줌 */
    function cycleItem(){
        var item = $('.slide-item').eq(currentIndex); // 해당 슬라이드 선택
        items.fadeOut(); // 모든 슬라이드를 페이드아웃
        item.fadeIn(); // 현재 슬라이드를 페이드인
        
        // 현재 슬라이드의 네비게이션을 활성화
        $('.slide-pagination li').removeClass('active');
        $('.slide-pagination li').eq(currentIndex).addClass('active');
    }

    /** 자동으로 슬라이드를 넘김 */
    function startSlideShow() {
        autoSlide = setInterval(function(){
            currentIndex += 1;
            if(currentIndex > itemAmt - 1){
                currentIndex = 0;
            }
            cycleItem();
        }, 6000);
    }

    $('.slide-next').click(function(){
        // 반복 타이머 취소
        clearInterval(autoSlide);
        currentIndex += 1;
        if(currentIndex > itemAmt - 1){
            currentIndex = 0;
        }
        cycleItem();
        startSlideShow();
    });
    $('.slide-prev').click(function(){
        clearInterval(autoSlide);
        currentIndex -= 1;
        if(currentIndex < 0){
            currentIndex = itemAmt - 1;
        }
        cycleItem();
        startSlideShow();
    });

    
});