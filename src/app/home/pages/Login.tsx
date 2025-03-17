import { useState } from "react";
import { login } from "../../../shared/services/autorizacao";
import { useNavigate } from "react-router-dom";
import Button from "../../../shared/components/Button";
import Input from "../../../shared/components/Input";
import ErrorMessage from "../../../shared/components/ErrorMessage";
import styles from "../styles/Login.module.css"; // ✅ Estilos específicos
import globalStyles from "../../../shared/components/LoginCadastro.module.css"; // ✅ Estilos compartilhados
import Loader from "../../../shared/components/Loader";

const Login = () => {
    const [email, setEmail] = useState("");
    const [senha, setPassword] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);

        try {
            const response = await login(email, senha);
    
            if (!response.success) {
                setError(response.error ?? "");
                setLoading(false);
                return;
            }
    
            navigate("/reservas");
        } catch (err) {
            setError("Falha no login. Verifique suas credenciais.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className={globalStyles.container}>
            <div className={globalStyles.card}>
                <h2 className={styles.title}>SAGAA</h2>
                <p className={styles.subtitle}>
                    Sistema de Agendamento e <br />
                    Gerenciamento Acadêmico Automático
                </p>

                {error && <ErrorMessage message={error} />}

                <form onSubmit={handleLogin} className={styles.form}>
                    <Input type="email" placeholder="Email" value={email} onValueChange={setEmail} />
                    <Input type="password" placeholder="Senha" value={senha} onValueChange={setPassword} />
                    <Button type="submit" disabled={loading} style={{ backgroundColor: "#6200ea", color: "#fff" }}>
                        {loading ? <Loader /> : "Entrar"}
                    </Button>

                </form>

                <div className={styles.links}>
                    <span className={styles.link}>Esqueceu a senha?</span>
                    <span onClick={() => navigate("/cadastro")}  className={styles.link}>Não tem conta ainda?</span>
                </div>
            </div>
        </div>
    );
};

export default Login;
