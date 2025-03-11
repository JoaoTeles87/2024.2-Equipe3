import { useState } from "react";
import { login } from "../../../shared/services/autorizacao";
import { useNavigate } from "react-router-dom";

const Login = () => {
    const [email, setEmail] = useState("");
    const [senha, setPassword] = useState("");
    const [error, setError] = useState("");
    const navigate = useNavigate();

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault();

        console.log("Enviando para API:", { email, senha });
        try {
            const response = await login(email, senha);
    
            if (!response.success) {
                setError(response.error);   
                return;
             }
    
            navigate("/reservas");
        } catch (err) {
            console.error("Erro na requisição:", err);

            setError("Falha no login. Verifique suas credenciais.");
        }
    };
    

    return (
        <div>
            <h2>Login</h2>
            {error && <p style={{ color: "red" }}>{error}</p>}
            <form onSubmit={handleLogin}>
                <input
                    type="email"
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                />
                <input
                    type="password"
                    placeholder="Senha"
                    value={senha}
                    onChange={(e) => setPassword(e.target.value)}
                />
                <button type="submit">Entrar</button>
            </form>
            <p>Não tem uma conta?</p>
            <button onClick={() => navigate("/cadastro")}>Criar Conta</button> {/* Novo botão */}
        </div>
    );
};

export default Login;
