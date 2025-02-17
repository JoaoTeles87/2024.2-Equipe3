from pytest_bdd import scenario, given, when, then, parsers
import pytest

# Cenários de teste
@scenario("../features/recursos.feature", "sucesso ao criar solicitação de recursos para uma reserva ativa com todos os campos preenchidos")
def teste_SucessoCriarSolicitacao():
    pass

@scenario("../features/recursos.feature", "fracasso ao criar solicitação de recursos com campos preenchidos com espaços ou não preenchidos")
def teste_FracassoCriarSolicitacaoCamposVazios():
    pass

@scenario("../features/recursos.feature", "fracasso ao criar solicitação de recursos com apenas o campo observacoes preenchido")
def teste_FracassoCriarSolicitacaoSomenteObservacoes():
    pass

@scenario("../features/recursos.feature", "sucesso ao criar solicitação de recursos sem preencher o campo itens_nao_listados")
def teste_SucessoCriarSolicitacaoSemItensNaoListados():
    pass

@scenario("../features/recursos.feature", "sucesso ao criar solicitação de recursos sem preencher o campo itens_nao_listados e o campo observacoes")
def teste_SucessoCriarSolicitacaoBasica():
    pass

@scenario("../features/recursos.feature", "sucesso ao criar solicitação de recursos com o campo de recursos vazio e apenas especificando os itens não listados")
def teste_SucessoCriarSolicitacaoComItensNaoListados():
    pass

@scenario("../features/recursos.feature", "sucesso ao criar solicitação de recursos com o campo de recursos vazio e especificando os itens não listados e as observacoes")
def teste_SucessoCriarSolicitacaoComItensNaoListadosObs():
    pass

@scenario("../features/recursos.feature", "sucesso ao editar uma solicitação de recursos existente")
def teste_SucessoEditarSolicitacao():
    pass

@scenario("../features/recursos.feature", "fracasso ao editar uma solicitação de recursos com apenas o campo observacoes preenchido")
def teste_FracassoEditarSolicitacao():
    pass

@scenario("../features/recursos.feature", "sucesso ao excluir uma solicitação de recursos existente")
def teste_SucessoExcluirSolicitacao():
    pass

# Given
@given(parsers.parse('o professor possui uma reserva ativa com reserva_id "{reserva_id}"'))
def reserva_ativa(contexto, reserva_id):
    contexto["reserva_id"] = int(reserva_id)

@given(parsers.parse('o professor possui uma solicitação de recursos associada a reserva_id "{reserva_id}"'))
def criar_solicitacao_previa(contexto, reserva_id):
    contexto["reserva_id"] = int(reserva_id)
    contexto["recursos"] = "Projetor, Teclado"
    contexto["solicitacao_id"] = 1

# When
@when(parsers.parse('ele envia uma requisição POST /solicitacoes/recursos com os dados: reserva_id: "{reserva_id}", recursos: "{recursos}", itens_nao_listados: "{itens_nao_listados}", observacoes: "{observacoes}"'))
def criar_solicitacao(client, contexto, reserva_id, recursos, itens_nao_listados, observacoes):
    resposta = client.post("/solicitacoes/recursos", json={"reserva_id": reserva_id, "recursos": recursos, "itens_nao_listados": itens_nao_listados, "observacoes": observacoes})
    contexto["resposta"] = resposta
    contexto["recursos"] = recursos
    contexto["itens_nao_listados"] = itens_nao_listados
    contexto["observacoes"] = observacoes

@when(parsers.parse('ele envia uma requisição PUT /solicitacoes/recursos/{id} contendo o ID da solicitação e os novos detalhes da solicitação recursos: "{recursos}", observacoes: "{observacoes}"'))
def editar_solicitacao(client, contexto, recursos, observacoes):
    import json
    solicitacao_id = contexto["solicitacao_id"]
    resposta = client.put(f"/solicitacoes/recursos/{solicitacao_id}", json={"recursos": recursos, "observacoes": observacoes})
    contexto["resposta"] = resposta
    dados = json.loads(resposta.data)
    contexto["recursos"] = recursos
    contexto["observacoes"] = observacoes

@when(parsers.parse('ele envia uma requisição DELETE /solicitacoes/recursos/{id} contendo o ID da solicitação'))
def deletar_solicitacao(client, contexto):
    solicitacao_id = contexto["solicitacao_id"]
    resposta = client.delete(f"/solicitacoes/recursos/{solicitacao_id}")
    contexto["resposta"] = resposta

# Then
@then(parsers.parse('o sistema retorna "{mensagem_tipo}" "{mensagem}" e um status "{status}"'))
def verificar_resposta(contexto, mensagem_tipo, mensagem, status):
    resposta = contexto["resposta"]
    assert resposta.status_code == int(status)
    assert resposta.get_json()[mensagem_tipo] == mensagem

@then(parsers.parse('a reserva_id "{reserva_id}" possui uma solicitação com recursos "{recursos}", itens_nao_listados "{itens_nao_listados}" e observacoes "{observacoes}"'))
def verificar_solicitacao(contexto, reserva_id, recursos, itens_nao_listados, observacoes):
    assert contexto["reserva_id"] == int(reserva_id)
    assert contexto["recursos"] == recursos
    assert contexto["itens_nao_listados"] == itens_nao_listados
    assert contexto["observacoes"] == observacoes

@then(parsers.parse('o sistema atualiza os detalhes da solicitação: recursos: "{recursos}", observacoes: "{observacoes}"'))
def verificar_solicitacao_de_manutencao(contexto, recursos, observacoes):
    assert contexto["recursos"] == recursos
    assert contexto["observacoes"] == observacoes

@then(parsers.parse('o sistema remove a solicitação do banco de dados e retorna um status "{status}"'))
def verificar_exclusao(contexto, status):
    assert contexto["resposta"].status_code == int(status)
