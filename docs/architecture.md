# Architecture Details
Purpose: Outline visually and through text how the application can be interacted with as well as its functionality.

## SQL Database ERD
The following is an ERD generated through mermaid.

```mermaid
erDiagram

    user {
        int id
        VARCHAR(255) email
        VARCHAR(255) phone_number
        Datetime create_time
    }
    payment {
        int id
        int transaction_id
        int user_id_paid_by
        varchar(45) method
        decimal(2) amount
        date date
        int created_by
        datetime created_at
    }
    transaction {
        int id
        int transaction_category_id
        decimal(2) amount
        varchar(255) source
        int split_to_persons
        varchar(45) description
        date date
        int created_by
        datetime created_at
        int modified_by
        datetime modified_at
    }
    charge {
        int id
        int transaction_id
        int user_id_charge_affected
        decimal(2) amount
        int created_by 
        datetime created_at 
        int modified_by 
        datetime modified_at 
    }
    transaction_category {
        int id
        varchar(45) name
        datetime created_at
    }
    user || -- o{ transaction : has
    user || -- o{ charge : has
    user || -- o{ payment : has
    transaction }o -- || transaction_category : has


```
