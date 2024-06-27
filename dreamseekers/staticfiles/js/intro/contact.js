// 기본 좌표
var position = new naver.maps.LatLng(latitude, longitude);
var markerImageUrl = "{% static 'img/intro/contact/marker.png' %}";

var mapOptions = {
    center: position,
    zoom: 18,
    disableKineticPan: false,
    scrollWheel: false, // 마우스 스크롤 휠을 이용한 지도 확대/축소 허용 여부

    zoomControl: true,
    zoomControlOptions: {
        style: naver.maps.ZoomControlStyle.SMALL,
        position: naver.maps.Position.TOP_RIGHT
    }
};

var map = new naver.maps.Map('map', mapOptions);
//<img src = {% static "img/intro/contact/marker.png" %} alt="예제이미지">
// 마커 추가
var marker = new naver.maps.Marker({
    position: position,
    map: map,
});