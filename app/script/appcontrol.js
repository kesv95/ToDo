const areaSelect = document.getElementById("area");

areaSelect.addEventListener("change", function () {
    if (this.value === "") {
        this.classList.add("placeholder");
    } else {
        this.classList.remove("placeholder");
    }
});