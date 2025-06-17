function startListening() {
    const recognition = new webkitSpeechRecognition();
    recognition.lang = 'en-US';
    recognition.start();

    recognition.onresult = function(event) {
        const message = event.results[0][0].transcript;
        document.getElementById('question').innerText = "You: " + message;

        fetch('/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({message})
        })
        .then(res => res.json())
        .then(data => {
            document.getElementById('response').innerText = "ChatGPT: " + data.text;
            const audio = document.getElementById('audio');
            audio.src = data.audio_url;
            audio.style.display = 'block';

            const downloadLink = document.getElementById('downloadLink');
            downloadLink.href = data.audio_url;
            downloadLink.style.display = 'inline';
        });
    };

    recognition.onerror = function(event) {
        alert('Error recognizing speech. Try again.');
    };
}
