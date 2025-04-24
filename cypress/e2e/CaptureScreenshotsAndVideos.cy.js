describe('mysuite',()=>{
    it('capture screenshots & videos', ()=>{
        //all screenshots captured will be saved in screenshots folder
        cy.visit('https://demo.opencart.com');
        cy.screenshot('homepage');
        cy.wait(5000);
        // screenshot of logo
        cy.screenshot('img[title"Your Store"]').screenshot('logo');

        //automatically capture screenshot & video on failure 
        cy.get('li:nth-child(7) a:nth-child(1)').click();
        cy.get('div[id="content"] h2').should('have.text','tablets');
        //npx cypress run --spec cypress\e2e\CaptureScreenshotsAndVideos.cy.js    <- run with this command will automatically capture

    })
})