// 이미지 끌림 방지
document.querySelectorAll('.slide_img').forEach(function(image) {
    image.addEventListener('dragstart', function(event){
        event.preventDefault();
    })
})

// 슬라이드 전체크기 구하기
const slide = document.querySelector(".slide");
let slideWidth = slide.clientWidth;

// 버튼 선택
const prevBtn = document.querySelector(".go-prev");
const nextBtn = document.querySelector(".go-next");

// 슬라이드 전체 선택해 값을 변경해주기 위해 슬라이드 전체 선택
let slideItems = document.querySelectorAll(".slide_item");
// 슬라이드 위치 한계
const maxSlide = slideItems.length;

// 슬라이드의 현재위치
let currSlide = 0;

// 페이지 네비 생성
const pagination = document.querySelector(".slide_pagination");
for (let i = 0; i < maxSlide; i++){
    pagination.innerHTML += `<li class="${i === 0 ? 'active' : ''}">•</li>`;
}

const paginationItems = document.querySelectorAll(".slide_pagination > li");

// 무한 슬라이드를 위해 처음과 마지막 슬라이드 복사
const startSlide = slideItems[0];
const endSlide = slideItems[slideItems.length - 1];

// 요소 생성
const startElem = startSlide.cloneNode(true);
const endElem = endSlide.cloneNode(true);

// 복제한 요소를 각 위치에 추가
slide.append(startElem); // 첫 번째 슬라이드를 마지막에 추가
slide.prepend(endElem); // 마지막 슬라이드를 처음에 추가

// 슬라이드 전체를 선택해 값 변경
slideItems = document.querySelectorAll(".slide_item");

// 초기 오프셋 설정
let offset = slideWidth * (currSlide + 1); // currSlide가 0이므로 +1
slideItems.forEach((i) => {
    i.style.left = `${-offset}px`;
});

function nextMove(){
    if(currSlide < maxSlide){
        currSlide++;
    } else {
        // 마지막 슬라이드에서 첫 슬라이드로 넘어가는 경우
        currSlide = 1;
        slideItems.forEach((i) => {
            // i.style.transition = 'none'; // 트랜지션 비활성화
            i.style.left = `-${slideWidth}px`; // 첫 번째 슬라이드 위치로 즉시 이동
        });
    }

    // 비동기 처리로 트랜지션 다시 적용
    setTimeout(() => {
        slideItems.forEach((i) => {
            i.style.transition = ''; // 트랜지션 다시 적용
            i.style.left = `${-(slideWidth * currSlide)}px`; // 새 위치로 이동
        });
    }, 20);
    // 페이지네비 업데이트
    paginationItems.forEach((i, index) => {
        i.classList.toggle("active", index === currSlide - 1);
    });
}

function prevMove(){
    if(currSlide > 1){
        currSlide--;
    } else {
        currSlide = maxSlide; // 마지막 실제 슬라이드로 이동
        slideItems.forEach((i) => {
            i.style.transition = 'none';
            i.style.left = `${-(slideWidth * (maxSlide + 1))}px`; // 마지막 실제 슬라이드 위치로 즉시 이동
        });
    }
    // 비동기 처리로 트랜지션 다시 적용
    setTimeout(() => {
        slideItems.forEach((i) => {
            i.style.transition = ''; // 트랜지션 다시 적용
            i.style.left = `${-(slideWidth * currSlide)}px`; // 새 위치로 이동
        });
    }, 10);

    // 페이지네비 업데이트
    paginationItems.forEach((i, index) => {
        i.classList.toggle("active", index === currSlide - 1);
    });
}

// 버튼에 클릭이벤트 추가
nextBtn.addEventListener("click",() => {
    nextMove();
});
prevBtn.addEventListener("click",() => {
    prevMove();
});

// 브라우저 화면 조정시 slideWidth 변경
window.addEventListener("resize", () => {
    slideWidth = slide.clientWidth;
});

// 각 페이지네비를 누르면 해당 슬라이드로 이동
for (let i = 0; i < maxSlide; i++){
    // 각 페이지네비 마다 클릭이벤트 추가
    paginationItems[i].addEventListener("click",() => {
        // 클릭한 페이지에따라 슬라이드 변경
        currSlide = i + 1;
        // 슬라이드를 이동시키기 위해 offset계산
        const offset = slideWidth * currSlide;
        // 각 슬라이드 아이템의 left에 offset 적용
        slideItems.forEach((i) => {
            i.style.left = `${-offset}px`;
        });
        // 슬라이드 이동시 현재 활성화된 페이지네비 변경
        paginationItems.forEach((i) => i.classList.remove("active"));
        paginationItems[currSlide - 1].classList.add("active");
    })
}

// 드래그 이벤트를 위한 변수 초기화
let startPoint = 0;
let endPoint = 0;

// 클릭 이벤트
slide.addEventListener("mousedown", (e) => {
    console.log("mousedown",e.pageX);
    startPoint = e.pageX; // 마우스 드래그 시작위치 저장
});
slide.addEventListener("mouseup",(e) => {
    console.log("mouseup", e.pageX);
    endPoint = e.pageX; // 마우스 드래그 끝 위치 저장
    if(startPoint < endPoint){
        // 마우스가 오른쪽으로 드래그 된 경우
        console.log("prev move");
        prevMove();
    } else if(startPoint > endPoint){
        // 마우스가 왼쪽으로 드래그 된 경우
        console.log("next move");
        nextMove();
    }
});

// 모바일 터치 이벤트
slide.addEventListener("touchstart",(e) => {
    startPoint = e.touches[0].pageX; // 터치 시작 위치 저장
});
slide.addEventListener("touchend",(e) => {
    endPoint = e.changedTouches[0].pageX; //터치가 끝나는 위치 저장
    if(startPoint < endPoint){
        // 오른쪽으로 드래그 된 경우
        console.log("prev move");
        prevMove();
    } else if(startPoint > endPoint){
        // 왼쪽으로 드래그 된 경우
        console.log("next move");
        nextMove();
    }
});

// 기본 슬라이드 루프 시작
let loopInterval = setInterval(() => {
    nextMove();
}, 3000);

// 슬라이드에 마우스가 올라간 경우 루프 멈춤
slide.addEventListener("mouseover", () => {
    clearInterval(loopInterval);
});

// 슬라이드에서 마우스를 땐 경우 루프 재시작
slide.addEventListener("mouseout", () => {
    loopInterval = setInterval(() => {
        nextMove();
    }, 3000);
});