const menuButton = document.querySelector(".mobile_menu-btn");
const modalOverlay = document.querySelector(".overlay");
const menuCloseButton = document.querySelector(".mobile_menu-btn-close");

const menuToggleHandler = () => {
    const navMenu = document.querySelector(".mobile__landing-menu");

    navMenu.classList.toggle("hidden");
    menuButton.classList.toggle("hidden");
    menuCloseButton.classList.toggle("hidden");
    modalOverlay.classList.toggle("hidden");

    let navAriaHidden = navMenu.classList.contains("hidden") ? "true" : "false";
    navMenu.ariaHidden = navAriaHidden;
}

menuButton.addEventListener('click', menuToggleHandler )

modalOverlay.addEventListener('click', menuToggleHandler)

menuCloseButton.addEventListener('click', menuToggleHandler)