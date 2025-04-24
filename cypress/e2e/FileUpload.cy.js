import 'cypress-file-upload'

//https://github.com/abramenal/cypress-file-upload
describe('File Uploads',()=>{
    it('Single File Upload', ()=>{
        cy.visit('http://the-internet.herokuapp.com/upload');
        //Need to upload the file want to uplaod to the "fixtures" folder
        cy.get('#file-upload').attachFile('Equilar Profile - TimothyD. Cook.pdf')
        cy.get('#file-submit').click();
        cy.wait(5000);
        cy.get('div[class="example"] h3').should('have.text','File Uplaoded!');
    })

    it('File Upload - Rename', ()=>{
        cy.visit('http://the-internet.herokuapp.com/upload');
        // use filePath | fileName to rename 
        cy.get('#file-upload').attachFile({filePath:'Equilar Profile - TimothyD. Cook.pdf', fileName:'myfile.pdf'})
        cy.get('#file-submit').click();
        cy.wait(5000);
        cy.get('div[class="example"] h3').should('have.text','File Uplaoded!');
    })

    it('File Upload - Drag and drop', ()=>{
        cy.visit('http://the-internet.herokuapp.com/upload');
        cy.get('#drag-drop-upload').attachFile('Equilar Profile - TimothyD. Cook.pdf', {subjectType:'drag-n-drop'});
        cy.wait(5000);
    })

    it('Multiple files upload', ()=>{
        cy.visit('https://davidwalsh.name/demo/multiple-file-upload.php');
        cy.get('#filesToUplaod').attachFile(['test1.pdf','test2.pdf'])
    })

    it('File upload - Shadow Dom',()=>{
        //when inspect : see something like #shadow-root
        cy.visit('https://www.htmlelements.com/demos/fileupload/shadow-dom/index.html')
        //if element is in shadow Dom, use {includeShadowDome:true}
        cy.get('.smart-browse-input', {includeShadowDome:true}).attachFile('test1.pdf');
        cy.wait(5000);
        cy.get('.smart-item-name',{includeShadowDom:true}).contains('test1.pdf');
    })
})