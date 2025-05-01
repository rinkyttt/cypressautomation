//install ajv library 
// npm install ajv

const Ajv = require('ajv')
const avj = Ajv()

describe('Schema Validation',()=>{
    cy.request(
        {
            method:'GET',
            url:'https://fakesotreapi.com/products'
        }
    )
    .then((response)=>{
        const schema ={}//schema definition
        const validate = avj.compile(schema)
        const isvalidate = validate(response.body)
        expect(isvalidate).to.be.true;
    })
})