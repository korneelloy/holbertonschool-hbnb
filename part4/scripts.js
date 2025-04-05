document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
      loginForm.addEventListener('submit',  verif);
    }
    
    checkAuthentication();
    
    const price_filter = document.getElementById('price-filter');
    if (price_filter) {
      price_filter.addEventListener('change', filter);
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

function checkAuthentication() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');

  if (!token) {
      loginLink.style.display = 'block';
  } else {
      loginLink.style.display = 'none';
      // Fetch places data if the user is authenticated
      fetchPlaces(token);
  }
}

function getCookie(name) {
  const cookies = document.cookie;
  const cookiesArray = cookies.split(';');
  for (element of cookiesArray) {
    element = element.split('=');
    if (element[0] === name)
    {
      return element[1];
    }
  }
  return null;
}

async function fetchPlaces() {
  const token = getCookie('token');
  const headers = token ? 
    { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` } : 
    { 'Content-Type': 'application/json' };
    
  const response = await fetch('http://localhost:5000/api/v1/places/', {
    method: 'GET',
    headers: headers,
    credentials: 'include',
  });

  if (response.ok) {
    const data = await response.json();
    displayPlaces(data);
  } else {
    alert('Error in getting the place data: ' + response.statusText);
    return [];
  }
}


function displayPlaces(places) {
  const places_list = document.getElementById('places-list');
  if (places_list) {
    for (place of places.places) {
      const place_card = document.createElement('div');
      place_card.className = "place-card";

      const title = document.createElement('h2');
      const titleText = document.createTextNode(place.description);
      title.appendChild(titleText);
      place_card.appendChild(title);

      const price = document.createElement('p');
      const priceText = document.createTextNode('Prix : ' + place.price + ' euros');
      price.appendChild(priceText);
      price.setAttribute('data-price', place.price);
      place_card.appendChild(price);

      const details = document.createElement('a');
      const butt = document.createElement('button');
      const buttText = document.createTextNode('View Details');
      butt.appendChild(buttText);
      details.appendChild(butt);
      const url = 'http://localhost:8000/places/' + place.id;
      details.setAttribute('href', url);
      place_card.appendChild(details);

      places_list.append(place_card);
    }
  }
    
}

function filter() {
  let max_price = document.getElementById('price-filter').value;
  const all_places = document.getElementsByClassName('place-card');

  if (max_price === 'all') {
    for (const place of all_places) {
      place.style.display = 'block';
    }
  }
  else {
    max_price = Number(max_price);
    for (const place of all_places) {
      const child = place.children[1];
      const price = Number(child.getAttribute('data-price'));

      if(price <= max_price) {
        child.parentElement.style.display = 'block';
      } else {
        child.parentElement.style.display = 'none';
      }
    }
  }
}
