CREATE TABLE IF NOT EXISTS `users` (
    id CHAR(36) PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255),
    password VARCHAR(255),
    is_admin BOOLEAN DEFAULT FALSE
);
 
CREATE TABLE IF NOT EXISTS `places` (
    id CHAR(36) PRIMARY KEY,
    title VARCHAR(255),
    description TEXT,
    price DECIMAL(10,2),
    latitude FLOAT,
    longitude FLOAT,
    owner_id CHAR(36), FOREIGN KEY (owner_id) REFERENCES `users`(id)
);
 
CREATE TABLE IF NOT EXISTS `reviews` (
    id CHAR(36) PRIMARY KEY,
    text TEXT,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    user_id CHAR(36),
    place_id CHAR(36),
    FOREIGN KEY (user_id) REFERENCES `users`(id),
    FOREIGN KEY (place_id) REFERENCES `places`(id),
    UNIQUE (user_id, place_id)
);


CREATE TABLE IF NOT EXISTS `amenities` (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) UNIQUE
);


CREATE TABLE IF NOT EXISTS `amenity_place` (
    place_id CHAR(36),
    amenity_id CHAR(36),
    FOREIGN KEY (place_id) REFERENCES `places`(id),
    FOREIGN KEY (amenity_id) REFERENCES `amenities`(id)    
);


INSERT INTO `users` (id, email, first_name, last_name, password, is_admin)
VALUES ('36c9050e-ddd3-4c3b-9731-9f487208bbc1', 'admin@hbnb.io', 'Admin', 'HBnB', 'Admin1234', TRUE);

INSERT INTO `amenities` (id, name)
VALUES  
    (lower(hex(randomblob(16))), 'Wifi'),
    (lower(hex(randomblob(16))), 'Swimming Pool'),
    (lower(hex(randomblob(16))), 'Air Conditioning');
