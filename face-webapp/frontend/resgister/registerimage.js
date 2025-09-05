document.addEventListener('DOMContentLoaded', () => {
    const params = new URLSearchParams(window.location.search);
    const showName= document.getElementById("showName");
    const saveinput= document.getElementById("saveinput");

    const username = params.get("name");
    console.log(saveinput);
    console.log(username);

    const video = document.getElementById('videoRegister');
    const canvas = document.getElementById('canvas');
    const photo = document.getElementById('photo');
    const captureBtn = document.getElementById('cap');
    showName.textContent = "ชื่อ : " + username;

    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            video.srcObject = stream;
        })
        .catch(err => {
            console.error("ไม่สามารถเปิดกล้องได้:", err);
        });

    captureBtn.addEventListener('click', () => {
        const context = canvas.getContext('2d');
        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        // แปลงภาพเป็น base64
        const imageData = canvas.toDataURL('image/png');
        
        // แสดงภาพใน <img>
        photo.src = imageData;

        // เก็บตัวแปร
        console.log("Captured Image:", imageData);
        
    });

    saveinput.addEventListener('click',()=>{
        if (!username) { 
            return alert("sd");
        }
        if (!imageData){
            return alert('4k')
        }
    })

});