describe('MyTest',()=>{

    it('DataDrivenTest',()=>{
        cy.fixture('orangehrm2').then((data)=>{
            cy.visit('https://opensource-demo.orangehrmlive.com/')
            //iteration 
            data.forEach((userdata)=>{
                cy.get('input[placeholder="Username"]').type(userdata.username);
                cy.get('input[placeholder="Password"]').type(userdata.password);
                cy.get('button[type="submit"]').click();
                if(userdata.username=='Admin' && userdata.password=='admin123'){
                    cy.get(':nth-child(2) > .oxd-main-menu-item').should('have.text',userdata.expected); 
                    cy.get('.oxd-userdropdown-tab').click();
                    cy.get(':nth-child(4) > .oxd-userdropdown-link').click();
                    cy.wait(2000);
                }
                else{
                    cy.get('oxd-text.oxd-test--p.oxd-alert-content-text').should('have.text',userdata.expected)
                }
            })
        })
    })
})