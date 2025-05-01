describe('Authentication',()=>{
    // Sends the username and password encoded in Base64 with every request header:
    // makefile
    // Copy
    // Edit
    // Authorization: Basic dXNlcjpwYXNzd29yZA==
    // Base64 is not encryption, just encoding — anyone who intercepts the request can decode it.
    it('Basic Authentication',()=>{
        cy.request({
            method:'GET',
            url:'https://postman-echo.com/basic-auth',
            auth:{
                user:'postman',
                pass:'password'
            }
        })
        .then((response)=>{
            expect(response.status).to.eq(200)
            expect(response.body.authenticated).to.eq(true)
        })
    })

    // Uses hashing to avoid sending the password in plaintext.
    // Server sends a nonce (a random string).
    // Client hashes the username, password, nonce, and request data, then sends that hash in the Authorization header.
    it('Digest Authentication',()=>{
        cy.request({
            method:'GET',
            url:'https://postman-echo.com/basic-auth',
            auth:{
                username:'postman',
                password:'password',
                method:'digest'
            }
        })
        .then((response)=>{
            expect(response.status).to.eq(200)
            expect(response.body.authenticated).to.eq(true)
        })
    })
    
    const token = 'fdfadfadf'
    it('Bearer Token Auth',()=>{
        cy.request({
            method:'GET',
            url:'https://api.github.com/user/repos',
            header:{
                Authorization:'Bearer'+token
            }
        })
        .then((response)=>{
            expect(response.status).to.eq(200)
        })
    })

    it('API key auth',()=>{
        cy.request({
            method:'GET',
            url:'api.openweathermap.org/data/2...',
            qs:{
                appid:'irtwetket' //API key and value
            }
        })
        .then((response)=>{
            expect(response.status).to.eq(200);
        })
    })

})