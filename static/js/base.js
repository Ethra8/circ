document.addEventListener("DOMContentLoaded", () => {
    // Close alert messages
    document.querySelectorAll(".alert .close").forEach(closeButton => {
        closeButton.addEventListener("click", () => {
            const alert = closeButton.closest(".alert");
            if (!alert) return;

            alert.classList.add("fade");
            setTimeout(() => alert.remove(), 300);
        });
    });

    // Main mobile nav
    const toggler = document.querySelector(".navbar-toggler");
    const mainNav = document.getElementById("main-nav");

    if (toggler && mainNav) {
        toggler.addEventListener("click", () => {
            const open = mainNav.classList.toggle("show");
            toggler.setAttribute("aria-expanded", open);
        });

        mainNav.querySelectorAll(".nav-link").forEach(link => {
            link.addEventListener("click", () => {
                if (window.innerWidth < 992) {
                    mainNav.classList.remove("show");
                    toggler.setAttribute("aria-expanded", "false");
                }
            });
        });
    }

    // User dropdown
    const userToggle = document.getElementById("user-options");
    const userMenu = userToggle?.nextElementSibling;

    if (userToggle && userMenu) {
        userToggle.addEventListener("click", e => {
            e.preventDefault();
            const open = userMenu.classList.toggle("show");
            userToggle.setAttribute("aria-expanded", open);
        });

        document.addEventListener("click", e => {
            if (!userToggle.contains(e.target) && !userMenu.contains(e.target)) {
                userMenu.classList.remove("show");
                userToggle.setAttribute("aria-expanded", "false");
            }
        });
    }
});