const express = require('express');

const jwt = require('jsonwebtoken');
const dotenv = require('dotenv');
const cors = require('cors');
const bcrypt = require('bcrypt');
const saltRounds = 10;

dotenv.config();

const app = express();
const port = 3000;


app.use(express.json());
app.use(cors())



function generateAccessToken(username) {
    return jwt.sign(username, process.env.TOKEN_SECRET, { expiresIn: '1800s' });
}

function authenticateToken(req, res, next) {
    const authHeader = req.headers['authorization']
    const token = authHeader && authHeader.split(' ')[1]
  
    if (token == null) return res.sendStatus(401)
  
    jwt.verify(token, process.env.TOKEN_SECRET, (err, user) => {
      console.log(err)
  
      if (err) return res.sendStatus(403)
  
      req.user = user
  
      next()
    })
}


app.post('/api/register', (req, res) => {

    // content-type is application/json
    // body should look like
    /*  
    /   {
    /       username: "",
    /       password: ""
    /   }
    */
    const password = req.body.password;
    bcrypt.hash(password, saltRounds, function(err, hash){
        console.log("password " + password);
        console.log("hash " + hash);
    });
    // store hash in db
    // return 200 if completed
    res.status(200).send();

});

app.post('/api/login', (req, res) => {

    /*
    * TODO: Access DB to verify username + passcode
    */
    
    // 1. Obtain hash from db
    // 2. Compare to password
    // 3. return JWT on success

    console.log(req.body.username)
    console.log(req.body.password)
    const token = generateAccessToken( {username: req.body.username} );
    res.json(token);

});


app.get('/api/transaction', authenticateToken, (req, res) => {
    res.statusCode(200).send('Hello World!')
});

app.post('/api/transaction', authenticateToken, (req, res) => {
    res.send('Hello World!')
});

app.get('/api/charge', authenticateToken, (req, res) => {
    res.send('Hello World!')
});

app.post('/api/charge', authenticateToken, (req, res) => {
    res.send('Hello World!')
});

app.get('/api/payment', authenticateToken, (req, res) => {
    res.send('Hello World!')
});

app.post('/api/payment', authenticateToken, (req, res) => {
    res.send('Hello World!')
});

app.get('/api/user', authenticateToken, (req, res) => {
    res.send('Hello World!')
});

app.post('/api/user', authenticateToken, (req, res) => {
    res.send('Hello World!')
});



app.listen(port, () => {
    console.log(`Example app listening on port ${port}`)
});