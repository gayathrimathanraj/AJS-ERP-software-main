document.getElementById("employeeSelect").addEventListener("change", function () {
    let selectedOption = this.options[this.selectedIndex];
    let empName = selectedOption.getAttribute("data-name");

    if (empName) {
        document.getElementById("usernameInput").value = empName;
    } else {
        document.getElementById("usernameInput").value = "";
    }
});

