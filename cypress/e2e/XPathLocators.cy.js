describe('XPathLocators', ()=>{
it('find number of products', ()=>{
    cy.visit('http://automationpractice.com/index.php')
    cy.xpath('//ul[@id="homefeatured"]/li').should('have.length',7)
})


})