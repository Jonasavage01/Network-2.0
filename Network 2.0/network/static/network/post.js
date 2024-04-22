function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', function() {
    const editButtons = document.querySelectorAll('.edit-post-btn');
    const likeButtons = document.querySelectorAll('.like-btn');
    const unlikeButtons = document.querySelectorAll('.unlike-btn');
    const followButtons = document.querySelectorAll('.follow-btn');
    const unfollowButtons = document.querySelectorAll('.unfollow-btn');

    editButtons.forEach(button => {
        button.addEventListener('click', function() {
            const postId = this.getAttribute('data-post-id');
            const postContentElement = document.getElementById(`post-content-${postId}`);
            const currentContent = postContentElement.innerText.trim();

            const textarea = document.createElement('textarea');
            textarea.value = currentContent;

            const saveButton = document.createElement('button');
            saveButton.textContent = 'Save';
            saveButton.addEventListener('click', function() {
                const newContent = textarea.value;

                // Send an asynchronous request to update the post content
                fetch(`/post/${postId}/edit/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken') // Include CSRF token
                    },
                    body: JSON.stringify({ content: newContent })
                })
                .then(response => {
                    if (response.ok) {
                        // Update the post content on the page
                        postContentElement.innerText = newContent;
                    } else {
                        console.error('Failed to update post content');
                    }
                })
                .catch(error => console.error('Error:', error));
            });

            // Replace the post content with the editable textarea and save button
            postContentElement.innerHTML = '';
            postContentElement.appendChild(textarea);
            postContentElement.appendChild(saveButton);
        });
    });



    likeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const postId = this.getAttribute('data-post-id');
            fetch(`/post/${postId}/like/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken') 
                }
            })
            .then(response => {
                if (response.ok) {
                    // Update the like count on the page
                    const likesCount = this.parentElement.querySelector('.likes-count');
                    if (!this.disabled) {
                        likesCount.textContent = parseInt(likesCount.textContent) + 1;
                        this.disabled = true; // Disable the like button after click
                        // Enable the unlike button
                        const unlikeBtn = this.parentElement.querySelector('.unlike-btn');
                        unlikeBtn.disabled = false;
                    }
                } else {
                    console.error('Failed to like the post');
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });

    unlikeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const postId = this.getAttribute('data-post-id');
            fetch(`/post/${postId}/unlike/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken') 
                }
            })
            .then(response => {
                if (response.ok) {
                    // Update the like count on the page
                    const likesCount = this.parentElement.querySelector('.likes-count');
                    if (!this.disabled) {
                        likesCount.textContent = parseInt(likesCount.textContent) - 1;
                        this.disabled = true; // Disable the unlike button after click
                        // Enable the like button
                        const likeBtn = this.parentElement.querySelector('.like-btn');
                        likeBtn.disabled = false;
                    }
                } else {
                    console.error('Failed to unlike the post');
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });
});
