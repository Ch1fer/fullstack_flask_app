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
                <button class="edit-btn" onclick="editUser(${user.id})">Check QR</button>
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

function editUser(userId) {
    // Ту можна додати логіку для переходу на сторінку редагування.
    // Наприклад, це може бути перехід на сторінку редагування за ID користувача:
    window.location.href = `/frontend/checkUser.html?id=${userId}`;
}

document.addEventListener('DOMContentLoaded', getAllUsers);