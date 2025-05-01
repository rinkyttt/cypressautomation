describe('API Testing',()=>{
    let authToken = null;
    //get Token first
    before('creating access token',()=>{
        cy.request({
            method:'POST',
            url:'https://simple-books-api.glitch.me/api-methods/',
            headers:{'Content-Type':'application/json'},
            body:{
                clientName:'ABC',
                clientEmail:Math.random().toString(5).substring(2)+'@gmail.com'
            }
        }).then((response)=>{
            authToken=response.body.accessToken;
        })
    });
    // use Token to generate a new order
    before('creating new order',()=>{
        cy.request({
            method:'POST',
            url:'https://simple-books-api.glitch.me/api-methods/',
            headers:{
                'Content-Type':'application/json',
                'Authorization':'Bearer '+authToken
            },
            body:{
                bookId:1,
                customerName:'ABC'
            }
        }).then((response)=>{
            expect(response.status).to.eq(201);
            expect(response.body.create).to.eq(true);
        })
    })

    it('Fetching tech orders',()=>{
        cy.request(
            {
                method:'GET',
                url:'https://simple-books-api.glitch.me/orders/',
                headers:{
                    'Content-Type':'application/json',
                    'Authorization':'Bearer '+authToken
                },
                cookies:{
                    'cookieName':'mycookie'
                }
            }
        ).then((reponse)=>{
            expect(reponse.status).to.eq(200);
        })
    })
})