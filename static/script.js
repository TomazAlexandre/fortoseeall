document.getElementById('uploadForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    let formData = new FormData();
    let imageFile = document.getElementById('imageInput').files[0];
    formData.append("image", imageFile);

    // Substitua pela URL correta do backend no Heroku
    const herokuBackendUrl = 'https://fortoseeall-a6f0c908bc1e.herokuapp.com/upload';  // Substitua por sua URL

    try {
        const response = await fetch(herokuBackendUrl, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            alert(`Erro: ${errorData.error}`);
            return;
        }

        const result = await response.json();
        const responseText = result.description;

        // Exibir a resposta no frontend
        document.getElementById('response').innerText = responseText;
        document.getElementById('result').style.display = 'block';

        // Adicionar funcionalidade para converter o texto em áudio
        document.getElementById('playAudio').onclick = function () {
            const speech = new SpeechSynthesisUtterance(responseText);
            speech.lang = 'pt-BR'; // Define o idioma para Português do Brasil
            window.speechSynthesis.speak(speech);
        };
    } catch (error) {
        console.error('Erro ao enviar a imagem:', error);
        alert('Ocorreu um erro ao enviar a imagem. Tente novamente.');
    }
});
