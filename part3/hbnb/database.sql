
CREATE TABLE IF NOT EXISTS `USER` (
    id CHAR(36) PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255),
    is_admin BOOLEAN DEFAULT FALSE
);
 
CREATE TABLE IF NOT EXISTS `PLACE` (
    id CHAR(36) PRIMARY KEY,
    title VARCHAR(255),
    description TEXT,
    price DECIMAL(10,2),
    latitude FLOAT,
    longitude FLOAT,
    owner_id CHAR(36), FOREIGN KEY (owner_id) REFERENCES `USER`(id)
);
 
CREATE TABLE IF NOT EXISTS `REVIEW` (
    id CHAR(36) PRIMARY KEY,
    text TEXT,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    user_id CHAR(36),
    FOREIGN KEY (user_id) REFERENCES `USER`(id),
    place_id CHAR(36),
    FOREIGN KEY (place_id) REFERENCES `PLACE`(id),
    UNIQUE (user_id, place_id)
);
"""
Add a unique constraint on the combination of user_id and place_id to ensure that a user can only leave one review per place.
"""

CREATE TABLE IF NOT EXISTS `AMENITY` (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) UNIQUE
);


CREATE TABLE IF NOT EXISTS `PLACE_AMENITY` (
    place_id CHAR(36),
    FOREIGN KEY (place_id) REFERENCES `PLACE`(id),
    amenity_id CHAR(36),
    FOREIGN KEY (amenity_id) REFERENCES `AMENITY`(id),
    
);


"""
Add a composite primary key for place_id and amenity_id.
Ensure that:

Foreign key constraints are correctly established for relationships.
UUIDs are properly generated for the id fields.
Insert Initial Data
"""

"""
Insert initial data into the database using SQL INSERT statements:

"""
-- Insert Admin User
INSERT INTO `USER` (id, email, first_name, last_name, password, is_admin)
VALUES ('36c9050e-ddd3-4c3b-9731-9f487208bbc1', 'admin@hbnb.io', 'Admin', 'HBnB', 'Admin1234', TRUE);

-- Insert Amenities
INSERT INTO `AMENITY` (id, name) VALUES 
(UUID(), 'Wifi'),
(UUID(), 'Swimming Pool'),
(UUID(), 'Air Conditioning');
