describe("Assertion demo", ()=>{

    it("Implicit assertion", ()=>{
        cy.visit('https://opensource-demo.orangehrmlive.com/web/index.php/auth/login')
        // url() -- get the url
        cy.url().should('include','orangehrmlive') 
        // capture url one time, and then can use multiple assertions
        .should('eq','https://opensource-demo.orangehrmlive.com/web/index.php/auth/login')
        .should('contain','orangehrm')

        // can also use and for multiple assertions
        cy.url().should('include','orangehrmlive') 
        .and('eq','https://opensource-demo.orangehrmlive.com/web/index.php/auth/login')
        .and('contain','orangehrm')
        // negative assertion
        .and('not.contain','greenhrm')

        cy.title().should('include','Orange')
        .and('eq','OrangeHRM')
        .and('contain','HRM')

        cy.get('.orangehrm-login-branding > img').should('be.visible')
        .and('exist') //check logo exists 

        // capture all links on the page
        cy.xpath('//a').should('have.length','5') //number of links

        //value check 
        cy.get('input[placeholder="Username"]').type('Admin')
        cy.get('input[placeholder="Username"]').should('have.value','Admin')
    })

    it('Explicit assertions', ()=>{
        cy.visit('https://opensource-demo.orangehrmlive.com/web/index.php/auth/login')
        cy.get('input[placeholder="Username"]').type('Admin')
        cy.get('input[placeholder="Password"]').type('admin123')
        cy.get('button[type="submit"]').click()

        //use let to define value
        let expName ='xy';
        // get the selector, store it in x, and get the text value of x
        cy.get('.oxd-userdropdown-name').then( (x)=>{
            let actName = x.text()

            //BDD
            //expect(actName).to.equal(expName)
            expect(actName).to.not.equal(expName)

            //TDD
            //assert.equal(actName,expName)
            assert.notEqual(actName,expName)
        })
    })
})
