import { error } from "console";

describe('Avaliação de Sala', () => {

    beforeEach(() => {
        // Antes de cada teste, acessa a página de Avaliar Sala
        cy.visit('/criar-avaliacao');
    });

    it('Deve enviar avaliação com sucesso', () => {
        cy.get('input[placeholder="ID da Reserva"]').type('12345');
        cy.get('input[placeholder="ID da Sala"]').type('67890');
        cy.get('input[placeholder="ID do Usuário"]').type('1');
        cy.get('div._starContainer_1n7zt_1 span._star_1n7zt_1').eq(4).click(); // Avaliação em 5 estrelas
        cy.get('textarea[placeholder="Comentário (opcional)"]').type('Ótima sala!');
        cy.get('button[type="submit"]').click();

        // Verificar se a mensagem de sucesso é exibida
        cy.contains('Avaliação enviada com sucesso!') // Se a mensagem de sucesso tiver texto específico

        // Verificar se os campos foram limpos
        cy.get('input[placeholder="ID da Reserva"]').should('have.value', '');
        cy.get('input[placeholder="ID da Sala"]').should('have.value', '');
        cy.get('input[placeholder="ID do Usuário"]').should('have.value', '');
        cy.get('textarea[placeholder="Comentário (opcional)"]').should('have.value', '');

        // Verificar se o redirecionamento ocorreu para a página de avaliações
        cy.visit('/avaliacoes');
    
    });

    it('Deve mostrar erro se faltar o ID da Reserva', () => {
        cy.get('input[placeholder="ID da Sala"]').type('67890');
        cy.get('input[placeholder="ID do Usuário"]').type('1');
        cy.get('._starContainer_1n7zt_1 span._star_1n7zt_1').eq(3).click();

        cy.get('button[type="submit"]').click();

        // Verificar se a mensagem de erro é exibida
        cy.contains('A ID da Reserva é obrigatória.').should('be.visible');
    });

    it('Deve mostrar erro se faltar o ID da Sala', () => {
        cy.get('input[placeholder="ID da Reserva"]').type('12345');
        cy.get('input[placeholder="ID do Usuário"]').type('1');
        cy.get('._starContainer_1n7zt_1 span._star_1n7zt_1').eq(3).click();

        cy.get('button[type="submit"]').click();

        // Verificar se a mensagem de erro é exibida
        cy.contains('A ID da Sala é obrigatória.').should('be.visible');
    });

    it('Deve mostrar erro se faltar o ID do Usuário', () => {
        cy.get('input[placeholder="ID da Reserva"]').type('12345');
        cy.get('input[placeholder="ID da Sala"]').type('67890');
        cy.get('._starContainer_1n7zt_1 span._star_1n7zt_1').eq(3).click();

        cy.get('button[type="submit"]').click();

        // Verificar se a mensagem de erro é exibida
        cy.contains('A ID do Usuário é obrigatória.').should('be.visible');
    });

    it('Deve mostrar erro se faltar a Nota', () => {
        cy.get('input[placeholder="ID da Reserva"]').type('12345');
        cy.get('input[placeholder="ID da Sala"]').type('67890');
        cy.get('input[placeholder="ID do Usuário"]').type('1');

        cy.get('button[type="submit"]').click();

        // Verificar a visibilidade da mensagem de erro
        cy.contains('A Nota é obrigatória.').should('be.visible');
    });

});
