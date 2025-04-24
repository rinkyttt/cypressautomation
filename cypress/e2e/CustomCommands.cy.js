//click on links using label
//over writing existing cotains() command
//re-usuable custom command 

describe('custom commands',()=>{

    it('handling links',()=>{
        cy.visit('https://demo.nopcommerce.com/');
        //direct - without using custom command
        cy.get('div[class="tem-grid"] div:nth-child(2) div:nth-child(1) div:nth-child(2) h2:nth-child(1) a:nth-child(1)').click();
        cy.get('div[class="product-name"] h1').should('have.text','Apple MacBook Pro 13-inch');

        //using custom command
        cy.clickLink('Apple MacBook Pro 13-inch');
        cy.get('div[class="product-name"] h1').should('have.text','Apple MacBook Pro 13-inch');
    })

    it('overwriting existing command', ()=>{
        cy.visit('https://demo.nopcommerce.com/');
        cy.clickLink('APPLE MacBook Pro 13-inch');
        cy.get('div[class="product-name"] h1').should('have.text','Apple MacBook Pro 13-inch');
    })

    it('Login command',()=>{
        cy.visit('https://demo.nopcommerce.com/');
        //login
        //search
        cy.clickLink('Log in')
        cy.loginapp('testing@gmail.com','test123');
        cy.get('.ico-account').should('have.text','My Account');

    })
})