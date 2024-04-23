document.addEventListener("DOMContentLoaded", function () {
    // Inicializa los componentes de Bootstrap
    var myModal = new bootstrap.Modal(document.getElementById('myModal'));
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });
});