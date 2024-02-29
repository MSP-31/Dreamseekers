var input = document.getElementById("img-input");

// 선택한 이미지를 저장하는 배열
var selectedFiles = [];

// 파일 선택시 이미지 업로드
input.addEventListener("change",(event) => {
    const files = event.target.files;

    // 선택한 파일들을 배열에 추가합니다.
    selectedFiles.push(...files);

    handleUpdate([...files]);
    console.log("파일선택핸들러")
})

// 모든 .container-img 요소에 이벤트 리스너 추가
document.querySelectorAll('.container-img').forEach(addClickListener);

// 파일처리 핸들러
function handleUpdate(fileList){
    const preview = document.getElementById("preview");

    // fileList 처리
    fileList.forEach((file)=>{
        const reader = new FileReader();
        reader.addEventListener("load",(event) => {
            // 이미지 자식요소 생성
            const img = el("img",{
                className: "embed-img",
                src: event.target?.result,
            });
            // 삭제 버튼 생성
            const deleteBtn = el("span", {
                className: "delete-btn",
                innerHTML: '<span class="x-mark">X</span>',
            });
            // 숨겨진 체크박스 생성
            const hiddenCheckbox = el("input", {
                type: "checkbox",
                className: "hidden-checkbox",
                style: "display: none;",
            });
            // 이미지 부모요소 생성
            const imgContainer = el("div",{ className: "container-img"},img,deleteBtn,hiddenCheckbox);
            preview.append(imgContainer);
            
            // 클릭 이벤트 리스너 추가
            addClickListener(imgContainer, file);

            console.log(input.value);

        });
        // 파일을 읽고 url로 변환
        reader.readAsDataURL(file);
    });
};

// 클릭 이벤트 리스너
function addClickListener(element, file) {
    element.addEventListener('click', function(e) {
        console.log(e.target)

        // 클릭된 요소가 .delete-btn 또는 .x-mark 요소인지 확인
        const deleteBtn = e.target.closest('.delete-btn');
        const xMark = e.target.closest('.x-mark');

        if (deleteBtn || xMark) {
            // 선택한 파일들에서 해당 파일을 제거합니다.
            var index = selectedFiles.indexOf(file);
            if (index !== -1) {
                selectedFiles.splice(index, 1);
            }

            // 클릭된 요소 숨기기
            element.style.display = 'none';
            // 숨겨진 체크박스 요소 찾기
            const hiddenCheckbox = element.querySelector('.hidden-checkbox');
            // 체크박스 상태 변경
            hiddenCheckbox.checked = !hiddenCheckbox.checked;
            console.log("체크")

            // DataTransfer 객체를 생성합니다.
            var dataTransfer = new DataTransfer();

            // selectedFiles 배열의 파일들을 DataTransfer 객체에 추가합니다.
            for (var i = 0; i < selectedFiles.length; i++) {
                dataTransfer.items.add(selectedFiles[i]);
            }

            // input 요소의 files 속성을 새로운 FileList 객체로 설정합니다.
            input.files = dataTransfer.files;
        }
    });
}

// el함수 정의
function el(nodeName, attributes, ...children){
    const node =
    nodeName === "fragment"
        ? document.createDocumentFragment()
        : document.createElement(nodeName);
    
    Object.entries(attributes).forEach(([key,value]) => {
        if (key === "events"){
            Object.entries(value).forEach(([type, listener]) => {
                node.addEventListener(type,listener);
            });
        } else if (key in node){
            try{
                node[key] = value;
            }catch(err){
                node.setAttribute(key, value);
            }
        } else{
            node.setAttribute(key,value);
        }
    });

    children.forEach((childNode) => {
        if (typeof childNode === "string"){
            node.appendChild(document.createTextNode(childNode));
        } else {
            node.appendChild(childNode);
        }
    });

    return node;
}