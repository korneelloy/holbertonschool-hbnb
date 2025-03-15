CREATE TABLE IF NOT EXISTS `users` (
    id CHAR(36) PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    _first_name VARCHAR(255),
    _last_name VARCHAR(255),
    _email VARCHAR(255),
    _password VARCHAR(255),
    _is_admin BOOLEAN DEFAULT FALSE
);
 
CREATE TABLE IF NOT EXISTS `places` (
    id CHAR(36) PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    _title VARCHAR(255),
    description TEXT,
    _price DECIMAL(10,2),
    _latitude FLOAT,
    _longitude FLOAT,
    _owner_id CHAR(36), FOREIGN KEY (_owner_id) REFERENCES `users`(id)
);
 
CREATE TABLE IF NOT EXISTS `reviews` (
    id CHAR(36) PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    _rating INT CHECK (_rating BETWEEN 1 AND 5),
    _comment TEXT,
    _place_id CHAR(36),
    _user_id CHAR(36),
    FOREIGN KEY (_user_id) REFERENCES `users`(id),
    FOREIGN KEY (_place_id) REFERENCES `places`(id),
    UNIQUE (_user_id, _place_id)
);


CREATE TABLE IF NOT EXISTS `amenities` (
    id CHAR(36) PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    _name VARCHAR(255) UNIQUE,
    _description TEXT
);


CREATE TABLE IF NOT EXISTS `amenity_place` (
    place_id CHAR(36),
    amenity_id CHAR(36),
    FOREIGN KEY (place_id) REFERENCES `places`(id),
    FOREIGN KEY (amenity_id) REFERENCES `amenities`(id)    
);


INSERT INTO `users` (id, _email, _first_name, _last_name, _password, _is_admin)
VALUES ('36c9050e-ddd3-4c3b-9731-9f487208bbc1', 'admin@hbnb.io', 'Admin', 'HBnB', '$2b$12$HRaI5zBYJBdazSF8lNFRdecX.lDUmZ0wFSyIF/jMTq.uKHoo27xEq', TRUE);

INSERT INTO `amenities` (id, _name, _description)
VALUES  
    (lower(hex(randomblob(16))), 'Wifi', 'Yahoo there is WiFi'),
    (lower(hex(randomblob(16))), 'Swimming Pool', 'Swimming is good, drowning is blblbllbl'),
    (lower(hex(randomblob(16))), 'Air Conditioning', "It's fresh in here!");
