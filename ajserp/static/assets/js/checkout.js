// ===============================
//  CHECK-IN PAGE JAVASCRIPT
// ===============================

// --------------------------------
// 1️⃣  Work Completion (YES / NO)
// --------------------------------

function toggleWorkOptions() {
    let options = document.getElementById("workOptions");

    if (options.style.display === "none" || options.style.display === "") {
        options.style.display = "block";
    } else {
        options.style.display = "none";
    }
}

function selectWork(status) {
    // store selected work status
    localStorage.setItem("work_status", status);

    // highlight button UI
    let yesBtn = document.querySelector("#workOptions button.btn-success");
    let noBtn = document.querySelector("#workOptions button.btn-danger");

    if (status === "yes") {
        yesBtn.style.opacity = "1";
        noBtn.style.opacity = "0.5";
    } else {
        yesBtn.style.opacity = "0.5";
        noBtn.style.opacity = "1";
    }

    // enable checkout button
    document.getElementById("checkout_btn").style.opacity = "1";
    document.getElementById("checkout_btn").style.pointerEvents = "auto";

    console.log("Work completed:", status);
}


// --------------------------------
// 2️⃣  Checkout Action
// --------------------------------

function checkoutAction() {
    let status = localStorage.getItem("work_status");

    if (!status) {
        alert("Please select Yes or No before checkout.");
        return false;
    }

    // Redirect to checkout view with status
    window.location.href = "/ajserp/checkout/?work_completed=" + status;

    return false;
}


// --------------------------------
// 3️⃣  Image Upload Toggle
// --------------------------------

function toggleImageUpload() {
    let box = document.getElementById("imageUploadBox");

    if (box.style.display === "none" || box.style.display === "") {
        box.style.display = "block";
    } else {
        box.style.display = "none";
    }
}


// --------------------------------
// 4️⃣ Automatic Submit Handler (Optional)
// --------------------------------
// If your image upload form is POST inside same page, it works automatically.
// No JS needed here unless you want AJAX upload.
// --------------------------------

// OPTIONAL: Prevent form submission if no image selected
document.addEventListener("DOMContentLoaded", function () {
    let form = document.getElementById("imageForm");

    if (form) {
        form.addEventListener("submit", function (e) {
            let fileInput = form.querySelector("input[name='image']");

            if (!fileInput.value) {
                e.preventDefault();
                alert("Please select an image to upload.");
            }
        });
    }
});

