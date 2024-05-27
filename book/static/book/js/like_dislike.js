// static/js/like_dislike.js

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.like-button').forEach(button => {
        button.addEventListener('click', function() {
            const postId = this.getAttribute('data-post-id');
            fetch(`/post/${postId}/like/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                },
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById(`likes-${postId}`).textContent = data.likes;
                document.getElementById(`dislikes-${postId}`).textContent = data.dislikes;
            });
        });
    });

    document.querySelectorAll('.dislike-button').forEach(button => {
        button.addEventListener('click', function() {
            const postId = this.getAttribute('data-post-id');
            fetch(`/post/${postId}/dislike/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                },
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById(`dislikes-${postId}`).textContent = data.dislikes;
                document.getElementById(`likes-${postId}`).textContent = data.likes;
            });
        });
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
