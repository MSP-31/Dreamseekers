
// 대댓글 작성폼
$(document).ready(function(){
    $(".comment").click(function(){
        var commentId = $(this).data("comment-id");
        $(".reply_write").not("#reply_write_" + commentId).hide();
        $("#reply_write_" + commentId).toggle();
    });
});