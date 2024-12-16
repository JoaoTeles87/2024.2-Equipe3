FEATURE: Cadastrar e fazer a manutenção dos usuários
    AS a usuário do SAGAA
    I WANT TO cadastrar-me no novo sistema
    SO THAT consiga acessar a plataforma


SCENARIO: Sucesso no cadastro de usuário.
    GIVEN eu estou na página de "Cadastro";
    WHEN eu preencho o campo "Nome" com "Demosténes"
    AND "CPF" com "123.456.789-00"
    AND "Email" com "demostenes@example.com"
    AND "Você é professor?" com "Não"
    AND "Senha" com "SecurePassword123"
    AND "Confirmar Senha" com "SecurePassword123";
    AND clico em "Cadastrar";
    THEN uma mensagem "Cadastro criado com sucesso!" deve ser exibida.


SCENARIO: Sucesso no cadastro de professor.
    GIVEN eu estou na página de "Cadastro";
    WHEN eu preencho o campo "Nome" com "Paula"
    AND "CPF" com "321.879.789-33"
    AND "Email" com "vanessa@example.com"
    AND "Você é professor?" com "Sim"
    AND "SIAP" com "101010"
    AND "Senha" com "12345678"
    AND "Confirmar Senha" com "12345678";
    AND clico em "Cadastrar";
    THEN uma mensagem "Cadastro criado com sucesso!" deve ser exibida.




SCENARIO: Fracasso no cadastro por campos obrigatórios não preenchidos
    GIVEN eu estou na página de "Cadastro de usuário";
    WHEN eu preencho o campo "Nome"
    AND "CPF"
    AND "Email"
    AND "Você é professor?" com "Não"
    AND "Senha"
    AND  deixo o campo "Confirmar Senha" vazio;
    AND clico em "Cadastrar"
    THEN uma sinalização informando que o campo "Confirmar Senha" é      obrigatório deve ser exibida.


SCENARIO: Fracasso no cadastro por duplicação de ID única.
    GIVEN eu estou na página de "Cadastro de usuário";
    WHEN eu preencho o campo "Nome" com "Carlos Mendes"
    AND "CPF" com "456.123.789-10"
    AND "Email" com "carlos.mendes@example.com"
    AND "Você é professor?" com "Sim"
    AND "SIAP" com "010101"
    AND "Senha" com "Password456"
    AND "Confirmar Senha" com "Password456";
    AND clico em "Cadastrar";
    THEN uma mensagem de erro "Erro: email/cpf/siap já está registrado." deve ser exibida.
   
   
SCENARIO: Fracasso no cadastro por senhas que não coincidem
    GIVEN eu estou na página de "Cadastro de usuário";
    WHEN eu preencho o campo "Nome" com "Beatriz"
    AND "CPF" com "789.456.123-00"
    AND "Email" com "Beatriz.oliveira@example.com"
    AND "Você é professor?" com "Não"
    AND "Senha" com "MyPassword123"
    AND "Confirmar Senha" com "DifferentPassword123";
    AND clico em "Cadastrar";
    THEN uma mensagem de erro "As senhas não coincidem." deve ser exibida.


# Login
SCENARIO: Sucesso no login
GIVEN eu estou na página de "Login";
WHEN eu preencho o campo "Email" com "demostenes@example.com"
AND o campo "Senha" com "SecurePassword123";
AND clico em "Entrar";
THEN eu devo ser redirecionado para a página "reserva"


SCENARIO: Fracasso no login
GIVEN eu estou na página de "Login";
WHEN eu preencho o campo "Email" com "demostenes@example.com"
AND o campo "Senha" com "SenhaIncorreta123";
AND clico em "Entrar";
THEN uma sinalização de erro "Usuário ou senha incorretos." deve ser exibida.

