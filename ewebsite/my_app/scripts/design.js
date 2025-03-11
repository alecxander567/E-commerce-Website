document.addEventListener("DOMContentLoaded", function () {
    const container = document.createElement("div");
    container.style.position = "fixed";
    container.style.top = "0";
    container.style.left = "0";
    container.style.width = "100vw";
    container.style.height = "100vh";
    container.style.zIndex = "-1"; // Keeps circles in the background
    document.body.appendChild(container);

    for (let i = 0; i < 3; i++) {
        let circle = document.createElement("div");
        circle.classList.add("circle");

        let size = Math.random() * 80 + 20; // Random size between 20px and 100px
        let x = Math.random() * window.innerWidth;
        let y = Math.random() * window.innerHeight;

        circle.style.width = `${size}px`;
        circle.style.height = `${size}px`;
        circle.style.left = `${x}px`;
        circle.style.top = `${y}px`;
        circle.style.background = `radial-gradient(circle, rgba(0, 255, 255, 0.2), transparent)`;
        circle.style.position = "absolute";

        container.appendChild(circle);
    }
});
