
describe('handle dropdowns',()=>{

    it('dropdown with select tag', ()=>{
        cy.visit('https://zoho.com/commerce/free-demo.html')
        cy.get('#zcf_address_country').select('Italy').should('have.value','Italy')
    })

    it('dropdown without select tag (for example dropdown with input box', ()=>{
        cy.visit('dummyticket.com/dummy-ticket-for-visa-application/')
        // click the dropdown list to trigger dropdown
        cy.get('#select2-billing_country-container').click()
        // type in the value
        cy.get('.select2-search__field').type('Italy').type('{enter}')
        // check the value of dropdown, because it's not a input text box value, it's what showing on the dropdown list, so use have.text
        cy.get('#select2-billing_country-container').should('have.text','Italy')

    })

    it('Auto suggest dropdown', ()=> {
        cy.visit('https://www.wikipedia.org')
        cy.get('#searchInput').type('Delhi')
        //get all dropdown options
        cy.get('.suggestion-title').contains('Delhi University').click()
    })

    it('dynamic dropdown', ()=>{
        cy.visit('https://www.google.com')
        cy.get('input[name="q"]').type('cypress automation')
        cy,get('div.wM6W7d>span').each(($el,index,$list)=>{
            if($el.text()=='cypress automation tool'){
                cy.wrap($el).click()
            }
        })
        cy.get('input[name="q"]').should('have.value','cypress automation tool')
    })

})