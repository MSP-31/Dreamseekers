
// 대댓글 작성폼
$(document).ready(function(){
    $(".comment").click(function(){
        var commentId = $(this).data("comment-id");
        $(".reply_write").not("#reply_write_" + commentId).hide();
        $("#reply_write_" + commentId).toggle();
    });
});

// 댓글 수정 기능
const modify_btn = document.querySelectorAll(".comment-modify");
modify_btn.forEach(button => {
    button.addEventListener('click',() => {
        const commentId = button.getAttribute('data-comment-id');

        //요소 선택
        const comment = button.closest(`.cmt${commentId}`);
        const commentModify = document.querySelector(`.cmt-modify${commentId}`);

        comment.style.display = 'none';
        commentModify.style.display = 'block';
        
        // 취소 버튼 동작
        const cancel_btn = document.querySelector(`.cancel-${commentId}`);
        cancel_btn.addEventListener('click',() => {
            commentModify.style.display = 'none';
            comment.style.display = 'block';
        });
    });
});

/*
cancel_btn.forEach(button => {
    button.addEventListener('click',() => {
        const commentId = button.getAttribute('data-comment-id');
        console.log(commentId)

        //요소 선택
        const comment = button.closest(`.cmt${commentId}`);
        const commentModify = document.querySelector(`.cmt-modify${commentId}`);

        comment.style.display = 'block';
        commentModify.style.display = 'none';
    })
})
*/

