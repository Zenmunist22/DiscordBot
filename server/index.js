const express = require('express');
const jwt = require('jsonwebtoken');

const dotenv = require('dotenv');
dotenv.config();


const app = express();
const port = 3000;

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

app.post('api/login', (req, res) => {

    /*
    * TODO: Access DB to verify username + passcode
    */
    
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