/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
      loginForm.addEventListener('submit',  verif);
    }
  });

function verif(e){
  e.preventDefault();
  const mail = document.getElementById('email').value;
  const pw = document.getElementById('password').value;
  const regexMail = /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/;
  const regexPw = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/;

  if (regexMail.test(mail) && regexPw.test(pw)) {
    loginUser(mail, pw);
  }
  else {
    alert ("Please enter a valid email and password");
  }
}

async function loginUser(email, password) {
  const response = await fetch('http://localhost:5000/api/v1/auth/login', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email, password }),
      credentials: 'include'  // Ensure cookies & authentication work across origins
  });
  if (response.ok) {
    const data = await response.json();
    document.cookie = `token=${data.access_token}; path=/`;
    window.location.href = 'index.html';
  } else {
    alert('Login failed: ' + response.statusText);
  }
}