function isValidUUID(uuid) {
    const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[4][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
    return uuidRegex.test(uuid);
}

function checkStatus(trackingId) {
    fetch(`/subject/track?tracking_id=${trackingId}`)
        .then(response => response.json())
        .then(data => {
            if(data.status === 'PROCESSED'){
                location.reload()
            }
        })
        .catch(error => console.error('Error:', error));
}

function pollStatuses(trackingIds) {
    let trackingIds = trackingIds.split('|')
    trackingIds.forEach((trackingId) => {
        if(isValidUUID(trackingId)){
            setInterval(() => {
                checkStatus(trackingId)
            }, 5000)
        }
    });
}
