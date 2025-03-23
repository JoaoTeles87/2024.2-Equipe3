import { useState } from "react";
import { cadastrar } from "../../../shared/services/autorizacao";
import { useNavigate } from "react-router-dom";
import Button from "../../../shared/components/Button";
import Input from "../../../shared/components/Input";
import ErrorMessage from "../../../shared/components/ErrorMessage";
import styles from "../styles/Cadastro.module.css"; 
import globalStyles from "../../../shared/components/LoginCadastro.module.css"; 

const Cadastro = () => {
    const [nome, setNome] = useState("");
    const [cpf, setCpf] = useState("");
    const [email, setEmail] = useState("");
    const [professor, setProfessor] = useState("N");
    const [siape, setSiape] = useState("");
    const [senha, setSenha] = useState("");
    const [confirmarSenha, setConfirmarSenha] = useState("");
    const [error, setError] = useState("");
    const [successMessage, setSuccessMessage] = useState("");
    const navigate = useNavigate();

    const handleCadastro = async (e: React.FormEvent) => {
        e.preventDefault();

        try {
            const response = await cadastrar({ nome, cpf, email, professor, siape, senha, confirmarSenha });

            if (!response.success) {
                setError(response.error || "");
                return;
            }

            setSuccessMessage("Cadastro realizado com sucesso!");
            setNome("");
            setCpf("");
            setEmail("");
            setProfessor("N");
            setSiape("");
            setSenha("");
            setConfirmarSenha("");
            setError("");
        } catch (err) {
            setError("Falha no cadastro. Verifique os dados e tente novamente.");
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

                {successMessage ? (
                    <div style={{ textAlign: 'center', marginTop: '20px' }}>
                        <div style={{ color: 'green', fontSize: '1.2rem', marginBottom: '20px' }}>{successMessage}</div>
                        <Button onClick={() => navigate("/")} style={{ backgroundColor: "#6200ea", color: "#fff", borderRadius: "5px", padding: "10px 20px", cursor: "pointer" }}>
                            Voltar à Área de Login
                        </Button>
                    </div>
                ) : (
                    <form onSubmit={handleCadastro} className={styles.form}>
                        <Input type="text" placeholder="Nome" value={nome} onValueChange={setNome} />
                        <Input type="text" placeholder="CPF" value={cpf} onValueChange={setCpf} />
                        <Input type="email" placeholder="Email" value={email} onValueChange={setEmail} />
                        <Input type="password" placeholder="Senha" value={senha} onValueChange={setSenha} required />
                        <Input type="password" placeholder="Confirmar senha" value={confirmarSenha} onValueChange={setConfirmarSenha} required />

                        <label className={styles.label}>Você é professor?</label>
                        <select 
                            value={professor} 
                            onChange={(e) => setProfessor(e.target.value)} 
                            className={styles.select}
                        >
                            <option value="N">Não</option>
                            <option value="S">Sim, sou professor</option>
                        </select>

                        {professor === "S" && <Input type="text" placeholder="SIAPE" value={siape} onValueChange={setSiape} required />}

                        <div className={styles.footer}>
                            <span className={styles.link} onClick={() => navigate("/")}>Já possuo uma conta</span>
                            <Button type="submit" className={styles.button}  style={{ backgroundColor: "#6200ea", color: "#fff", borderRadius: "5px" }} >Criar</Button> 
                        </div>
                    </form>
                )}
            </div>
        </div>
    );
};

export default Cadastro;
