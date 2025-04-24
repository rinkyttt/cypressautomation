import 'cypress-iframe';

require ('@4tw/cypress-drag-drop')
describe('Mouse Operations', ()=>{
    it.skip('MouseHover',()=>{
        cy.visit('https://demo.opencart.com/');
        // before mouse hovering to the tab, the dropdown list should not be visible 
        cy.get('mac selector').should('not.be.visible')
        // move mouse to the tab
        cy.get('.nav > :nth-child(1) > .dropdown-toggle').trigger('mouseover').click();
        cy.get('mac selector').should('be.visible');

    });
    
    it.skip('Right Click',()=>{
        cy.visit('https://swisni.github.io/Query-contextMenu/demo.html')
        // Approach 1
        cy.get('.context-menu-one.btn.btn-neutral').trigger('contextmenu'); // contextmenu perform as the right click 
        cy.get('.context-menu-icon-copy > span').should('be.visible'); // right click menu item should be visible
        // Approach 2
        cy.get('.context-menu-one.btn.btn-neutral').rightclick();

    });

    it.skip('Double Click', ()=>{
        cy.visit('https://w3scholls.com/tags/tryit.asp?filename=tryhtml5_ev_ondblclick3');
        cy.frameLoaded('#iframeResult');

        //Approach1 - trigger()
        cy.iframe('#iframeResult').find('button[ondblclick="myFucntion()"]').trigger('dblclick');
        cy.iframe('#iframeResult').find('#field2').should('have.value','Hello World!');

        //Approach2 - dbclick()
        cy.iframe('#iframeResult').find('button[ondblclick="myFucntion()"]').dblclick();
        cy.iframe('#iframeResult').find('#field2').should('have.value','Hello World!');


    });

    it.skip('Drag and Drop using plugin',()=>{
        cy.visit('http://www.dhtmlgoodies.com/scripts/drag-drop-custom/demo-drag-drop-3.html')
        cy.get('#box6').drag('#box106',{force:true}); //box6 is the box you want to drag, and box106 is the target
    });

    it.only('Scrolling Page',()=>{
        cy.visit('https://www.countries-ofthe-world.com/flags-of-the-world.html')
        //scroll down 
        // get the element first; use duration to change scrolling speed
        cy.get(':nth-child(1) > tbody > :nth-child(86) > :nth-child(1) > img').scrollIntoView({duration:2000})
        cy.get(':nth-child(1) > tbody > :nth-child(86) > :nth-child(1) > img').should('be.visible')
        // then scroll up
        cy.get(':nth-child(1) > tbody > :nth-child(4) > :nth-child(1) > img').scrollIntoView({duration:2000})
        cy.get(':nth-child(1) > tbody > :nth-child(4) > :nth-child(1) > img').should('be.visible')        
    })
})