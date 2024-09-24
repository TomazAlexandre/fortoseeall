document.getElementById('uploadForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    let formData = new FormData();
    let imageFile = document.getElementById('imageInput').files[0];
    formData.append("image", imageFile);

    // Substitua pela URL correta do backend no Heroku
    const herokuBackendUrl = 'https://fortoseeall-a6f0c908bc1e.herokuapp.com/upload';

    const response = await fetch(herokuBackendUrl, {
        method: 'POST',
        body: formData
    });

    const result = await response.json();
    const responseText = result.description;

    // Exibir a descrição no frontend
    document.getElementById('response').innerText = responseText;
    document.getElementById('result').style.display = 'block';

    // Mostrar o botão para gerar o áudio
    const generateAudioBtn = document.getElementById('generateAudioBtn');
    generateAudioBtn.style.display = 'inline';
    generateAudioBtn.onclick = async function () {
        // Enviar a descrição ao backend para gerar o áudio
        const audioResponse = await fetch('https://fortoseeall-a6f0c908bc1e.herokuapp.com/generate-audio', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: responseText })
        });

        // Criar URL para o áudio gerado e tocar no player
        const audioBlob = await audioResponse.blob();
        const audioUrl = URL.createObjectURL(audioBlob);
        const audioPlayer = document.getElementById('audioPlayer');
        audioPlayer.src = audioUrl;
        audioPlayer.style.display = 'block';
    };
});
