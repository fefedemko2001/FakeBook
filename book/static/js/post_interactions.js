document.getElementById('like-button').addEventListener('click', function() {
    fetch("{% url 'post-like' post.pk %}", {
        method: 'POST',
        headers: {
            'X-CSRFToken': '{{ csrf_token }}',
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('like-button').innerHTML = `<i class="bi bi-hand-thumbs-up"></i> Like (${data.likes})`;
        document.getElementById('dislike-button').innerHTML = `<i class="bi bi-hand-thumbs-down"></i> Dislike (${data.dislikes})`;
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('dislike-button').addEventListener('click', function() {
    fetch("{% url 'post-dislike' post.pk %}", {
        method: 'POST',
        headers: {
            'X-CSRFToken': '{{ csrf_token }}',
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('like-button').innerHTML = `<i class="bi bi-hand-thumbs-up"></i> Like (${data.likes})`;
        document.getElementById('dislike-button').innerHTML = `<i class="bi bi-hand-thumbs-down"></i> Dislike (${data.dislikes})`;
    })
    .catch(error => console.error('Error:', error));
});