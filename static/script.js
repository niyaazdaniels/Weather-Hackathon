function showLoading() {
    const loadingMessage = document.getElementById("loadingMessage");
    const weatherData = document.getElementById("weatherData");

    // Clear the current weather data
    weatherData.style.display = "none";

    // Show the loading message
    loadingMessage.style.display = "block";

    // Delay for loading spinner (optional)
    setTimeout(() => {
        loadingMessage.style.display = "none";
    }, 2000); // You can adjust this time if needed

    return true;
}

window.onload = function () {
    const elementsToFadeIn = document.querySelectorAll('.fade-in');
    elementsToFadeIn.forEach((element, index) => {
        setTimeout(() => {
            element.classList.add('fade-in');
        }, index * 300); // Adjust delay time between elements here (in milliseconds)
    });
};