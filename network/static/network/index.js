var edits = document.getElementsByClassName("edit");
const contents = document.querySelectorAll(".content");

document.addEventListener('DOMContentLoaded', function() {
    for(var i = 0; i < edits.length; i++) {
        edits[i].addEventListener('click', handleEditClick);
    }
});

function handleEditClick(event) {
    event.preventDefault()
    var clickedEdit = event.target
    var postContainer = clickedEdit.closest(".post-container")
    content = postContainer.querySelector('.content')
    content.innerHTML = `<h1>test</h1>`
}
