var editContentType = ""
var editContentId = ""
var removeContentType = ""
var removeContentId = ""

try {
    const refNode = document.querySelector("#id_pic");
    if (refNode != null) {
        const button = document.createElement('button');
        button.innerHTML = "Remove";
        button.setAttribute("type", "button");
        button.onclick = function () {
            document.getElementById("id_pic").value = null;
        };
        refNode.before(button);
    }

}
catch (error) {
    console.error(error)
}

try {
    var modal = document.getElementById('deleteModal')
    modal.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget
        const dataId = button.getAttribute('data-id')
        const dataType = button.getAttribute('data-type')
        // console.log()

        const modalBodyText = modal.querySelector('.modal-body p')
        const modalTitle = modal.querySelector('.modal-title')

        removeContentType = dataType
        removeContentId = dataId

        if (dataType === "comment") {
            modalBodyText.innerHTML = "Are you sure you want to remove this comment? This will remove all likes associated with it."
            modalTitle.innerHTML = "Remove Comment?"
        }
        else if (dataType === "post") {
            modalBodyText.innerHTML = "Are you sure you want to remove this post? This will remove all likes and comments."
            modalTitle.innerHTML = "Remove Post?"
        }
        else if (dataType === "upload") {
            modalBodyText.innerHTML = "Are you sure you want to remove this image?"
            modalTitle.innerHTML = "Remove Image?"
        }
        else if (dataType === "friend") {
            modalBodyText.innerHTML = "Are you sure you want to unfriend " + button.getAttribute('data-name') + "?"
            modalTitle.innerHTML = "Remove Friend?"
        }

        // var deleteBtn = modal.querySelector('#delete-btn')//.setAttribute('value', postId)
        // deleteBtn.addEventListener('click', function (event) {

        //     // event.stopImmediatePropagation();
        //     const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        //     if (dataType === 'post') {
        //         deleteURL = '/post/deletePost/'
        //         dataDict = {
        //             'csrfmiddlewaretoken': csrftoken,
        //             'post': dataId,
        //         }
        //     }
        //     else if (dataType === 'comment') {
        //         deleteURL = '/post/deletePost/'
        //         dataDict = {
        //             'csrfmiddlewaretoken': csrftoken,
        //             'comment': dataId,
        //         }
        //     }
        //     else if (dataType === 'upload') {
        //         deleteURL = '/uploads/'
        //         dataDict = {
        //             'csrfmiddlewaretoken': csrftoken,
        //             'remove_upload': dataId,
        //         }
        //     }
        //     else if (dataType === 'friend') {
        //         deleteURL = '/friend/unfriend/'
        //         dataDict = {
        //             'csrfmiddlewaretoken': csrftoken,
        //             'friend_id': dataId,
        //         }
        //     }

        //     $.ajax({
        //         url: deleteURL,
        //         type: "POST",
        //         data: dataDict,
        //         dataType: 'json',
        //         success: function (context) {
        //             if (context['server_error']) {
        //                 window.location = "/"
        //             }
        //             else if (context['login_required']) window.location = '/login/'
        //             else {
        //                 location.reload()
        //                 // document.querySelector("#" + dataType + "-" + dataId).remove();
        //             }
        //         }
        //     })

        // })
    })
}
catch (error) {
    console.error(error);
}

try {
    var exampleModal = document.getElementById('exampleModal')

    exampleModal.addEventListener('show.bs.modal', function (event) {

        var button = event.relatedTarget
        var dataId = button.getAttribute('data-id')
        var dataType = button.getAttribute('data-type')

        var modalTitle = exampleModal.querySelector('.modal-title')
        var modalBodyTextArea = exampleModal.querySelector('.modal-body textarea')

        modalTitle.textContent = 'Edit ' + dataType
        modalBodyTextArea.value = document.querySelector("#text-" + dataId + "-" + dataType).textContent

        editContentType = dataType
        editContentId = dataId
    })
}
catch (error) {
    console.error(error);
}


function editPost() {

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const modalBodyTextArea = document.getElementById('exampleModal').querySelector('.modal-body textarea')
    const newText = modalBodyTextArea.value
    dataDict = {}
    dataDict['csrfmiddlewaretoken'] = csrftoken
    dataDict[editContentType] = editContentId
    dataDict['text'] = newText

    // console.log(dataDict)

    $.ajax({
        url: '/post/updatePost/',
        type: "POST",
        data: dataDict,
        dataType: 'json',
        success: function (context) {
            if (context['server_error']) window.location = "/"
            else if (context['login_required']) window.location = '/login/'
            else if (context['success']) {
                var innerHtml = ""
                if (editContentType === "comment") innerHtml = '<small>' + newText + '</small>'
                else if (editContentType === "post") innerHtml = newText
                document.querySelector("#text-" + editContentId + "-" + editContentType).innerHTML = innerHtml
            }
        }
    })
}

