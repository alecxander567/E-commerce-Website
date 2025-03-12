const toggleButton = document.getElementById("toggleButton");
const menuTitle = document.getElementById("menu-title");
const collapseElement = document.getElementById("navbarToggleExternalContent");

document.getElementById("form").style.display = "none";

document.querySelectorAll(".log-in").forEach(button => {
    button.addEventListener("click", () => {
        document.getElementById("form").style.display = "block"; 
    });
});

document.querySelector(".close").addEventListener("click", (event) => {
    event.preventDefault(); 
    document.getElementById("form").style.display = "none";
});

collapseElement.addEventListener("show.bs.collapse", function () {
    menuTitle.style.display = "none"; // Hide text when menu opens
});

collapseElement.addEventListener("hidden.bs.collapse", function () {
    menuTitle.style.display = "inline"; // Show text when menu closes
});
