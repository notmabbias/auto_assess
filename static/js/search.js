// initalize when loaded
document.addEventListener("DOMContentLoaded", function() {
    
    // auto expanding text areas
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        textarea.addEventListener('input', function() {
            this.style.height = '';
            this.style.height = this.scrollHeight + 'px';
        });
    });

    // CARFAX reveal button logic
    const carfaxBtn = document.getElementById('carfax_btn');
    const carfaxRow = document.getElementById('carfax_row');
    
    if (carfaxBtn && carfaxRow) {
        carfaxBtn.addEventListener('click', function() {
            carfaxRow.style.display = 'table-row';
            this.style.display = 'none';
        });
    }
});