function removeContent() {
    console.log(removeContentType, removeContentId)
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    dataDict = {}
    dataDict['csrfmiddlewaretoken'] = csrftoken
    dataDict[removeContentType] = removeContentId

    if (removeContentType === 'post' || removeContentType === 'comment') removeUrl = '/post/deletePost/'
    else if (removeContentType === 'upload') removeUrl = '/uploads/removeUpload/'
    else if (removeContentType === 'friend') removeUrl = '/friend/unfriend/'

    $.ajax({
        url: removeUrl,
        type: "POST",
        data: dataDict,
        dataType: 'json',
        success: function (context) {
            if (context['server_error']) window.location = "/"
            else if (context['login_required']) window.location = '/login/'
            else if (context['success']) location.reload()
        }
    })
}

function setProfilePic(uploadId) {
    try {
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        $.ajax({
            url: "/uploads/setProfilePic/",
            type: "POST",
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'upload': uploadId,
            },
            dataType: 'json',
            success: function (context) {
                if (context['login_required']) window.location = '/login/'
                else if (context['server_error']) window.location = '/'
                else {
                    location.reload()
                }
            }
        })
    }
    catch (error) {
        console.error(error);
    }
}

function addLikeToPost(postId) {
    // console.log("about to add like to post:", postId);
    try {
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        $.ajax({
            url: "/post/likePost/",
            type: "POST",
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'post_id': postId,
            },
            dataType: 'json',
            success: function (context) {
                if (context['login_required']) window.location = '/login/';
                else if (context['server_error']) window.location = '/'
                else if (context['not_friends']) {
                    console.log("this is happening")
                    location.reload();
                }
                else {
                    btn = document.querySelector('#post-like-btn-' + postId);
                    if (context['is_liked']) {
                        btn.innerHTML = '<i class="fs-5 bi-hand-thumbs-up-fill"></i><span class="d-none d-md-inline"> Liked!</span>'
                    }
                    else btn.innerHTML = '<i class="fs-5 bi-hand-thumbs-up"></i><span class="d-none d-md-inline"> Like</span>'

                    document.querySelector("#post-like-comment-count-" + postId).innerHTML = context['like_count'] + " Likes, " + context['comment_count'] + " Comments"
                }
            }
        })
    }
    catch (error) {
        console.error("Error liking post", error);
    }
}

function addCommentToPost(postId) {
    try {
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const comment_text = document.querySelector('#text-' + postId + "-post-comment").value;

        // console.log(comment_text)
        $.ajax({
            url: "/post/addPostComment/",
            type: "POST",
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'post_id': postId,
                'comment_text': comment_text
            },
            dataType: 'json',
            success: function (context) {
                if (context['login_required']) window.location = '/login/';
                else if (context['not_friends'] || context['server_error']) {
                    window.location = '/'
                }
                else if (context['success']) {
                    document.querySelector('#text-' + postId + "-post-comment").value = ""
                    location.reload();
                }
            }
        })
    }
    catch (error) {
        console.error("Error in commenting post", error);
    }
}

function likePostComment(postCommentId) {
    try {
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        // console.log(postCommentId, sentiment);
        $.ajax({
            url: "/post/likePostComment/",
            type: "POST",
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'post_comment_id': postCommentId,
            },
            dataType: 'json',
            success: function (context) {
                if (context['login_required']) window.location = '/login/';
                else if (context['not_friends'] || context['server_error']) window.location = '/';
                else {
                    like_btn = document.querySelector('#like-comment-btn-' + postCommentId);
                    if (context['liked']) {
                        like_btn.innerHTML = '<i class="bi bi-emoji-smile-fill"></i> <span class="text-muted">' + context['like_count'] + '</span>'
                    }
                    else {
                        like_btn.innerHTML = '<i class="bi bi-emoji-smile"></i> <span class="text-muted">' + context['like_count'] + '</span>'
                    }
                }
            }
        })
    }
    catch (error) {
        console.error("Error in commenting post", error);
    }
}