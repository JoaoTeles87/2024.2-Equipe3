describe("Deletar Avaliação", () => {
    beforeEach(() => {
      cy.intercept("DELETE", "http://127.0.0.1:5000/api/reviews/1", {
        statusCode: 200,
        body: { mensagem: "Avaliação deletada com sucesso!" },
      }).as("deleteReviewSuccess");
  
      cy.intercept("DELETE", "http://127.0.0.1:5000/api/reviews/999", {
        statusCode: 404,
        body: { error: "Avaliação não encontrada." },
      }).as("deleteReviewNotFound");
    });
  
    it("Deve deletar uma avaliação existente com sucesso", () => {
      cy.visit("/avaliacoes/1/delete");
      cy.contains("Tem certeza que deseja excluir essa avaliação?").should("be.visible");
  
      cy.get("button").contains("Confirmar Exclusão").click();
      
      cy.wait("@deleteReviewSuccess");
      cy.contains("Avaliação deletada com sucesso!").should("be.visible");
  
      // Aguarda o redirecionamento para a página de avaliações
      cy.url().should("include", "/avaliacoes");
    });
  
    it("Deve exibir erro ao tentar deletar uma avaliação inexistente", () => {
      cy.visit("/avaliacoes/999/delete");
      cy.contains("Tem certeza que deseja excluir essa avaliação?").should("be.visible");
  
      cy.get("button").contains("Confirmar Exclusão").click();
      
      cy.wait("@deleteReviewNotFound");
      cy.contains("Avaliação não encontrada.").should("be.visible");
    });
  });
  