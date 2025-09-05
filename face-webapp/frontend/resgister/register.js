document.addEventListener('DOMContentLoaded', () => {
    const nameInput = document.getElementById('nameInput');
    const savename = document.getElementById('savename');
    console.log(document.getElementById('savename'));

    savename.addEventListener('click', () => {
        const username = nameInput.value.trim();
        if (!username) { 
            return alert("sd");
        }
        window.location.href = "registerimage.html?name=" + encodeURIComponent(username);


    });

});