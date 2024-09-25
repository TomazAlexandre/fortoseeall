document.getElementById('upload-form').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const formData = new FormData();
    const imageInput = document.getElementById('image-input').files[0];

    if (!imageInput) {
        alert("Por favor, selecione uma imagem para upload.");
        return;
    }

    formData.append('image', imageInput);

    // Exibe mensagem de carregamento
    const descriptionDiv = document.getElementById('description');
    descriptionDiv.style.display = 'none';
    descriptionDiv.innerText = "Analisando a imagem...";
    descriptionDiv.style.display = 'block';

    // Limpar o player de áudio
    const audioPlayer = document.getElementById('audio-player');
    audioPlayer.style.display = 'none';
    audioPlayer.src = '';

    // Enviar a imagem para a API
    fetch('/upload', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            descriptionDiv.innerText = data.error;
        } else {
            // Mostrar a descrição gerada
            descriptionDiv.innerText = "Descrição: " + data.description;
            descriptionDiv.classList.remove('alert-info');
            descriptionDiv.classList.add('alert-success');

            // Configurar o player de áudio
            audioPlayer.src = data.audio_url;
            audioPlayer.style.display = 'block';
        }
    })
    .catch(error => {
        descriptionDiv.innerText = "Erro ao processar a imagem: " + error;
        descriptionDiv.classList.remove('alert-info');
        descriptionDiv.classList.add('alert-danger');
    });
});
