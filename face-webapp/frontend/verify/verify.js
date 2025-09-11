document.addEventListener('DOMContentLoaded', () => {
    const videoVerify = document.getElementById('videoVerify');
    const captureBtn = document.getElementById('captureVerifyBtn1');
    const canvas = document.getElementById('canvas');
    const photo = document.getElementById('photo');
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            videoVerify.srcObject = stream;
        })
        .catch(err => {
            console.error("ไม่สามารถเปิดกล้องได้:", err);
        });

    captureBtn.addEventListener('click', () => {
        const context = canvas.getContext('2d');
        context.drawImage(videoVerify, 0, 0, canvas.width, canvas.height);

        
        imageData = canvas.toDataURL('image/png');
        
        // แสดงภาพใน <img>
        photo.src = imageData;
        photo.style.display = 'block';

        // เก็บตัวแปร
        console.log("Captured Image:", imageData);
        
    });
});