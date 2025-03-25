describe("Listar Avaliações de Usuários", () => {

    it("Deve listar as avaliações disponíveis", () => {
      // Mockando uma resposta bem-sucedida
      cy.intercept('GET', 'http://127.0.0.1:5000/api/reviews', {
        statusCode: 200,
        body: [
          {
            id: 1,
            reserva_id: 101,
            sala_id: 202,
            usuario_id: 303,
            nota: 4,
            comentario: "Boa sala, mas precisa de melhorias.",
            data_avaliacao: "2025-03-20T12:00:00Z",
          },
          {
            id: 2,
            reserva_id: 102,
            sala_id: 203,
            usuario_id: 304,
            nota: 5,
            comentario: "Excelente sala, muito boa para reuniões!",
            data_avaliacao: "2025-03-22T12:00:00Z",
          }
        ]
      }).as('getReviews');
  
      cy.visit('/avaliacoes'); // Visite a página de avaliações
  
      // Espera a interceptação acontecer
      cy.wait('@getReviews');
  
      // Verificar se as avaliações são exibidas corretamente
      cy.get('._gridContainer_jtq64_69 > :nth-child(1)');
      cy.get('._gridContainer_jtq64_69 > :nth-child(2)');
      cy.get(':nth-child(1) > ._reviewTitle_jtq64_119').should('contain', 'Avaliação #1');
      cy.get(':nth-child(2) > ._reviewTitle_jtq64_119').should('contain', 'Avaliação #2');
      cy.get('._gridContainer_jtq64_69 > :nth-child(1) > :nth-child(2)').should('contain', 'ID da Reserva: 101');
      cy.get('._gridContainer_jtq64_69 > :nth-child(2) > :nth-child(2)').should('contain', 'ID da Reserva: 102');
    });
  
    it("Deve exibir mensagem quando não houver avaliações cadastradas", () => {
      // Mockando uma resposta com nenhuma avaliação
      cy.intercept('GET', 'http://127.0.0.1:5000/api/reviews', {
       statusCode: 200,
       body: []
      }).as('getReviewsEmpty');
  
      cy.visit('/avaliacoes'); // Visite a página de avaliações
  
      // Espera a interceptação acontecer
      cy.wait('@getReviewsEmpty');
  
      // Verificar a exibição da mensagem de "Nenhuma avaliação encontrada."
      cy.get('._subtitle_jtq64_41').should('contain', 'Nenhuma avaliação encontrada.');
    });
  
  });
