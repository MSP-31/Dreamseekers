//출처: https://songsong.dev/entry/Javascript로-달력-만들기 [송송은 오늘도 열심히 코딩 하네:티스토리]
$(document).ready(function() {
    calendarInit();
});

// 관리자인지 판별
var adminIndicator = document.querySelector('#admin-indicator');
var isAdmin = adminIndicator ? adminIndicator.dataset.isAdmin === 'true' : false;

function calendarInit() {
    // 날짜 정보 가져오기
    var date = new Date(); // 현재 날짜(로컬 기준) 가져오기
    var utc = date.getTime() + (date.getTimezoneOffset() * 60 * 1000); // utc 표준시 도출
    var kstGap = 9 * 60 * 60 * 1000; // 한국 kst 기준시간 더하기
    var today = new Date(utc + kstGap); // 한국 시간으로 date 객체 만들기(오늘)

    // 달력에서 표기하는 날짜 객체
    var thisMonth = new Date(today.getFullYear(), today.getMonth(), today.getDate());

    var currentYear = thisMonth.getFullYear(); // 달력에서 표기하는 연
    var currentMonth = thisMonth.getMonth(); // 달력에서 표기하는 월
    var currentDate = thisMonth.getDate(); // 달력에서 표기하는 일
    
    var selectedDate; // 클릭한 날짜 저장
    // 관리자인지 판별
    var adminIndicator = document.querySelector('#admin-indicator');
    var isAdmin = adminIndicator ? adminIndicator.dataset.isAdmin === 'true' : false;


    // 캘린더 렌더링
    renderCalender(thisMonth);

    function renderCalender(thisMonth) {
        // 렌더링을 위한 데이터 정리
        currentYear = thisMonth.getFullYear();
        currentMonth = thisMonth.getMonth();
        currentDate = thisMonth.getDate();

        // 이전 달의 마지막 날 날짜와 요일 구하기
        var startDay = new Date(currentYear, currentMonth, 0);
        var prevDate = startDay.getDate();
        var prevDay = startDay.getDay();

        // 이번 달의 마지막날 날짜와 요일 구하기
        var endDay = new Date(currentYear, currentMonth + 1, 0);
        var nextDate = endDay.getDate();
        var nextDay = endDay.getDay();

        // 현재 월 표기
        $('.year-month').text(currentYear + '.' + (currentMonth + 1));

        // 렌더링 html 요소 생성
        calendar = document.querySelector('.dates')
        calendar.innerHTML = '';

        // 지난달
        for (var i = prevDate - prevDay + 1; i <= prevDate; i++) {
            var newDiv = document.createElement('div');
            newDiv.className = 'day prev disable';

            var span = document.createElement('span');
            span.textContent = i;
            newDiv.appendChild(span);

            // 셀의 날짜를 'data-date' 속성에 설정합니다.
            var cellDate = new Date(currentYear, currentMonth-1, i+1);
            newDiv.dataset.date = cellDate.toISOString().split('T')[0];

            // 클릭 이벤트 리스너 추가
            newDiv.addEventListener('click', function() {
                // 클릭한 날짜 저장
                var fullDate = new Date(this.dataset.date);

                // 이전 달로 넘어감
                thisMonth = new Date(currentYear, currentMonth - 1, 1);
                renderCalender(thisMonth);
                
                // 모달창 띄우기
                showModal(fullDate);
            });

            calendar.appendChild(newDiv);
        }
        
        // 이번달
        for (var i = 1; i <= nextDate; i++) {
            var newDiv = document.createElement('div');
            newDiv.className = 'day current';
            
            var span = document.createElement('span');
            span.textContent = i;
            newDiv.appendChild(span);
            
            if (i == selectedDate){
                newDiv.classList.add('selected');
            }

            // 셀의 날짜를 'data-date' 속성에 설정합니다.
            var cellDate = new Date(currentYear, currentMonth, i+1);
            newDiv.dataset.date = cellDate.toISOString().split('T')[0];

            // 클릭 이벤트 리스너 추가
            newDiv.addEventListener('click', function() {
                // 이전에 선택된 요소가 있는 경우, 'selected' 클래스 제거
                var selected = document.querySelector('.selected');
                if (selected) {
                    selected.classList.remove('selected');
                }
                // 클릭한 요소에 'selected' 클래스 추가
                this.classList.add('selected');
                
                // 클릭한 날짜 저장
                var fullDate = new Date(this.dataset.date);

                // 모달창 띄우기
                showModal(fullDate);
            });

            calendar.appendChild(newDiv);
        }
        
        // 다음달
        for (var i = 1; i <= (7 - nextDay == 7 ? 0 : 7 - nextDay); i++) {
            var newDiv = document.createElement('div');
            newDiv.className = 'day next disable';

            var span = document.createElement('span');
            span.textContent = i;
            newDiv.appendChild(span);

            // 셀의 날짜를 'data-date' 속성에 설정합니다.
            var cellDate = new Date(currentYear, currentMonth+1, i+1);
            newDiv.dataset.date = cellDate.toISOString().split('T')[0];

            // 클릭 이벤트 리스너 추가
            newDiv.addEventListener('click', function() {
                // 클릭한 날짜 저장
                var fullDate = new Date(this.dataset.date);
                
                thisMonth = new Date(currentYear, currentMonth + 1, 1);
                renderCalender(thisMonth);

                // 모달창 띄우기
                showModal(fullDate);
            });

            calendar.appendChild(newDiv);
        }

        // 오늘 날짜 표기
        if (today.getMonth() == currentMonth) {
            todayDate = today.getDate();
            var currentMonthDate = document.querySelectorAll('.dates .current');
            currentMonthDate[todayDate -1].classList.add('today');
        }

        // 일정 추가
        addSchedules();
    }
    // 이전달로 이동
    $('.go-prev').on('click', function() {
        thisMonth = new Date(currentYear, currentMonth - 1, 1);
        selectedDate = null;
        renderCalender(thisMonth);
    });

    // 다음달로 이동
    $('.go-next').on('click', function() {
        thisMonth = new Date(currentYear, currentMonth + 1, 1);
        selectedDate = null;
        renderCalender(thisMonth); 
    });

    
}
// 상세 모달
function showModal(fullDate){
    var modal = document.getElementById('calender-modal');
    var closeBtn = document.getElementsByClassName('modal-close')[0];
    var date = document.getElementsByClassName('selected-date')[0];
    var day = document.getElementsByClassName('selected-day')[0];
    var modalRevise = document.getElementsByClassName('modal-revise')[0];
    var detailListArea = document.getElementsByClassName('detail-list-area')[0];

    var dateString = fullDate.toISOString().split('T')[0];  // 'YYYY-MM-DD' 형식
    dateString = dateString.replace(/-/g, '.'); // '-'를 '.'으로 바꾸기
    date.textContent = dateString; // 선택한 날짜 표시

    // 요일 표시
    var daysInKorean = ['일', '월', '화', '수', '목', '금', '토'];
    var dayInKorean = daysInKorean[fullDate.getDay()];
    day.textContent = dayInKorean+"요일";

    // 모든 'detail-list' li 요소를 제거합니다.
    var lis = document.querySelectorAll('.detail-list');
    for (var i = 0; i < lis.length; i++) {
        lis[i].remove();
    }

    // 일정 내용 추가 부분
    for (var i = 0; i < schedules.length; i++) {
        var schedule = schedules[i]; // 일정의 날짜를 가져옵니다.
        var schedulePK = schedule.pk;
        var contentTextValue = schedule.fields.contents;
        var allDay = schedule.fields.allDay; // 종일 여부
            if (allDay == true){
                var timeText = '종일 일정';
            }
            else{
                var timeText = dateSchedules(schedule)
            }

        var date = new Date(schedule.fields.date); // 달력의 각 셀을 순회합니다.
        if(JSON.stringify(date) === JSON.stringify(fullDate)){
            // 'detail-list' li 요소 생성
            var li = document.createElement('li');
            li.className = 'detail-list';
            li.dataset.pk = schedulePK; // 'data-pk' 속성 추가

            // 기존의 'content-time'과 'content-text' 요소를 제거합니다.
            var oldContentTime = li.querySelector('.content-time');
            var oldContentText = li.querySelector('.content-text');
            if (oldContentTime) oldContentTime.remove();
            if (oldContentText) oldContentText.remove();
            

            // 'content-time' span 요소 생성
            var contentTime = document.createElement('span');
            contentTime.className = 'content-time';
            contentTime.textContent = timeText;
            li.appendChild(contentTime);

            // 'content-text' span 요소 생성
            var contentText = document.createElement('span');
            contentText.className = 'content-text';
            contentText.textContent = contentTextValue
            li.appendChild(contentText);

            // 사용자가 staff인지 확인
            if (isAdmin) {
                // 기존의 'modal-revise' 요소를 제거합니다.
                var oldModalRevise = li.querySelector('.modal-revise');
                if (oldModalRevise) oldModalRevise.remove();

                // 'modal-revise' span 요소 생성
                var modalRevise = document.createElement('span');
                modalRevise.className = 'modal-revise';

                // 'reviseForm' span 요소 생성
                var reviseForm = document.createElement('span');
                reviseForm.id = 'reviseForm';
                reviseForm.className = 'btn';
                reviseForm.textContent = '수정';
                modalRevise.appendChild(reviseForm);

                // form 요소 생성
                var form = document.createElement('form');
                form.id = 'deleteForm';
                form.method = 'POST';
                form.action = 'calender/del/'+schedulePK+'/';
                form.onsubmit = function() {
                    return confirm('정말로 삭제하시겠습니까?');
                };

                // CSRF 토큰을 포함하는 hidden input 요소 생성
                var csrfInput = document.createElement('input');
                csrfInput.type = 'hidden';
                csrfInput.name = 'csrfmiddlewaretoken';
                csrfInput.value = getCookie('csrftoken');  // getCookie는 CSRF 토큰을 가져오는 함수입니다.
                form.appendChild(csrfInput);

                // '삭제' 버튼을 포함하는 input 요소 생성
                var deleteButton = document.createElement('input');
                deleteButton.className = 'btn';
                deleteButton.type = 'submit';
                deleteButton.value = '삭제';
                form.appendChild(deleteButton);

                // 'modal-revise' span 요소에 form 요소 추가
                modalRevise.appendChild(form);

                // 'detail-list' li 요소에 'modal-revise' span 요소 추가
                li.appendChild(modalRevise);
            }
            // 'detail-list' li 요소를 detailListArea에 추가
            detailListArea.appendChild(li);

            // 일정 수정 (즉시 실행 함수)
            reviseForm.onclick = (function(schedulePK) {
                return function() {
                    updateCalender(fullDate, schedulePK);
                };
            })(schedulePK);
        }
    }

    // 값이 비어있을땐 관리자만 열람가능
    if(!(contentText && timeText)){
        if(isAdmin){
            modal.style.display = 'block';
        }
    }
    else{
        modal.style.display = 'block';
    }

    // 'x' 버튼 클릭시 모달창 닫기
    closeBtn.onclick = function() {
        modal.style.display = 'none';
        if(contentText && timeText){
            modalRevise.style.display = 'none';
        }
    }

    if (isAdmin) { // 관리자이고 일정 추가 버튼이 눌러졌을때
        var add_sched = document.getElementsByClassName('add-sched')[0];
        add_sched.addEventListener('click', function() {
            createModal(fullDate);
        // 관리자인 경우에만 모달창 띄우기
        });
    }
}

