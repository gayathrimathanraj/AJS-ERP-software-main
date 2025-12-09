function previewPhoto(event) {
    const output = document.getElementById('photoPreview');
    output.src = URL.createObjectURL(event.target.files[0]);
    output.onload = function () {
        URL.revokeObjectURL(output.src);
    }
}

