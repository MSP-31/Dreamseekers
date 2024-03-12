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

function showModal(fullDate){
    var modal = document.getElementById('calender-modal');
    var closeBtn = document.getElementsByClassName('modal-close')[0];
    var date = document.getElementsByClassName('selected-date')[0];
    var day = document.getElementsByClassName('selected-day')[0];
    var spanTime = document.getElementsByClassName('content_time')[0];
    var spanText = document.getElementsByClassName('content_text')[0];
    var modalRevise = document.getElementsByClassName('modal_revise')[0];
    var modalReviseForm = modalRevise.getElementsByTagName('form')[0];
    var modalReviseUpdate = modalRevise.getElementsByTagName('span')[0];

    var dateString = fullDate.toISOString().split('T')[0];  // 'YYYY-MM-DD' 형식
    dateString = dateString.replace(/-/g, '.'); // '-'를 '.'으로 바꾸기
    date.textContent = dateString; // 선택한 날짜 표시

    // 요일 표시
    var daysInKorean = ['일', '월', '화', '수', '목', '금', '토'];
    var dayInKorean = daysInKorean[fullDate.getDay()];
    day.textContent = dayInKorean+"요일";

    // 일정 내용 추가 부분
    for (var i = 0; i < schedules.length; i++) {
        var schedule = schedules[i]; // 일정의 날짜를 가져옵니다.
        var date = new Date(schedule.fields.date); // 달력의 각 셀을 순회합니다.
        if(JSON.stringify(date) === JSON.stringify(fullDate)){
            var timeText = dateSchedules(schedule);
            var contentText = schedule.fields.contents;
            var schedulePK = schedule.pk;
        }
    }

    // 일정의 날짜 / 내용 추가
    spanTime.textContent = timeText;
    spanText.textContent = contentText;

    // 일정 삭제
    modalReviseForm.action = 'calender/del/'+schedulePK+'/';

    // 일정 수정
    modalReviseUpdate.onclick = function() {
        updateCalender(fullDate,schedulePK);
    }

    // 값이 비어있을땐 관리자만 열람가능
    if(!(contentText && timeText)){
        if(isAdmin){
            modal.style.display = 'block';
        }
    }
    else{
        // 수정 삭제 버튼 추가
        if(isAdmin){
            modalRevise.style.display = 'block';
        }
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
    var modal = document.getElementById('add-calender');
    var closeBtn = document.getElementsByClassName('modal-close')[1];
    var date = document.getElementById('startDate');
    var startTime = document.getElementById('startTime');
    var endTime = document.getElementById('endTime');
    var contents = document.getElementById('id_contents');
    var title = document.querySelector('#add-calender .modal-title .title');
    var form = document.querySelector('#add-calender form');

    
    // 오늘날짜로 수정
    date.value = fullDate.toISOString().split('T')[0];
    startTime.value = '12:00';
    endTime.value = '13:00';
    contents.value = '';

    title.textContent = '일정 작성';
    
    // action 속성 삭제
    form.removeAttribute('action');

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
    var cell = document.querySelector('.day[data-date="' + dateString + '"] > div.cell_con_area');
    var timeRange = cell.querySelector('span.cell_con_time').textContent;  // 해당 시간
    var times = timeRange.split('-');  // '-'을 기준으로 문자열을 분리합니다.
    var text = cell.querySelector('span.cell_con_text').textContent;  // 해당 내용

    // 오늘날짜로 수정
    date.value = dateString;
    startTime.value = times[0];
    endTime.value = times[1];
    contents.value = text;
    title.textContent = '일정 수정';
    
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
    for (var i = 0; i < schedules.length; i++) {
        var schedule = schedules[i]; // 일정의 날짜를 가져옵니다.
        var date = new Date(schedule.fields.date); // 달력의 각 셀을 순회합니다.
        
        var dateString = date.toISOString().split('T')[0];

        // 'data-date' 속성이 일정의 날짜와 일치하는 셀을 찾습니다.
        var cell = document.querySelector('.day[data-date="' + dateString + '"]');
        if (cell) { // 일치하는 셀이 있으면
            // 시간
            var timeText = dateSchedules(schedule);
            // 일정 내용
            var contentText = schedule.fields.contents;

            // 일정의 날짜 추가
            var time = document.createElement('span');
            time.textContent = timeText;
            time.className = 'cell_con_time';
            
            // 일정의 내용을 추가
            var content = document.createElement('span');
            content.textContent = contentText;
            content.className = 'cell_con_text';

            // 일정의 내용을 추가
            var theme = document.createElement('span');
            theme.className = 'cell_con_background';

            // div 요소 생성
            var div = document.createElement('div');
            div.className = 'cell_con_area';
            div.appendChild(time);
            div.appendChild(content);
            div.appendChild(theme);

            // div 요소 추가
            cell.appendChild(div);
        }
    }
}

// 시간 변환 함수
function dateSchedules(schedule){
    // 시간 가져옴
    var startTime = schedule.fields.start_time;
    var endTime = schedule.fields.end_time;

    // 초 부분 제거
    startTime = startTime.substring(0, 5);
    endTime = endTime.substring(0, 5);

    // 시작 시간과 종료 시간을 함께 표시
    var timeText = startTime + '-' + endTime;
    return timeText;
}