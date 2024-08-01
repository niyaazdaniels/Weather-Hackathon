function showLoading() {
    const loadingMessage = document.getElementById("loadingMessage");
    loadingMessage.style.display = "block";
    setTimeout(() => {
        loadingMessage.style.display = "none";
    }, 3000); 
}

window.onload = function () {
    const elementsToFadeIn = document.querySelectorAll('.fade-in');
    elementsToFadeIn.forEach((element, index) => {
        setTimeout(() => {
            element.classList.add('fade-in');
        }, index * 300); 
    });
};