function createCircles(numCircles) {
    for (let i = 0; i < numCircles; i++) {
        let circle = document.createElement("div");
        circle.classList.add("circle");
        
        let size = Math.random() * 100 + 20; // Circle size (20px - 120px)
        let x = Math.random() * window.innerWidth;
        let y = Math.random() * window.innerHeight;
        let colors = ["#FF5733", "#33FF57", "#5733FF", "#FFC300", "#FF33A1"];
        let color = colors[Math.floor(Math.random() * colors.length)];

        circle.style.width = `${size}px`;
        circle.style.height = `${size}px`;
        circle.style.background = color;
        circle.style.left = `${x}px`;
        circle.style.top = `${y}px`;

        document.body.appendChild(circle);
    }
}

createCircles(50);

