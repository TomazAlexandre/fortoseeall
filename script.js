document.getElementById('uploadForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    let formData = new FormData();
    let imageFile = document.getElementById('imageInput').files[0];

    formData.append("image", imageFile);

    const response = await fetch('/upload', {
        method: 'POST',
        body: formData
    });

    const result = await response.json();
    document.getElementById('response').innerText = result.description;
});
