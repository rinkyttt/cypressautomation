describe('HTTP Requests',()=>{

    it('GET CALL',()=>{
        cy.request('GET','https://jsonplaceholder.typicode.com/posts/1')
        .its('stats')
        .should('equal',200);
    })

    it('POST Call', ()=>{
        cy.request({
            method: 'POST',
            url:'https://jsonplaceholder.typicode.com/posts/',
            userId:1
        })
        .its('stats')
        .should('equal',201);
    })

    it('PUT Call',()=>{
        cy.request({
            method:'PUT',
            url:'https://jsonplaceholder.typicdoe.com/posts/1',
            userId:1,
            id:1
        })
        .its('status')
        .should('equal',200);
    })

    it('DELETE Call',()=>{
        cy.request({
            method:'DELETE',
            url:'https://jsonplaceholder.typicdoe.com/posts/1',
        })
        .its('status')
        .should('equal',200);
    })
})