var edits = document.getElementsByClassName("edit");
const contents = document.querySelectorAll(".content");
const likes = document.querySelectorAll(".like-icon")


document.addEventListener('DOMContentLoaded', function() {
    for(var i = 0; i < edits.length; i++) {
        edits[i].addEventListener('click', handleEditClick);
    }
    for(var i =0; i < likes.length; i++) {
        likes[i].addEventListener('click', handleLikeClick);
    }
});

function handleLikeClick(event) {
    console.log("like")
}

function handleEditClick(event) {
    event.preventDefault()
    var clickedEdit = event.target
    clickedEdit.style.visibility = "hidden"
    var postContainer = clickedEdit.closest(".post-container")
    var user = postContainer.querySelector(".user")
    var content = postContainer.querySelector('.content')
    origin_content = content.textContent

    content.innerHTML = `
        <textarea id="post" rows="7" cols="250" name="content">
        ${origin_content}
        </textarea>
        <button id="save-btn" type="submit" class="btn btn-primary">Save</button>
    `

    postContainer.querySelector('#save-btn').addEventListener('click', function() {
        new_content = postContainer.querySelector('#post').value
        var postId = user.dataset.postId
        console.log(postId)
        var csrfToken = getCSRFTokenFromCookie('csrftoken');
        fetch(`/editpost/${postId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken, // Include the CSRF token in the headers
            },
            body: JSON.stringify({
                content: new_content
            })
        })
        .catch(error => {
            // Handle errors
            console.error('Error fetching data:', error);
        });
        clickedEdit.style.visibility = "visible"
        content.innerHTML = new_content
    })
}


function getCSRFTokenFromCookie(cookieName) {
    var value = "; " + document.cookie;
    var parts = value.split("; " + cookieName + "=");
    if (parts.length === 2) return parts.pop().split(";").shift();
}