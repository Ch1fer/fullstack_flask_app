async function fetchData(){

    const userId = document.getElementById("userId").value;

    try{
        const responce = await fetch(`http://localhost:4000/api/flask/users/${userId}`)

        if(!responce.ok){
            throw new Error("Could not fetch resource");
        }

        const data = await responce.json();
        const userName = data.user.name
        const userEmail = data.user.email
        document.getElementById("userName").innerText = userName;
        document.getElementById("userEmail").innerText = userEmail;
    }
    catch(error){
        console.error(error)
    }
}

async function getAllUsers(){
    try{
        const responce = await fetch(`http://localhost:4000/api/flask/users`)

        if(!responce.ok){
            throw new Error("Could not fetch resource")
        }

        const users = await responce.json();
        const usersList = document.getElementById("usersList");

        usersList.innerHTML = "";

        users.forEach(user => {
            const userItem = document.createElement("div");
            userItem.classList.add("user-container");
            userItem.innerHTML = `
                <strong>${user.name}</strong> ${user.email}
                <button class="edit-btn" onclick="openEditQR(${user.id})">Check QR</button>
            `;
            usersList.appendChild(userItem);
        });
    }
    catch(error){
        console.error(error)
    }
}

async function addUser(event){
    event.preventDefault();

    const nameInput = document.getElementById("newUserName");
    const emailInput = document.getElementById("newUserEmail");

    const name = nameInput.value;
    const email = emailInput.value;

    try{
        const response = await fetch(`http://localhost:4000/api/flask/users`,{
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ name, email })
        });

        if (!response.ok){
            throw new Error("Failed to add user");
        }

        const result = await response.json();
        getAllUsers()
        nameInput.value = "";
        emailInput.value = "";
        alert("User added successfuly!");

        

    } catch (error) {
        console.error(error);
        alert("Error adding user");
    }
}

function openEditQR(qrcodeId) {
    // Ту можна додати логіку для переходу на сторінку редагування.
    // Наприклад, це може бути перехід на сторінку редагування за ID користувача:
    window.location.href = `/frontend/checkQRcode.html?id=${qrcodeId}`;
}

function openAddQR(){
    window.location.href = `/frontend/addQRcode.html`;
}

function openListQR(){
    window.location.href = `/frontend/index.html`;
}



async function getAllQrcodes(){
    try{
        const responce = await fetch(`http://localhost:4000/api/flask/qrcodes`)

        if(!responce.ok){
            throw new Error("Could not fetch resource")
        }

        const qrcodes = await responce.json();
        const qrcodesList = document.getElementById("qrcodesList");

        qrcodesList.innerHTML = "";

        qrcodes.forEach(qrcode => {
            const qrcodeItem = document.createElement("div");
            qrcodeItem.classList.add("qrcode-container");
            qrcodeItem.innerHTML = `
                <strong>${qrcode.author}</strong> ${qrcode.qr_name}
                <button class="edit-btn" onclick="openEditQR(${qrcode.id})">Check QR</button>
            `;
            qrcodesList.appendChild(qrcodeItem);
        });
    }
    catch(error){
        console.error(error)
    }
}

async function addQRcode(event){
    event.preventDefault();

    const authorInput = document.getElementById("newQRAuthor");
    const qrNameInput = document.getElementById("newQRName");
    const textInput = document.getElementById("newQRText");

    const author = authorInput.value;
    const qr_name = qrNameInput.value;
    const text = textInput.value;

    console.log(JSON.stringify({ author, qr_name, text }))
    try{
        const response = await fetch(`http://localhost:4000/api/flask/qrcodes`,{
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ author, qr_name, text })
        });

        if (!response.ok){
            throw new Error("Failed to add QR code");
        }

        const result = await response.json();
        authorInput.value = "";
        qrNameInput.value = "";
        textInput.value = "";

        alert("QR code added successfuly!");

    } catch (error) {
        console.error(error);
        alert("Error adding QR code");
    }
}

async function loadQRCodeData() {
    const urlParams = new URLSearchParams(window.location.search);
    const qrcodeId = urlParams.get("id");

    if (!qrcodeId) {
        console.error("QR Code ID not found in URL");
        return;
    }

    try {
        const response = await fetch(`http://localhost:4000/api/flask/qrcodes/${qrcodeId}`);
        if (!response.ok) {
            throw new Error("Failed to fetch QR code details");
        }

        const rawQRData = await response.json();
        const qrData = rawQRData.qrcode
        console.log(qrData)

        // Заповнюємо форму отриманими даними
        document.getElementById("qrAuthor").value = qrData.author;
        document.getElementById("qrName").value = qrData.qr_name;
        document.getElementById("qrDate").value = qrData.date;
        document.getElementById("qrText").value = qrData.text;

    } catch (error) {
        console.error(error);
        alert("Не вдалося отримати дані QR-коду");
    }
}

async function editQRcode(event){
    event.preventDefault();

    const urlParams = new URLSearchParams(window.location.search);
    const qrcodeId = urlParams.get("id");

    if (!qrcodeId) {
        console.error("QR Code ID not found in URL");
        return;
    }

    const authorInput = document.getElementById("qrAuthor");
    const qrNameInput = document.getElementById("qrName");
    const textInput = document.getElementById("qrText");
    const dateInput = document.getElementById("qrDate");

    const author = authorInput.value;
    const qr_name = qrNameInput.value;
    const text = textInput.value;
    const date = dateInput.value;

    console.log(JSON.stringify({author, date, qr_name, text }))
    try{
        const response = await fetch(`http://localhost:4000/api/flask/qrcodes/${qrcodeId}`,{
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ author, date, qr_name, text })
        });

        if (!response.ok){
            throw new Error("Failed to edit QR code");
        }
        const result = await response.json();
        openListQR()

    } catch (error) {
        console.error(error);
        alert("Error adding QR code");
    }

}

async function deleteQRcode(){
    const urlParams = new URLSearchParams(window.location.search);
    const qrcodeId = urlParams.get("id");

    if (!qrcodeId) {
        console.error("QR Code ID not found in URL");
        return;
    }

    try{
        const response = await fetch(`http://localhost:4000/api/flask/qrcodes/${qrcodeId}`,{
            method: "DELETE",
            headers: {
                "Content-Type": "application/json"
            },
        });
        if (!response.ok) {
            throw new Error("Failed to delete QR code");
        }
        openListQR();
    }
    catch(error) {
        console.error(error);
        alert("Error adding QR code");
    }       

}

document.addEventListener("DOMContentLoaded", function () {
    if (document.getElementById("QRForm")) {
        loadQRCodeData();

        // Додаємо обробник події для кнопки видалення
        const deleteButton = document.getElementById("deleteQRButton");
        if (deleteButton) {
            deleteButton.addEventListener("click", function () {
                if (confirm("Are you sure you want to delete this QR code?")) {
                    deleteQRcode();
                }
            });
        }

        // Обробник для кнопки закриття
        const closeButton = document.getElementById("closeQRButton");
        if (closeButton) {
            closeButton.addEventListener("click", function () {
                openListQR();
            });
        }

    } else if (document.getElementById("qrcodesList")) {
        getAllQrcodes();
    }
});