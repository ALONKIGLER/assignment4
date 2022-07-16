
function myFunction() {
    let num =  document.getElementById("user_id").value
    fetch(`https://reqres.in/api/users/${num}`).then(
        response => response.json()
    ).then(
        responseOBJECT => UsersList(responseOBJECT.data)
    ).catch(
        err => console.log(err)
    );
}

function UsersList(users){
      const user = users
       const curr_main = document.querySelector("main");
         const section = document.createElement('section');
         section.innerHTML = ` <br>
         <img src="${user.avatar}" alt="Profile Picture"/>
           <br>
         <div>
            <span>${user.first_name} ${user.last_name}</span>
            <br>
             <a href="mailto:${user.email}">Send Email</a>
        </div>
        <br>
        `;
         curr_main.appendChild(section);
}
