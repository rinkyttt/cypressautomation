describe('Mytest',()=>{
    //Direct access
    it('FixturesDemoTest',()=>{
        cy.visit('https://opensource-demo.orangehrmlive.com/')
        //put the file to cll in fixtures folder
        cy.fixture('orangehrm').then((data)=>{
            cy.get('input[placeholder="Username"]').type(data.username);
            cy.get('input[placeholder="Password"]').type(data.password);
            cy.get('button[type="submit"]').click();
    
            cy.get(':nth-child(2) > .oxd-main-menu-item').should('have.text',data.expected); 
        })

        // cy.get('input[placeholder="Username"]').type("Admin");
        // cy.get('input[placeholder="Password"]').type("admin123");
        // cy.get('button[type="submit"]').click();

        // cy.get(':nth-child(2) > .oxd-main-menu-item').should('have.text','PIM');
    })

    //Access through hook - for multiple it blocks 
    let userdata;
    before(()=>{
        cy.fixture('orangehrm').then((data)=>{
            userdata = data
        })
    })

    it.only('FixturesDemoTest',()=>{
        cy.visit('https://opensource-demo.orangehrmlive.com/')
        cy.get('input[placeholder="Username"]').type(userdata.username);
        cy.get('input[placeholder="Password"]').type(userdata.password);
        cy.get('button[type="submit"]').click();

        cy.get(':nth-child(2) > .oxd-main-menu-item').should('have.text',userdata.expected); 
    })
})