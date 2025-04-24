describe('check UI elements', ()=>{

    it('checking radio buttons', ()=>{
        cy.visit('https://itera-qa.azurewebsites.net/home/automation')
        cy.get('input#male').should('be.visible')
        cy.get('input#female').should('be.visible')

        //selecting radio buttons
        cy.get('input#male').check().should('be.checked')
        cy.get('input#female').check().should('be.checked')
    })

    it('checking check boxes', ()=>{
        cy.get('input#monday').should('be.visible')
        //selecting single checkbox
        cy.get('input#monday').check().should('be.checked')
        //unselect single checkbox
        cy.get('input#monday').uncheck().should('not.be.checked')
        //select all checkboxes
        cy.get('input.form-check-input[type="checkbox"]').check().should('be.checked')
        // select first checkbox among multiple checkboxes
        cy.get('input.form-check-input[type="checkbox"]').first().check().should('be.checked')
        // select last checkbox among multiple checkboxes
        cy.get('input.form-check-input[type="checkbox"]').last().check().should('be.checked')
    })
})