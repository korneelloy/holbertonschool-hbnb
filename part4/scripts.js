document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
      loginForm.addEventListener('submit',  verif);
    }
    
    checkAuthentication();

    fetchPlaces();

    
    const price_filter = document.getElementById('price-filter');
    if (price_filter) {
      price_filter.addEventListener('change', filter);
    }

    const path = window.location.pathname;

    if (path.endsWith('/place.html')) {
      const data = JSON.parse(localStorage.getItem('selectedPlace'));
      if (data) {
        displayPlaceDetails(data);
      }
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
  const add_review = document.getElementById('add-review');
  const add_review_message = document.getElementById('add-review-message');


  if (!token) {
      loginLink.style.display = 'inline';
      if(add_review) {
        add_review.style.display = 'none';
        add_review_message.style.display = 'block'
      }
  } else {
      loginLink.style.display = 'none';
      if(add_review) {
        add_review.style.display = 'block';
        add_review_message.style.display = 'none'
      }
  }
}

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
    for (let place of places.places) {
      const place_card = document.createElement('div');
      place_card.className = "place-card";

      const title = document.createElement('h2');
      const titleText = document.createTextNode(place.description);
      title.appendChild(titleText);
      place_card.appendChild(title);

      const price = document.createElement('p');
      const priceText = document.createTextNode('Price : ' + place.price + ' euros');
      price.appendChild(priceText);
      price.setAttribute('data-price', place.price);
      place_card.appendChild(price);

      const details = document.createElement('a');
      const butt = document.createElement('button');
      butt.className = 'btn-link';
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

function displayPlaceDetails(data) {
  const place_details = document.getElementById('place-details').children[1];
  if (place_details) {
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

        const oneReviewTitle = document.createElement('h2');
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
  }
}


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
