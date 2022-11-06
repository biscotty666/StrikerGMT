const card = document.querySelectorAll(".flip-card-inner");

card.forEach((card) => {
    card.addEventListener("click", () => {
        card.classList.toggle("is-flipped");
    });
})