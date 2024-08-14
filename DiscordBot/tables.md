This file shows the sql queries to create the tables used in the database

The table names are a clear indication of what the table holds

The tables should be created in the given order due to foreign key dependencies

CREATE TABLE Users (
    id INT PRIMARY KEY AUTO_INCREMENT, 
    server_id BIGINT NOT NULL,  
    server_specific_id INT NOT NULL,
    name VARCHAR(255) NOT NULL, 
    phone_number VARCHAR(20) NOT NULL, 
    email VARCHAR(255) NOT NULL, 
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    UNIQUE(server_id, server_specific_id)
);

CREATE TABLE transaction_category 
    (id INT PRIMARY KEY AUTO_INCREMENT, 
    name VARCHAR(45) NOT NULL, 
    created_at DATE NOT NULL);

INSERT INTO transaction_category (name, created_at) values 
    ("Grocery", CURDATE()), 
    ("Rent",CURDATE()), 
    ("Furniture",CURDATE()), 
    ("Supply",CURDATE()), 
    ("Other", CURDATE());

CREATE TABLE Transactions 
    (id int PRIMARY KEY AUTO_INCREMENT, 
    server_id BIGINT,  
    server_specific_id INT,
    transaction_category_id INT NOT NULL, 
    user_id_paid_by INT NOT NULL, 
    amount DECIMAL(10,2) NOT NULL, 
    source VARCHAR(255) NOT NULL, 
    split_to_users INT NOT NULL, 
    description VARCHAR(255) NOT NULL, 
    date DATE NOT NULL, 
    updated_at TIMESTAMP DEFAULT CURRENT_DATE ON UPDATE CURRENT_DATE, 
    created_at TIMESTAMP DEFAULT CURRENT_DATE NOT NULL, 
    created_by INT NOT NULL, 
    updated_by INT, 
    FOREIGN KEY (user_id_paid_by) REFERENCES users(id) ,  
    FOREIGN KEY (created_by) REFERENCES users(id), 
    FOREIGN KEY (updated_by) REFERENCES users(id), 
    FOREIGN KEY (transaction_category_id) REFERENCES transaction_category(id),
    UNIQUE(server_id, server_specific_id));

CREATE TABLE charges   
    (id INT PRIMARY KEY AUTO_INCREMENT,
    server_id BIGINT,  
    transaction_id INT NOT NULL,
    user_id_charge_affected INT NOT NULL,
    amount DECIMAL(65, 2) NOT NULL,
    created_by INT NOT NULL,
    created_at DATE NOT NULL,
    modified_by INT,
    modified_at DATE,
    FOREIGN KEY (transaction_id) REFERENCES transactions(id),
    FOREIGN KEY (user_id_charge_affected) REFERENCES users(id),
    FOREIGN KEY (created_by) REFERENCES users(id),
    FOREIGN KEY (modified_by) REFERENCES users(id));

CREATE TABLE payments 
    (id INT PRIMARY KEY AUTO_INCREMENT,
    server_id BIGINT,  
    transaction_id INT,
    user_id_paid_by INT NOT NULL,
    user_id_paid_to INT NOT NULL,
    method VARCHAR(45) NOT NULL,
    amount DECIMAL(65, 2) NOT NULL,
    date DATE NOT NULL,
    created_by INT NOT NULL,
    created_at DATE NOT NULL,
    FOREIGN KEY (transaction_id) REFERENCES transactions(id),
    FOREIGN KEY (user_id_paid_by) REFERENCES users(id),
    FOREIGN KEY (created_by) REFERENCES users(id),
    FOREIGN KEY (user_id_paid_to) REFERENCES users(id)
    );