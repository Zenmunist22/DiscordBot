import mysql.connector as con
import user
import datetime
#CREATE TABLE payments (id INT PRIMARY KEY AUTO_INCREMENT,
#transaction_id INT NOT NULL,
#user_id_paid_by INT NOT NULL,
#method VARCHAR(45) NOT NULL,
#amount DECIMAL(2) NOT NULL,
#date DATE NOT NULL,
#created_by INT NOT NULL,
#created_at DATE NOT NULL,
#FOREIGN KEY (transaction_id) REFERENCES transactions(id),
#FOREIGN KEY (user_id_paid_by) REFERENCES users(id),
#FOREIGN KEY (created_by) REFERENCES users(id)
#);
def splitTransaction(amount: int):
    return amount/5