describe('Atualizar Avaliação de Sala', () => {
    beforeEach(() => {
        cy.visit('/avaliacoes/'); // Página de edição da avaliação
    });

    it('Deve atualizar a avaliação com sucesso ao modificar os campos', () => {
        // Verifica que os campos estão preenchidos com os valores iniciais
        cy.visit('/avaliacoes/5');
        cy.get('div._starContainer_1n7zt_1 span._star_1n7zt_1').eq(3);
        cy.contains('Boa sala, mas precisa de melhorias.');
        cy.get('._footer_5irnt_61 > :nth-child(2)').click();

        // Modifica os campos de nota e comentário
        cy.get('div._starContainer_1n7zt_1 span._star_1n7zt_1').eq(4).click();
        cy.get('textarea[placeholder="Comentário"]').clear().type('Excelente sala, muito boa para reuniões!');
        cy.get('button[type="submit"]').click();

        cy.contains("Avaliação atualizada com sucesso!");
        cy.visit('/avaliacoes/5');
    });

    it('Deve atualizar a avaliação com sucesso sem modificar os campos', () => {
        // Verifica que os campos estão preenchidos com os valores iniciais
        cy.visit('/avaliacoes/9');
        cy.get('div._starContainer_1n7zt_1 span._star_1n7zt_1').eq(3);
        cy.contains('Sala boa, mas falta mais organização com a infraestrutura.');

        // Não modifica nenhum campo
        cy.get('._footer_5irnt_61 > :nth-child(2)').click();

        // Submete o formulário
        cy.get('button[type="submit"]').click();

        // Verifica se a mensagem de sucesso é exibida
        cy.contains('Avaliação atualizada com sucesso!');

        // Verifica se o redirecionamento para a página da avaliação aconteceu
        cy.visit('/avaliacoes/9');

        // Verifica se as alterações não foram feitas
        cy.get('div._starContainer_1n7zt_1 span._star_1n7zt_1').eq(3);
        cy.contains('Sala boa, mas falta mais organização com a infraestrutura.');
    });

    it('Deve exibir erro ao tentar atualizar uma avaliação não encontrada', () => {
        // Acessa a página de editar com um ID inválido ou não encontrado
        cy.visit('/avaliacoes/9999/edit'); // ID inválido

        // Verifica se a mensagem de erro é exibida
        cy.contains('Avaliação não encontrada para o ID fornecido.').should('be.visible');

        cy.get('button').click();

        // Verifica se o usuário não foi redirecionado para a página de edição
        cy.visit('/avaliacoes');
    });
});
