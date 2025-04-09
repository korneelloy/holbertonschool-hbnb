document.addEventListener('DOMContentLoaded', () => {
    // check current url on each loading
    const path = window.location.pathname;
    // check authentification on each loading
    checkAuthentication();

    // route handling: entry of website with all places info
    if (path.endsWith('/index.html') || path.endsWith('/')) {
      fetchPlaces();
    }

    // route handling: handling detailed info of one specific place
    if (path.endsWith('/place.html')) {
      const data = JSON.parse(localStorage.getItem('selectedPlace'));
      if (data) {
        displayPlaceDetails(data);
      }
    }

    // route handling: handling review of a specific place
    if (path.endsWith('/add_review.html')) {
      const data = JSON.parse(localStorage.getItem('thisPlace'));
      if (data) {
        goToAddReview(data);
      }
    }

    // adding event listener to login form
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
      loginForm.addEventListener('submit', verifLogin);
    }

    // adding event listener to price filter
    const price_filter = document.getElementById('price-filter');
    if (price_filter) {
      price_filter.addEventListener('change', filter);
    }

    // adding event listener to button redirecting from specific place to adding a review for this specific place
    const add_review_linker = document.getElementById('add-review-linker');
    if (add_review_linker) {
      add_review_linker.addEventListener('click',  function(event) {
        event.preventDefault();
        placeId = add_review_linker.getAttribute('data-place-id');
        // store info locally before redirection
        localStorage.setItem('thisPlace', JSON.stringify(placeId));        
        window.location.href = 'add_review.html';
      });
    }

    // adding event listener to submission button review
    const submit_review = document.getElementById("submit-review");
    if (submit_review){
      submit_review.addEventListener('click', function(e){
        e.preventDefault();
        submitReview();
      })
    }
  });

// verify connection values entered by user are correct before loging in
function verifLogin(e){
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

// help function to decode token, and get the additional information (additional_claims) stored in the token
function decodeJWT(token) {
  const base64Payload = token.split('.')[1];
  const payload = atob(base64Payload);
  return JSON.parse(payload);
}

// verify passwors / email + store token and user info locally
async function loginUser(email, password) {
  const response = await fetch('http://localhost:5000/api/v1/auth/login', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email, password }),
      credentials: 'include'
  });
  if (response.ok) {
    const data = await response.json();
    document.cookie = `token=${data.access_token}; path=/`;
    
    const decoded = decodeJWT(data.access_token);
    localStorage.setItem('first_name', decoded.first_name);
    localStorage.setItem('last_name', decoded.last_name); 
    localStorage.setItem('email', decoded.email); 
    window.location.href = 'index.html';
  } else {
    alert('Login failed: ' + response.statusText);
  }
}

// clears token and other locally stored info from the user when he clicks on his name and confirms the pop up to log off
function logof() {
  if(confirm('Are you sure you want to log off? ')) {
    localStorage.clear();
    document.cookie = "token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC;";
    window.location.href = '/login.html';
  }
}

// handling info shown / not shown when user is logged / not logged
function checkAuthentication() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');
  const add_review = document.getElementById('add-review');
  const add_review_message = document.getElementById('add-review-message');
  const logged_in = document.getElementById('logged-in');


  if (!token) {
      loginLink.style.display = 'inline';
      if(add_review) {
        add_review.style.display = 'none';
        add_review_message.style.display = 'block'
      }
      if(logged_in) {
        logged_in.style.display = 'none';
      }
  } else {
      loginLink.style.display = 'none';
      if(add_review) {
        add_review.style.display = 'block';
        add_review_message.style.display = 'none'
      }
      if(logged_in) {
        const first_name = localStorage.getItem('first_name');
        const last_name = localStorage.getItem('last_name');
        if (first_name && last_name){
          const nameLog = document.createElement('a');
          nameLog.setAttribute('href', "#");
          nameLog.setAttribute('title', "You are logged in as " + first_name + ' ' + last_name + '\n' + 'Click on your name if you want to log off');
          const nameLogText = document.createTextNode(first_name + ' ' + last_name);
          nameLog.appendChild(nameLogText);
          logged_in.addEventListener('click', logof);
          logged_in.appendChild(nameLog);
        }
        logged_in.style.display = 'block';
      }
  }
}

// help function to retrieve cookie info
function getCookie(name) {
  const cookies = document.cookie;
  const cookiesArray = cookies.split(';');
  for (let element of cookiesArray) {
    element = element.split('=');
    if (element[0] === name)
    {
      return element[1];
    }
  }
  return null;
}

