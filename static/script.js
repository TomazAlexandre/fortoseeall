document.getElementById('upload-form').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const formData = new FormData();
    const imageInput = document.getElementById('image-input').files[0];

    if (!imageInput) {
        alert("Por favor, selecione uma imagem para upload.");
        return;
    }

    formData.append('image', imageInput);

    fetch('/upload', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            // Mostrar a descrição gerada
            const descriptionDiv = document.getElementById('description');
            descriptionDiv.innerText = "Descrição: " + data.description;

            // Configurar o player de áudio
            const audioPlayer = document.getElementById('audio-player');
            audioPlayer.src = data.audio_url;
            audioPlayer.style.display = 'block';
            audioPlayer.play();
        }
    })
    .catch(error => {
        console.error('Erro ao processar a imagem:', error);
    });
});
