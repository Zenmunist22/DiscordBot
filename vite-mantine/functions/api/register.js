import * as crypto from "crypto";
function generateAccessToken(username, TOKEN_SECRET) {
    return jwt.sign({name: username}, TOKEN_SECRET, { expiresIn: 1800 });
}
export async function onRequestPost(context) {
      /*
    * TODO: Access DB to verify username + passcode
    */
    // 1. Obtain hash from db
    // 2. Compare to password
    // 3. return JWT on success
    const json = await context.request.json()
    const jwt = await generateAccessToken(json.username, `${context.env.TOKEN_SECRET}`)
    const res = {
        jwt: jwt,
        name: json.username
    }
    return Response.json(res)
}