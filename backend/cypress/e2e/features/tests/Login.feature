FEATURE: Cadastrar e fazer a manutenção dos usuários
    AS a usuário do SAGAA
    I WANT TO cadastrar-me no novo sistema
    SO THAT consiga acessar a plataforma


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
