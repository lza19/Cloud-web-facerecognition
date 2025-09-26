document.addEventListener('DOMContentLoaded', () => {
    const params = new URLSearchParams(window.location.search);
    const showName= document.getElementById("showName");
    const saveinput= document.getElementById("saveinput");
    const loadingOverlay = document.getElementById('loadingOverlay');
    const username = params.get("name");
    console.log(saveinput);
    console.log(username);

    const video = document.getElementById('videoRegister');
    const canvas = document.getElementById('canvas');
    const photo = document.getElementById('photo');
    const captureBtn = document.getElementById('cap');
    showName.textContent = "ชื่อ : " + username;

    let imageData = null;

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

        
        imageData = canvas.toDataURL('image/png');
        
        // แสดงภาพใน <img>
        photo.src = imageData;
        photo.style.display = 'block';
        // เก็บตัวแปร
        console.log("Captured Image:", imageData);
        
    });

    function base64ToBlob(base64) {
        const byteString = atob(base64.split(',')[1]);
        const arrayBuffer = new ArrayBuffer(byteString.length);
        const intArray = new Uint8Array(arrayBuffer);
        for (let i = 0; i < byteString.length; i++) {
            intArray[i] = byteString.charCodeAt(i);
        }
        return new Blob([intArray], { type: 'image/png' });
    }

    saveinput.addEventListener('click',()=>{
        if (!username) { 
            return alert("ใส่ชื่อ");
        }
        if (!imageData){
            return alert('ถ่ายรูป')
        }
        //loadingOverlay.style.display = 'flex';
        const imageBlob = base64ToBlob(imageData);

        console.log(imageBlob)
        const formData = new FormData();
        formData.append("name", username);
        formData.append("image", imageBlob, "photo.png");

        fetch("http://ec2-54-179-181-172.ap-southeast-1.compute.amazonaws.com:8000/upload", {
            method: "POST",
            body: formData
        })
        
        .then(res => {
            if(!res.ok){
                alert("ส่งข้อมูลสำเร็จ");
            }
            if(res.ok){
                alert("ส่งข้อมูลสำเร็จ");
            }
            console.log("Response Object:", res);
            return res.json();
        })

        .then(data => console.log("Server response:", data))
        .catch(error => {
            alert("ไม่สามารถตรวจจับใบหนาได้");
            console.log("Response Object:", error);
        })
        //.finally(() => {
            // ปิด loading overlay ไม่ว่าจะสำเร็จหรือล้มเหลว
            //loadingOverlay.style.display = 'none';
        //});

    })

});