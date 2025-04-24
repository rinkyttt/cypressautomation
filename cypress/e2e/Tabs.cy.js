describe('Handle tabs',()=>{
    it('Approach1', ()=>{
        cy.visit('https://the-internet.herokuapp.com/windows');
        //remove the target, so wont open the new tab.
        cy.get('.example >a').invoke('removeAttr','target').click()
        cy.url().should('include','https://the-internet.herokuapp.com/windows/new')

        //operations
        cy.go('back'); //back to parent tab

    })

    it('Approach2',()=>{
        cy.visit('https://the-internet.herokuapp.com/windows');
        //save the new window to url. 
        cy.get('.example> a').then((e) =>{
            url = e.prop('href');
            cy.visit(url);
        })

        cy.url().should('include','https://the-internet.herokuapp.com/windows/new')
    })
})