document.addEventListener('DOMContentLoaded', () => {
    const videoVerify = document.getElementById('videoVerify');
    const captureBtn = document.getElementById('captureVerifyBtn1');
    const canvas = document.getElementById('canvas');
    const photo = document.getElementById('photo');
    const captureVerifyBtn2 = document.getElementById('captureVerifyBtn2');
    const result = document.getElementById('result');
    let imageData = null;

    console.log(result)
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

        function base64ToBlob(base64) {
        const byteString = atob(base64.split(',')[1]);
        const arrayBuffer = new ArrayBuffer(byteString.length);
        const intArray = new Uint8Array(arrayBuffer);
        for (let i = 0; i < byteString.length; i++) {
            intArray[i] = byteString.charCodeAt(i);
        }
        return new Blob([intArray], { type: 'image/png' });
    }

    captureVerifyBtn2.addEventListener('click',()=>{
        if (!imageData){
            return alert('4k')
        }
        const imageBlob = base64ToBlob(imageData);

        console.log(imageBlob)
        const formData = new FormData();
        formData.append("image", imageBlob, "photo.png");

        fetch("http://ec2-52-74-118-144.ap-southeast-1.compute.amazonaws.com:8000/vertify", {
            method: "POST",
            body: formData
        })
        .then(res => {
            if(!res.ok){
                alert("ส่งข้อมูลไม่สำเร็จ");
            }
            //if(res.ok){
                //alert("ส่งข้อมูลสำเร็จ");
            //}
            console.log("Response Object:", res);
            return res.json();
        })
        .then(data => {
            console.log("Server response:", data.id)
            result.textContent = `ชื่อลำดับ 1 ${data.id} Cosine ${data.score}`;
        }
        )
        .catch(error => {
            alert("ไม่สามารถเชื่ม่อมต่อเซิร์ฟเวอร์ได้");
            console.log("Response Object:", error);
        })

    })
});
