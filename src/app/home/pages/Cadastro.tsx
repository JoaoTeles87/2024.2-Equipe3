import { useState } from "react";
import { cadastrar } from "../../../shared/services/autorizacao"; // Ajuste para a função correta
import { useNavigate } from "react-router-dom";

const Cadastro = () => {
    const [nome, setNome] = useState("");
    const [cpf, setCpf] = useState("");
    const [email, setEmail] = useState("");
    const [professor, setProfessor] = useState("N");
    const [siape, setSiape] = useState("");
    const [senha, setSenha] = useState("");
    const [confirmarSenha, setConfirmarSenha] = useState("");
    const [error, setError] = useState("");
    const navigate = useNavigate();

    const handleCadastro = async (e: React.FormEvent) => {
        e.preventDefault();

        console.log("Enviando para API:", { nome, cpf, email, professor, siape, senha, confirmarSenha });

        try {
            const response = await cadastrar({ nome, cpf, email, professor, siape, senha, confirmarSenha });

            if (!response.success) {
                setError(response.error);
                return;
            }

            console.log("Cadastro realizado com sucesso!");
            navigate("/"); // Redireciona para a tela de login após cadastro
        } catch (err) {
            console.error("Erro na requisição:", err);
            setError("Falha no cadastro. Verifique os dados e tente novamente.");
        }
    };

    return (
        <div>
            <h2>Cadastro</h2>
            {error && <p style={{ color: "red" }}>{error}</p>}
            <form onSubmit={handleCadastro}>
                <input
                    type="text"
                    placeholder="Nome"
                    value={nome}
                    onChange={(e) => setNome(e.target.value)}
                    required
                />
                <input
                    type="text"
                    placeholder="CPF"
                    value={cpf}
                    onChange={(e) => setCpf(e.target.value)}
                    required
                />
                <input
                    type="email"
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />
                <select value={professor} onChange={(e) => setProfessor(e.target.value)}>
                    <option value="N">Não sou professor</option>
                    <option value="S">Sou professor</option>
                </select>
                {professor === "S" && (
                    <input
                        type="text"
                        placeholder="Siape"
                        value={siape}
                        onChange={(e) => setSiape(e.target.value)}
                        required
                    />
                )}
                <input
                    type="password"
                    placeholder="Senha"
                    value={senha}
                    onChange={(e) => setSenha(e.target.value)}
                    required
                />
                <input
                    type="password"
                    placeholder="Confirmar Senha"
                    value={confirmarSenha}
                    onChange={(e) => setConfirmarSenha(e.target.value)}
                    required
                />
                <button type="submit">Cadastrar</button>
            </form>
            <p>Já tem uma conta?</p>
            <button onClick={() => navigate("/")}>Fazer Login</button> {/* Voltar para login */}
        </div>
    );
};

export default Cadastro;
