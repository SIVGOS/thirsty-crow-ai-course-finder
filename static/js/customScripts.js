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

function checkVideoFindStatus(trackingIds) {
    if(trackingIds.length>30){
        setInterval(()=>{
            fetch(`/subject/track?tracking_ids=${trackingIds}`)
            .then(response => response.json())
            .then(data => {
                if(data.status === 'PROCESSED'){
                    location.reload();
                }
            })
            .catch(error => console.error('Error:', error));
        }, 3000);
    }
}

function deleteTest(subjectId) {
    const apiUrl = `/usersubject/delete/?tracking_id=${subjectId}`;
    const CSRFToken = getCookie('csrftoken');
    fetch(apiUrl, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': CSRFToken
            }
        }).then((response)=>{
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            location.reload();
        }
        ).catch(error => console.error('Error:', error));
}


function checkTopicCreation(trackingId) {
    const callbackUrl = `/topic/track/?tracking_id=${trackingId}`;
    setInterval( () => {
    fetch(callbackUrl)
    .then(response => {
            if (response.status === 200) {
                return response.json();
            }
            else if(response.status === 204){
                console.log('Topics not yet created.')
            }
            else {
                throw new Error(`HTTP Error! Status: ${response.status}`);
            }
    })
    .then(data => {
        const subjectId = data.subject_id;
        window.location = `/topics/?subject_id=${subjectId}`;
    }
    )
    .catch(error => {
            console.error('Error:', error);
        });
    }, 1000);
}

function subjectViewHandler(trackingId) {
    const CSRFToken = getCookie('csrftoken');
    document.querySelectorAll('.add-to-playlist').forEach(function(button) {
        button.addEventListener('click', function() {
            const videoId = button.getAttribute('data-video-id');
            const action = button.classList.contains('added') ? 'remove' : 'add';
            const url = '/playlist/' + action;
            const payload = {
                'tracking_id': trackingId,
                'video_id': videoId
            };

            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': CSRFToken // Add CSRF token for Django
                },
                body: JSON.stringify(payload)
            })
            .then((response) => {
                if(response.status === 200){
                    return response.json();
                }
                else{
                    throw "Failed to add video to playlist."
                }
            })
            .then(data => {
                if (data.status === 'success') {
                    if (action === 'add') {
                        button.textContent = 'Remove from Playlist';
                        button.classList.add('added', 'btn-danger');
                        button.classList.remove('btn-secondary');
                    } else {
                        button.textContent = 'Add to Playlist';
                        button.classList.remove('added', 'btn-danger');
                        button.classList.add('btn-secondary');
                    }
                } else {
                    alert('An error occurred while updating the playlist. Please try again.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while updating the playlist. Please try again.');
            });
        });
    });
}