// function handling he display of the places on the main page (function called from fetchPlaces which handles the api call)
function displayPlaces(places) {
  const places_list = document.getElementById('places-list');
  if (places_list) {
    for (let place of places.places) {
      const place_card = document.createElement('div');
      place_card.className = "place-card";

      const title = document.createElement('h2');
      const titleText = document.createTextNode(place.title);
      title.appendChild(titleText);
      place_card.appendChild(title);

      const description = document.createElement('p');
      const descriptionText = document.createTextNode(place.description);
      description.appendChild(descriptionText);
      place_card.appendChild(description);

      const price = document.createElement('p');
      const priceText = document.createTextNode('Price : ' + place.price + ' euros');
      price.appendChild(priceText);
      price.setAttribute('data-price', place.price);
      place_card.appendChild(price);

      const details = document.createElement('a');
      const butt = document.createElement('button');
      butt.className = 'btn-link details-button';
      const buttText = document.createTextNode('View Details');
      butt.appendChild(buttText);
      details.appendChild(butt);
      details.addEventListener('click', function() {
        fetchPlaceDetails(place.id);
      });
      place_card.appendChild(details);

      places_list.append(place_card);
    }
  }
    
}

// function retrieving all places, and calling the function to display this info
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

// function to filter on price
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

// help function to retrieve the name of the host based on its id
async function getHost(owner_id) {
  const token = getCookie('token');
  const headers = token ? 
    { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` } : 
    { 'Content-Type': 'application/json' };

  const apiUrl = 'http://localhost:5000/api/v1/users/' + owner_id;
  const response = await fetch(apiUrl, {
    method: 'GET',
    headers: headers,
    credentials: 'include',
  });

  if (response.ok) {
    const data = await response.json();
    const name = `${data.first_name} ${data.last_name}` ;
    return name;
    ;
  } else {
    alert('Error in getting the owner data: ' + response.statusText);
    return '';
  }
}

// help function to retrieve the name of the amenity based on its id
async function getAmenity(amenity_id) {
  const token = getCookie('token');
  const headers = token ? 
    { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` } : 
    { 'Content-Type': 'application/json' };

  const apiUrl = 'http://localhost:5000/api/v1/amenities/' + amenity_id;
  const response = await fetch(apiUrl, {
    method: 'GET',
    headers: headers,
    credentials: 'include',
  });

  if (response.ok) {
    const data = await response.json();
    return data;
  } else {
    alert('Error in getting the amenities data: ' + response.statusText);
    return '';
  }
}

// help function to retrieve the list of reviews attached to a place
async function getReviews(placeId) {
  const token = getCookie('token');
  const headers = token ? 
    { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` } : 
    { 'Content-Type': 'application/json' };

  const apiUrl = 'http://localhost:5000/api/v1/reviews/places/' + placeId + '/reviews';
  const response = await fetch(apiUrl, {
    method: 'GET',
    headers: headers,
    credentials: 'include',
  });

  if (response.ok) {
    const data = await response.json();
    return data;
  } else {
    console.log('Error in getting the reviews data: ' + response.statusText);
    return [];
  }
}

// function handling the display of a specifi place (function called upon loading of route /.place.html) data / api call via fetchPlaceDetails)
function displayPlaceDetails(data) {
  const place_details = document.getElementById('place-details').children[1];
  if (place_details) {
    const title = document.createElement('p');
    const titleText = document.createTextNode('Title : ' + data.title);
    title.appendChild(titleText);
    place_details.appendChild(title);

    const host = document.createElement('p');
    const hostText = document.createTextNode('Host : ' + data.owner_id);
    host.appendChild(hostText);
    place_details.appendChild(host);

    const price = document.createElement('p');
    const priceText = document.createTextNode('Price : ' + data.price + ' euros');
    price.appendChild(priceText);
    place_details.appendChild(price);

    const description = document.createElement('p');
    const descriptionText = document.createTextNode('Description : ' + data.description);
    description.appendChild(descriptionText);
    place_details.appendChild(description);

    const amenities = document.createElement('p');

    if (data.amenities.length === 0) {
      let amenitiesText = document.createTextNode('No amenities were added to this place yet');
      amenities.appendChild(amenitiesText);

    } else {
      let amenitiesText = document.createTextNode('Amenities : ');
      amenities.appendChild(amenitiesText);

      const amenityList = document.createElement('ol');

      for (const amenity of data.amenities) {
        const listItem = document.createElement('li');
        const listItemText = document.createTextNode(amenity[0] + ' : ' + amenity[1]);
        listItem.appendChild(listItemText);
        amenityList.appendChild(listItem);
      }
      amenities.appendChild(amenityList);
    }
    place_details.appendChild(amenities);     


    const reviewId = document.getElementById('reviews');
    if (data.reviews.length === 0) {
      const reviews = document.createElement('p');
      let reviewText = document.createTextNode('No reviews were added to this place yet');
      reviews.appendChild(reviewText);
      reviews.className = 'message';
      reviewId.children[0].appendChild(reviews);

    } else {
      let i = 1;
      for (const rev of data.reviews) {
        const oneReview = document.createElement('div');
        oneReview.className = 'review-card';

        const oneReviewTitle = document.createElement('h4');
        oneReviewTitleText = document.createTextNode('Rating number ' + i);
        oneReviewTitle.appendChild(oneReviewTitleText);
        oneReview.appendChild(oneReviewTitle);

        const commentItem = document.createElement('p');
        const commentItemText = document.createTextNode('Comment : ' + rev[1]);
        commentItem.appendChild(commentItemText);
        oneReview.appendChild(commentItem);

        const userNameItem = document.createElement('p');
        const userNameText = document.createTextNode('User name : ' + rev[2] + ' ' + rev[3]);
        userNameItem.appendChild(userNameText);
        oneReview.appendChild(userNameItem);

        const ratingItem = document.createElement('p');
        const ratingItemText = document.createTextNode('Rating : ' + rev[0]);
        ratingItem.appendChild(ratingItemText);
        oneReview.appendChild(ratingItem);

        reviewId.appendChild(oneReview);

        i += 1;

      }
    }

    const add_review_link = document.getElementById('add-review-linker');
    if (add_review_link) {
      add_review_link.setAttribute('data-place-id',  data.id);
      add_review_link.setAttribute('data-place-description',  data.title);

    } else {
      console.error('Element with ID "add-review-linker" not found');
    }
  }
}

// help function to retriev user via user id
async function getUser(user_id) {
  const token = getCookie('token');
  const headers = token ? 
    { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` } : 
    { 'Content-Type': 'application/json' };
  
  const apiUrl = 'http://localhost:5000/api/v1/users/' + user_id;
  const response = await fetch(apiUrl, {
    method: 'GET',
    headers: headers,
    credentials: 'include',
  });

  if (response.ok) {
    const data = await response.json();
    return data;
  } else {
    alert('Error in getting the user data: ' + response.statusText);
    return [];
  }
}

