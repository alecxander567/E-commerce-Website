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