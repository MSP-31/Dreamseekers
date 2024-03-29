var imgInput = document.getElementById("img-input");
var fileInupt = document.getElementById("file-input");

// 선택한 이미지를 저장하는 배열
var selectedImgs = [];
// 파일 저장하는 배열
var selectedFiles = [];

// 이미지 선택시 이미지 업로드
imgInput.addEventListener("change",(event) => {
    const files = event.target.files;

    // 선택한 이미지들을 배열에 추가합니다.
    selectedImgs.push(...files);

    handleUpdate([...files]);
})

// 모든 .container-img 요소에 이벤트 리스너 추가
document.querySelectorAll('.container-img').forEach(addClickListener);

// 이미지처리 핸들러
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
                className: "img-delete-btn",
                innerHTML: '<span class="x-mark">X</span>',
            });
            // 숨겨진 체크박스 생성
            const hiddenCheckbox = el("imgInput", {
                type: "checkbox",
                className: "hidden-checkbox",
                style: "display: none;",
            });
            // 이미지 부모요소 생성
            const imgContainer = el("div",{ className: "container-img"},img,deleteBtn,hiddenCheckbox);
            preview.append(imgContainer);
            
            // 클릭 이벤트 리스너 추가
            addClickListener(imgContainer, file);

            console.log(imgInput.value);

        });
        // 파일을 읽고 url로 변환
        reader.readAsDataURL(file);
    });
};

// 파일 선택시 업로드
fileInupt.addEventListener("change",(event) => {
    const files = event.target.files;

    // 선택한 파일들을 배열에 추가합니다.
    selectedFiles.push(...files);

    fileHandleUpdate([...files]);
    console.log("파일선택핸들러")
})

// 모든 .container-file 요소에 이벤트 리스너 추가
document.querySelectorAll('.container-file').forEach(addClickListener);

// 이미지처리 핸들러
function fileHandleUpdate(fileList){
    const filePreview = document.getElementById("file-preview");

    // fileList 처리
    fileList.forEach((file)=>{
        const reader = new FileReader();
        reader.addEventListener("load",(event) => {
            // 이미지 자식요소 생성
            const files = el("span",{
                className: "embed-file",
                innerHTML: file.name,
            });
            // 삭제 버튼 생성
            const deleteBtn = el("span", {
                className: "file-delete-btn",
                innerHTML: 'X',
            });
            // 숨겨진 체크박스 생성
            const hiddenCheckbox = el("imgInput", {
                type: "checkbox",
                className: "hidden-checkbox",
                style: "display: none;",
            });
            // 이미지 부모요소 생성
            const fileContainer = el("li",{ className: "container-files"},files,deleteBtn,hiddenCheckbox);
            filePreview.append(fileContainer);
            
            // 클릭 이벤트 리스너 추가
            addClickListener(fileContainer, file);

            console.log(fileInupt.value);

        });
        // 파일을 읽고 url로 변환
        reader.readAsDataURL(file);
    });
};

// 이미지 제거 클릭 이벤트 리스너
function addClickListener(element, file) {
    element.addEventListener('click', function(e) {
        
        const fileDeleteBtn = e.target.closest('.file-delete-btn');
        const imgDeleteBtn = e.target.closest('.img-delete-btn');
        const xMark = e.target.closest('.x-mark');

        // 클릭된 요소가 .img-delete-btn 또는 .x-mark 요소인지 확인
        if (imgDeleteBtn || xMark) {
            // 선택한 파일들에서 해당 파일을 제거합니다.
            var index = selectedImgs.indexOf(file);
            if (index !== -1) {
                selectedImgs.splice(index, 1);
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

            // selectedImgs 배열의 파일들을 DataTransfer 객체에 추가합니다.
            for (var i = 0; i < selectedImgs.length; i++) {
                dataTransfer.items.add(selectedImgs[i]);
            }

            // imgInput 요소의 files 속성을 새로운 FileList 객체로 설정합니다.
            imgInput.files = dataTransfer.files;
        } else if(fileDeleteBtn){
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

            // fileInupt 요소의 files 속성을 새로운 FileList 객체로 설정합니다.
            fileInupt.files = dataTransfer.files;
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