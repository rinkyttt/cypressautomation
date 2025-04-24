//Hooks
//before
//after 
//beforeEach
//afterEach

//Tags
//skip --> it.skip
//only --> it.only 

describe('MyTest',()=>{
    //run only once before all it blocks 
    before(()=>{
        cy.log('******* launch app *******')

    })
    //run only once after all it blocks, can be placed anywhere
    after(()=>{
        cy.log('**********close app *************')
    })
    //run before every it blocks
    beforeEach(()=>{
        cy.log('***** login **********')
    })
    //run after every it blocks
    afterEach(()=>{
        cy.log("********* logout ************")
    })

    it('Search',()=>{
        cy.log('*******searching**************')
    })

    it('advanced search', ()=>{
        cy.log('*******advanced searching**************')
    })

    it('listing products', ()=>{
        cy.log('*******listing products**************')
    })
})