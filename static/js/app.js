document.getElementById('healthForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    const response = await fetch('/predict', {
        method: 'POST',
        body: formData
    });
    const result = await response.json();
    document.getElementById('result').innerText = result.prediction !== undefined
        ? 'Prediction: ' + result.prediction
        : 'Error: ' + result.error;
});
