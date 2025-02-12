let audioBase64 = null;  // Variável global para armazenar o áudio

// Exibe a imagem selecionada
document.getElementById('imageInput').addEventListener('change', function (event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            const previewImage = document.getElementById('previewImage');
            previewImage.src = e.target.result;
            previewImage.style.display = 'block';  // Exibe a imagem
        };
        reader.readAsDataURL(file);

        // Exibe o nome do arquivo
        document.getElementById('fileName').textContent = file.name;
    }
});

// Envia a imagem para o backend
async function uploadImage() {
    const fileInput = document.getElementById('imageInput');
    const file = fileInput.files[0];

    if (file) {
        const formData = new FormData();
        formData.append('image', file);

        try {
            const response = await fetch('http://localhost:5000/upload', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();
            if (result.error) {
                alert(result.error);
            } else {
                // Exibe a descrição
                document.getElementById('descriptionText').innerText = result.description;

                // Configura o player de áudio
                const audioPlayer = document.getElementById('audioPlayer');
                audioPlayer.src = `data:audio/mp3;base64,${result.audio}`;
                audioPlayer.style.display = 'block';  // Exibe o player de áudio

                // Mostra o botão "Processar Outra Imagem"
                document.getElementById('processAnotherImage').style.display = 'block';
            }
        } catch (error) {
            alert("Erro ao enviar a imagem. Verifique o console para mais detalhes.");
            console.error(error);
        }
    } else {
        alert("Nenhuma imagem selecionada.");
    }
}

// Reseta o processo para permitir o upload de uma nova imagem
function resetProcess() {
    document.getElementById('imageInput').value = '';  // Limpa o input de arquivo
    document.getElementById('fileName').textContent = '';  // Limpa o nome do arquivo
    document.getElementById('previewImage').src = '#';  // Limpa a pré-visualização da imagem
    document.getElementById('previewImage').style.display = 'none';  // Oculta a imagem
    document.getElementById('descriptionText').innerText = '';  // Limpa a descrição
    document.getElementById('audioPlayer').src = '';  // Limpa o áudio
    document.getElementById('processAnotherImage').style.display = 'none';  // Oculta o botão
}

// Configura o botão de upload para enviar a imagem
const uploadButton = document.querySelector('.upload-button');
if (uploadButton) {
    uploadButton.addEventListener('click', function () {
        document.getElementById('imageInput').click();
    });
} else {
    console.error("Botão de upload não encontrado.");
}

// Envia a imagem automaticamente após a seleção
document.getElementById('imageInput').addEventListener('change', uploadImage);