// 일정 추가 모달
function createModal(fullDate){
    var modal     = document.getElementById('add-calender');
    var closeBtn  = document.getElementsByClassName('modal-close')[1];
    var date      = document.getElementById('startDate');
    var startTime = document.getElementById('startTime');
    var endTime   = document.getElementById('endTime');
    var allDay    = document.querySelector('label[for="allDay"]');
    var contents  = document.getElementById('id_contents');
    var title     = document.querySelector('#add-calender .modal-title .title');
    var form      = document.querySelector('#add-calender form');
    
    // 오늘날짜로 수정
    date.value = fullDate.toISOString().split('T')[0];
    startTime.value = '12:00';
    endTime.value = '13:00';
    contents.value = '';

    title.textContent = '일정 작성';
    
    // action 속성 삭제
    form.removeAttribute('action');

    // 종일 버튼 클래스 추가제거
    allDay.onclick = function() {
        if(allDay.classList.contains('btn')){
            allDay.classList.remove('btn');
            allDay.classList.add('btn-active');
            // 시간 비활성화
            startTime.disabled = true;
            endTime.disabled = true;
        } else{
            allDay.classList.add('btn');
            allDay.classList.remove('btn-active');

            startTime.disabled = false;
            endTime.disabled = false;
        }
    };

    // 모달창 열기
    modal.style.display = 'block';

    // 'x' 버튼 클릭시 모달창 닫기
    closeBtn.onclick = function() {
        modal.style.display = 'none';
    }
}

