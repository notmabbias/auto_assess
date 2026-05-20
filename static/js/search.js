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

    const vehicleDatabase = {
        "2006": {
            "Honda": ["Civic"]
        },
        "2007": {
            "Nissan": ["350Z"]
        },
        "2012": {
            "Volkswagen": ["Golf R"]
        },
        "2015": {
            "Chevrolet": ["Corvette"],
            "Hyundai": ["Genesis Coupe"]
        },
        "2026": {
            "Volkswagen": ["Golf GTI"]
        }
    };

    const yearSelect = document.getElementById('vehicle_year');
    const makeSelect = document.getElementById('vehicle_make');
    const modelSelect = document.getElementById('vehicle_model');
    const resetBtn = document.getElementById('reset_btn');

    yearSelect.addEventListener('change', function() {
        makeSelect.innerHTML = '<option value="" disabled selected>-- Select Make --</option>';
        modelSelect.innerHTML = '<option value="" disabled selected>-- Select Model --</option>';
        modelSelect.disabled = true;
        
        const makes = Object.keys(vehicleDatabase[this.value] || {});
        makes.forEach(make => {
            const opt = document.createElement('option');
            opt.value = make;
            opt.textContent = make;
            makeSelect.appendChild(opt);
        });
        makeSelect.disabled = false;
    });

    makeSelect.addEventListener('change', function() {
        modelSelect.innerHTML = '<option value="" disabled selected>-- Select Model --</option>';
        
        const selectedYear = yearSelect.value;
        const models = vehicleDatabase[selectedYear]?.[this.value] || [];
        models.forEach(model => {
            const opt = document.createElement('option');
            opt.value = model;
            opt.textContent = model;
            modelSelect.appendChild(opt);
        });
        modelSelect.disabled = false;
    });

    resetBtn.addEventListener('click', function() {
        makeSelect.disabled = true;
        modelSelect.disabled = true;
    });
});