// function handling api call to get details of a specific place
async function fetchPlaceDetails(placeId) {
  const token = getCookie('token');
  const headers = token ? 
    { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` } : 
    { 'Content-Type': 'application/json' };
  
  const apiUrl = 'http://localhost:5000/api/v1/places/' + placeId;
  const response = await fetch(apiUrl, {
    method: 'GET',
    headers: headers,
    credentials: 'include',
  });

  if (response.ok) {
    const data = await response.json();

    //transform owner_id to name
    const host = await getHost(data.owner_id);
    data.owner_id = host;

    //transform amenities id's to amenities list
    let amenitiesList = [];
    for (const amenityId of data.amenities) {
      const amenity = await getAmenity(amenityId);
      amenitiesList.push([amenity.name, amenity.description]);
    }
    data.amenities = amenitiesList;

    // get the reviews
    let reviews = [];

    try {
      reviews = await getReviews(placeId);
    } catch (error) {
      reviews = [];
    }
    let reviewsList = [];
    for (const review of reviews) {
      const user = await getUser(review.user_id);
      reviewsList.push([review.rating, review.comment, user.first_name, user.last_name]);
    }
    data.reviews = reviewsList;

    // store info locally before redirection
    localStorage.setItem('selectedPlace', JSON.stringify(data));
    window.location.href = '/place.html';
  } else {
    alert('Error in getting the place data: ' + response.statusText);
    return [];
  }
}

// help function to retriev usere via email
async function getUserIdByEmail(email) {
  const token = getCookie('token');
  const headers = token ? 
    { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` } : 
    { 'Content-Type': 'application/json' };
  
  const apiUrl = `http://localhost:5000/api/v1/users/mail/${encodeURIComponent(email)}`;
  const response = await fetch(apiUrl, {
    method: 'GET',
    headers: headers,
    credentials: 'include',
  });

  if (response.ok) {
    const data = await response.json();


    return (data);
  } else {
    alert('Error in getting the user data: ' + response.statusText);
    return [];
  }
}

// function preparing the form for adding a review / populate it with the info of the place and the connected user
async function goToAddReview(data) {
  if (data) {
    const place = JSON.parse(localStorage.getItem('selectedPlace'));
    const title_place = place['title'];
    console.log(title_place);

    let textTitle = "Add a Review ";

    if (title_place) {
      textTitle = textTitle + "for place '" + title_place + "'";
    }

    document.getElementById('add-review-title').innerHTML = textTitle;


    document.getElementById('placeId').setAttribute('value', data);

    const email = localStorage.getItem('email');
    const user = await getUserIdByEmail(email);
    document.getElementById('personId').setAttribute('value', user.id);
  }
}

// handling the submision of the review
async function submitReview(){
  let rating = Number(document.getElementById("rating").value);
  const comment = document.getElementById("review").value;
  const user_id = document.getElementById("personId").value;
  const place_id = document.getElementById("placeId").value;
  const token = getCookie('token');
  const headers = token ? 
    { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` } : 
    { 'Content-Type': 'application/json' };
  const response = await fetch('http://localhost:5000/api/v1/reviews/', {
    method: 'POST',
    headers: headers,
    body: JSON.stringify({ rating, comment, user_id, place_id }),
    credentials: 'include'
  });
  if (response.ok) {
    const data = await response.json();
    alert('Review submitted successfully!');
  } else {
    alert('Failed to submit review');
  }
  document.getElementById("review-form").reset();
}
    