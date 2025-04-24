
//go()
describe('mysuite',()=>{
    it('NavigationTest',()=>{
        cy.visit('https://demo.opencart.com')
        cy.title().should('eq','Your Store')
        cy.get('li:nth-child(7) a:nth-child(1)').click();
        cy.get('div["content"] h2').should('have.text','Cameras'); //camera
        //go back to homepage
        cy.go('back')  // or cy.go(-1)
        cy.title().should('eq','Your Store')

        // go to camera page agian 
        cy.go('forward')  // or cy.go(1)
        cy.get('div["content"] h2').should('have.text','Cameras');

        //reload page
        cy.reload();
    })
})