// 일정 수정
function updateCalender(fullDate,schedulePK){
    var modal = document.getElementById('add-calender');
    var closeBtn = document.getElementsByClassName('modal-close')[1];
    var date = document.getElementById('startDate');
    var startTime = document.getElementById('startTime');
    var endTime = document.getElementById('endTime');
    var contents = document.getElementById('id_contents');
    var title = document.querySelector('#add-calender .modal-title .title');
    var form = document.querySelector('#add-calender form');

    var dateString = fullDate.toISOString().split('T')[0];
    // 'data-date' 속성이 일정의 날짜와 일치하는 셀을 찾습니다.
    var cell = document.querySelector('.detail-list[data-pk="' + schedulePK + '"]');
    console.log(schedulePK);
    var timeRange = cell.querySelector('span.content-time').textContent;  // 해당 시간
    var times = timeRange.split('-');  // '-'을 기준으로 문자열을 분리합니다.
    var text = cell.querySelector('span.content-text').textContent;  // 해당 시간
    var allDay = document.querySelector('label[for="allDay"]'); //종일 버튼
    var allDayCheckbox = document.getElementById('allDay'); // 종일 체크박스

    // 오늘날짜로 수정
    date.value = dateString;
    startTime.value = times[0];
    endTime.value = times[1];
    contents.value = text;
    title.textContent = '일정 수정';
    
    // 시간이 비어있다면 종일일정
    if(startTime.value === ''){
        allDay.classList.remove('btn');
        allDay.classList.add('btn-active');
        // 시간 비활성화
        startTime.disabled = true;
        endTime.disabled = true;
        // 체크박스 활성화
        allDayCheckbox.checked = true;
    } else {
        allDay.classList.add('btn');
        allDay.classList.remove('btn-active');
        startTime.disabled = false;
        endTime.disabled = false;
        // 체크박스 비활성화
        allDayCheckbox.checked = false;
    }

    // 종일 버튼 클래스 추가제거
    allDay.onclick = function() {
        if(allDay.classList.contains('btn')){
            allDay.classList.remove('btn');
            allDay.classList.add('btn-active');
            // 시간 비활성화
            startTime.disabled = true;
            endTime.disabled = true;
        } else{
            allDay.classList.add('btn');
            allDay.classList.remove('btn-active');

            startTime.disabled = false;
            endTime.disabled = false;
        }
    };

    // action 속성 삭제
    form.action = 'calender/update/'+schedulePK+'/';
    
    // 모달창 열기
    modal.style.display = 'block';

    // 'x' 버튼 클릭시 모달창 닫기
    closeBtn.onclick = function() {
        modal.style.display = 'none';
    }
}

