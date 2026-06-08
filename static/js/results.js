// extract UUID from the current URL path (/results/<uuid>)
document.addEventListener("DOMContentLoaded", function() {
    const urlParts = window.location.pathname.split('/');
    const searchId = urlParts[urlParts.length - 1];
    
    const idField = document.getElementById('search_id_field');
    if (idField) {
        idField.value = searchId;
    }
});

function copySearchID() {
    const idField = document.getElementById('search_id_field');
    idField.select();
    idField.setSelectionRange(0, 99999); 
    
    navigator.clipboard.writeText(idField.value).then(() => {
        const status = document.getElementById('copy_status');
        status.style.display = 'inline-block';
        setTimeout(() => { status.style.display = 'none'; }, 2000);
    }).catch(err => {
        console.error('Failed to copy text: ', err);
    });
}