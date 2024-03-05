// 기본 좌표
var position = new naver.maps.LatLng(35.2220973957462, 128.676299239476);
var markerImageUrl = "{% static 'img/intro/contact/marker.png' %}";

var mapOptions = {
    center: position,
    zoom: 15,
    disableKineticPan: false,

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

//https://map.naver.com/p/entry/place/1605260808