// 달력에 해당하는 일정 표시
function addSchedules(){
    var scheduleCount = {}; // 각 날짜의 일정 수를 저장하는 객체

    for (var i = 0; i < schedules.length; i++) {
        var schedule = schedules[i]; // 일정의 날짜를 가져옵니다.
        var date = new Date(schedule.fields.date); // 달력의 각 셀을 순회합니다.
        var allDay = schedule.fields.allDay; // 종일 여부
        var dateString = date.toISOString().split('T')[0];

        // 'data-date' 속성이 일정의 날짜와 일치하는 셀을 찾습니다.
        var cell = document.querySelector('.day[data-date="' + dateString + '"]');
        if (cell) { // 일치하는 셀이 있으면

            // div 요소 생성
            var div = document.createElement('div');
            div.className = 'cell-con-area';

            // 해당 날짜의 일정 수를 증가
            scheduleCount[dateString] = (scheduleCount[dateString] || 0) + 1;
            
            // 일정이 두 개 이상인 경우
            if (scheduleCount[dateString] > 1) {
                // 첫번째 요소 삭제
                var firstConArea = cell.querySelector('.cell-con-area');
                if (firstConArea) {
                    firstConArea.remove();
                }
                // 'n개의 일정'이라는 텍스트를 표시합니다.
                var time = document.createElement('span');
                time.textContent = scheduleCount[dateString] + '개의 일정';
                time.className = 'cell-con-time';

                // 배경색 변경
                var theme = document.createElement('span');
                theme.className = 'cell-con-background';

                div.appendChild(time);
                div.appendChild(theme);
                cell.appendChild(div);
            }
            else{
                // 시간
                var timeText = dateSchedules(schedule);
                // 일정 내용
                var contentText = schedule.fields.contents;

                // 일정의 날짜 추가
                var time = document.createElement('span');
                if (allDay == true){ // 종일 일정이라면
                    time.textContent = '종일 일정'; 
                }
                else { time.textContent = timeText; }
                time.className = 'cell-con-time';
            
                // 일정의 내용을 추가
                var content = document.createElement('span');
                content.textContent = contentText;
                content.className = 'cell-con-text';

                // 배경색 변경
                var theme = document.createElement('span');
                theme.className = 'cell-con-background';

                // div에 자식 요소 추가
                div.appendChild(time);
                div.appendChild(content);
                div.appendChild(theme);

                // div 요소 추가
                cell.appendChild(div);
            }
        }
    }
}

// 시간 변환 함수
function dateSchedules(schedule){
    // 시간 가져옴
    var startTime = schedule.fields.startTime;
    var endTime = schedule.fields.endTime;

    // 초 부분 제거
    startTime = startTime.substring(0, 5);
    endTime = endTime.substring(0, 5);

    // 시작 시간과 종료 시간을 함께 표시
    var timeText = startTime + '-' + endTime;
    return timeText;
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
