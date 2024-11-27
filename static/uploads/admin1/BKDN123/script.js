document.getElementById("show-message").addEventListener("click", function() {
    var message = document.getElementById("hidden-message");
    if (message.style.display === "none" || message.style.display === "") {
        message.style.display = "block";
    } else {
        message.style.display = "none";
    }
});
