document.addEventListener('DOMContentLoaded', function() {
    
    fetch('/allpost')
    .then(response => response.json())
    .then(all_post => {
        console.log(all_post)
        const post_section = document.querySelector(".post-section");
        all_post.forEach( post => {
            const post_container = document.createElement('div');
            post_container.innerHTML = `
                <h3 class="user"> ${post.user} </h3>
                <p class="content"> ${post.content}</p>
                <h5 class="timestamp">${post.timestamp}</h3>
                <p class="like"> ${post.like}</p>

                
            `
            post_container.classList.add('post-container')
            post_section.append(post_container);
        })
        
    })
})