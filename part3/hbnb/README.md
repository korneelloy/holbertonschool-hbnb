HBnb
By Korneel LOY and Antonin LEBRE 
This HBnB project mirrors the “AirBnB” site. The objective is to permit for a user to create a 
user account, a place advertisement, search for a place and review/rate it.

```mermaid
---
title: HBNB
---
erDiagram
    USER ||--o{ PLACE : owns
    USER {
        string first_name
        string last_name
        string email
        string password
        boolean is_admin
    }
    PLACE o{--|| AMENITY_PLACE : has
    PLACE {
        string title
        string description
        float price
        float latitude
        float longitude
        string owner_id
    }
    AMENITY_PLACE{
        string place_id
        string amenity_id
    }

    AMENITY_PLACE ||--o{ AMENITY : has
    AMENITY {
        string name
        string description
    }
    USER ||--o{ REVIEW : writes
    REVIEW {
        integer rating
        string comment
        string place_id
        string user_id
    }
    PLACE ||--o{ REVIEW : evaluates
