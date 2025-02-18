from pytest_bdd import scenario, given, when, then, parsers
import pytest

# Cenários de teste_
@scenario("../features/manutencao.feature", "sucesso ao criar uma solicitação de manutenção para uma reserva concluída")
def teste_SucessoCriarManutencao():
    pass

@scenario("../features/manutencao.feature", "fracasso ao criar uma solicitação de manutenção sem preencher o campo descricao")
def teste_FracassoCriarManutencao():
    pass

@scenario("../features/manutencao.feature", "sucesso ao editar uma solicitação de manutenção existente")
def teste_SucessoEditarManutencao():
    pass

@scenario("../features/manutencao.feature", "fracasso ao editar solicitação de manutenção sem preencher o campo descricao")
def teste_FracassoEditarManutencao():
    pass

@scenario("../features/manutencao.feature", "sucesso ao excluir uma solicitação de manutenção existente")
def teste_SucessoExcluirManutencao():
    pass

# Given
@given(parsers.parse('o professor possui uma reserva de sala reserva_id "{reserva_id}" que já foi encerrada'))
def reserva_encerrada(contexto, reserva_id):
    contexto["reserva_id"] = int(reserva_id)

@given(parsers.parse('o professor já criou uma solicitação de manutenção associada a reserva_id "{reserva_id}"'))
def criar_solicitacao_previa(contexto, reserva_id):
    contexto["reserva_id"] = int(reserva_id)
    contexto["descricao"] = "Mesa quebrada."
    contexto["manutencao_id"] = 1 # Simulando um ID gerado pelo sistema

# When
@when(parsers.parse('ele envia uma requisição POST /solicitacoes/manutencao com os dados: reserva_id: "{reserva_id}", descricao: "{descricao}"'))
def criar_solicitacao(client, contexto, reserva_id, descricao):
    resposta = client.post("/solicitacoes/manutencao", json={"reserva_id": reserva_id, "descricao": descricao})
    contexto["resposta"] = resposta
    contexto["descricao"] = descricao

@when(parsers.parse('ele envia uma requisição PUT /solicitacoes/manutencao/{id} contendo o ID da solicitação de manutenção e a alteração descricao: "{descricao}"'))
def editar_solicitacao(client, contexto, descricao):
    import json
    manutencao_id = contexto["manutencao_id"]
    resposta = client.put(f"/solicitacoes/manutencao/{manutencao_id}", json={"descricao": descricao})
    contexto["resposta"] = resposta
    dados = json.loads(resposta.data)
    contexto["descricao"] = dados.get("descricao")

@when(parsers.parse('ele envia uma requisição DELETE /solicitacoes/manutencao/{id}'))
def deletar_solicitacao(client, contexto):
    manutencao_id = contexto["manutencao_id"]
    resposta = client.delete(f"/solicitacoes/manutencao/{manutencao_id}")
    contexto["resposta"] = resposta


# Then
@then(parsers.parse('o sistema retorna "{mensagem_tipo}" "{mensagem}" e um status "{status}"'))
def verificar_resposta(contexto, mensagem_tipo, mensagem, status):
    resposta = contexto["resposta"]
    assert resposta.status_code == int(status), f"{resposta}"
    assert resposta.get_json()[mensagem_tipo] == mensagem

@then(parsers.parse('a reserva reserva_id: "{reserva_id}" possui uma solicitação de manutenção com descricao: "{descricao}"'))
def verificar_solicitacao_de_manutencao(contexto, reserva_id, descricao):
    assert contexto["reserva_id"] == int(reserva_id)
    assert contexto["descricao"] == descricao

@then(parsers.parse('o sistema atualiza os detalhes da solicitação com descricao: "{descricao}"'))
def verificar_solicitacao_de_manutencao(contexto, descricao):
    assert contexto["descricao"] == descricao

@then(parsers.parse('o sistema remove a solicitação do banco de dados e retorna um status "{status}"'))
def verificar_exclusao_de_manutencao(contexto, status):
    assert contexto["resposta"].status_code == int(status)