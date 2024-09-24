document.getElementById('uploadForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    let formData = new FormData();
    let imageFile = document.getElementById('imageInput').files[0];
    formData.append("image", imageFile);

    const response = await fetch('/upload', {
        method: 'POST',
        body: formData
    });

    const result = await response.json();
    const responseText = result.description;

    // Exibir a resposta no frontend
    document.getElementById('response').innerText = responseText;
    document.getElementById('result').style.display = 'block';

    // Adicionar funcionalidade para converter o texto em áudio
    document.getElementById('playAudio').addEventListener('click', function () {
        const speech = new SpeechSynthesisUtterance(responseText);
        speech.lang = 'pt-BR'; // Defina o idioma conforme necessário
        window.speechSynthesis.speak(speech);
    });
});