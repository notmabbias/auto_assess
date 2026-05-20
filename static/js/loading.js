document.addEventListener("DOMContentLoaded", function() {
    const container = document.getElementById("loading-container");
    if (!container) return;
    
    const uuid = container.getAttribute("data-uuid");
    
    // execute the backend process without locking the UI thread
    fetch(`/process/${uuid}`, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            // forward user to the formatted results view
            window.location.href = `/results/${uuid}`;
        } else {
            alert("Analysis failed: " + data.message);
        }
    })
    .catch(error => {
        console.error("Error processing vehicle analysis:", error);
        alert("A system error occurred during analysis execution.");
    });
});