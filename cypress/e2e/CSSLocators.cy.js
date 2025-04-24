const cypress = require("cypress")

describe('CSS Locators', () => {
it('css locators',() => {
    cypress.visit('https://opensource-demo.orangehrmlive.com/')
    cypress.get('#search_query_top').type('T-shirt')
    cypress.get('[name="submit_search"]').click()
    cypress.get('.lighter').contains('T-shirts')
})


})