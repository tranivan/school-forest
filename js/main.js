const navbar = document.getElementById('navbar');


document.addEventListener('scroll', () => {
    if (window.scrollY > 0) {
        navbar.classList.replace("bg-transparent", "bg-black");
            navbar.classList.replace("text-forest", "text-background-primary");
        } else {
            navbar.classList.replace("bg-black", "bg-transparent");
            navbar.classList.replace("text-background-primary", "text-forest");
        }
});

