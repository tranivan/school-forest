  fetch("navbar.html")
              .then(response => response.text())
              .then(data => {
                document.getElementById("header").innerHTML = data;

                // Now attach scroll listener after navbar is loaded
                document.addEventListener('scroll', () => {
                  const navbar = document.getElementById('navbar');
                  if (window.scrollY > 0) {
                    navbar.classList.replace("bg-transparent", "bg-black");
                  } else {
                    navbar.classList.replace("bg-black", "bg-transparent");
                  }
                });
              });