describe('alerts',()=>{
    //1) Javascript Alert: It will have some text and an 'OK' button
    it.skip('js alert',()=>{
        cy.visit('http://the-internet.herokuapp.com/javascript_alerts')
        cy.get('button[onclick="jsAlert()"]').click();
        cy.on('window:alert',(t)=>{
            expect(t).to.contains('I am a JS Alert');
        })

        //alert window automatically closed by cypress
        cy.get('#result').should('have.text','You successfully clicked an alert')
    })
    //2)Javascript confirmation alert
    it.skip('js confirmation alter',()=>{
        cy.visit('http://the-internet.herokuapp.com/javascript_alerts')
        cy.get('button[onclick="jsConfirm()"]').click();
        cy.on('window:confirm',(t)=>{
            expect(t).to.contains('I am a JS Confirm');
        })
        cy.on('window:confirm',()=>false); // cypress closes alert window using cancel button
        cy.get('#result').should('have.text','You clicked: Cancel')
    })

    // Javascript Prompt Alert: It will have some text with a text box for user input along with 'OK' button 
    it.skip('Js prompt alert',()=>{
        cy.visit('http://the-internet.herokuapp.com/javascript_alerts')
        //set value for text input box before get the locator
        cy.window().then((win)=>{
            cy.stub(win,'prompt').returns('welcome');
        })
        cy.get('button[onclick="jsPrompt()"]').click();
        cy.on('window:confirm',()=>false);
        cy.get('#result').should('have.text','You entered: welcome')
        //cy.get('#result').should('have.text','You entered: welcome')
    })

    //Authenticated Alert
    it('Authenticated alert',()=>{
        cy.visit('https://the-internet.herokuapp.com/basic_auth',{auth:
                                                                    {username:'admin',
                                                                    password:'admin'}
                                                                });
        // shorter way to access the website:
        //cy.visit('https://admin:admin@the-internet.herokuapp.com/basic_auth')
        cy.get('div[class="example"] p').should('have.contain','Congratulations');
    })
    
})