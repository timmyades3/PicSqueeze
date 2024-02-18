let slider = document.getElementById("myRange");
let output = document.getElementById("rangeValue");

output.innerHTML = "Compress Size: " + slider.value + "%"; // Display the default slider value

slider.oninput = function() {
    output.innerHTML = "Compress Size: " + this.value + "%";
}
