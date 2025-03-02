const cameraBtn = document.getElementById('camera-btn');
const cameraElement = document.getElementById('camera');
const cameraIcon = document.querySelector('.camera-icon');
const videoUploadInput = document.getElementById('video-upload'); // Get the video upload input
let stream = null;

cameraBtn.addEventListener('click', async () => {
    if (stream) {
        // Stop the camera if it's already on
        const tracks = stream.getTracks();
        tracks.forEach(track => track.stop());
        cameraElement.srcObject = null;
        stream = null;
        cameraBtn.textContent = "Turn Camera On";
        cameraIcon.style.display = "block";
    } else {
        // Start the camera
        try {
            stream = await navigator.mediaDevices.getUserMedia({ video: true });
            cameraElement.srcObject = stream;
            cameraBtn.textContent = "Turn Camera Off";
            cameraIcon.style.display = "none";
        } catch (error) {
            console.error('Error accessing camera: ', error);
            alert('Unable to access the camera.');
        }
    }
});

// Function to trigger the file input when the Upload Video button is clicked
function triggerFileInput() {
    videoUploadInput.click();
}

// Function to handle the video file when it's selected
function handleVideoUpload(event) {
    const file = event.target.files[0];
    if (file) {
        const videoURL = URL.createObjectURL(file);
        cameraElement.src = videoURL;  // Set the selected video to the video element
        cameraElement.play();  // Play the video automatically
        cameraBtn.textContent = "Turn Camera Off";  // Change button text
        cameraIcon.style.display = "none";  // Hide the camera icon
    }
}

function convertText() {
    // Get the selected languages
    const fromLanguage = document.getElementById("fromLanguage").value;
    const toLanguage = document.getElementById("toLanguage").value;

    // You can replace this with your actual translation logic
    const translatedText = `Translated ${fromLanguage} to ${toLanguage}: Some translated text goes here.`;

    // Update the output box with the translated text
    document.getElementById("output-box").innerText = translatedText;
}

