document.addEventListener("DOMContentLoaded", function() {
    const sidebar = document.getElementById("sidebar");
    const mainContent = document.getElementById("mainContent");
    const toggleBtn = document.getElementById("sidebarToggle");

    document.querySelector(".log-in").addEventListener("click", () => {
        document.getElementById("form").style.display = "block"; 
    });

    document.querySelector(".close").addEventListener("click", (event) => {
        event.preventDefault(); 
        document.getElementById("form").style.display = "none";
    });

    document.querySelector(".signup-btn").addEventListener("click", () => {
        document.getElementById("sign-up").style.display = "block";
    });

    document.querySelector(".close-sign-up").addEventListener("click", (event) => {
        event.preventDefault(); 
        document.getElementById("sign-up").style.display = "none";
    });

    document.querySelector(".seller-login").addEventListener("click", () => {
        document.getElementById("seller-login").style.display = "block";
    });

    document.querySelector(".close-seller-login").addEventListener("click", (event) => {
        event.preventDefault(); 
        document.getElementById("seller-login").style.display = "none";
    });

    document.querySelector(".signup-seller-btn").addEventListener("click", () => {
        document.getElementById("signup-as-seller").style.display = "block";
    });

    document.querySelector(".close-signup-seller").addEventListener("click", (event) => {
        event.preventDefault(); 
        document.getElementById("signup-as-seller").style.display = "none";
    });

    toggleBtn.addEventListener("click", () => {
        sidebar.classList.toggle("open-sidebar");
        mainContent.classList.toggle("shift-content");
    });

});




