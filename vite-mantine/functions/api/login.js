
import * as jwt from "jsonwebtoken";
function generateAccessToken(username) {
    return jwt.sign(username, process.env.TOKEN_SECRET, { expiresIn: '1800s' });
}
export async function onRequest(context) {
      /*
    * TODO: Access DB to verify username + passcode
    */
    
    // 1. Obtain hash from db
    // 2. Compare to password
    // 3. return JWT on success

    console.log(context.Response.body.json())
    console.log(req.body.password)
    const token = generateAccessToken( {username: req.body.username} );
    const myOptions = { status: 200, statusText: "SuperSmashingGreat!" };
    return (new Response(token, myOptions))
}