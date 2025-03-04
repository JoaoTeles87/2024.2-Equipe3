import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

const Reservas = () => {
    const navigate = useNavigate();

    useEffect(() => {
        const token = localStorage.getItem("token");
        
        if (!token) {
            alert("Acesso negado! Faça login para acessar esta página.");
            navigate("/"); // Redireciona para login caso não tenha token
        }
    }, [navigate]);

    return (
        <div>
            <h2>Reservas</h2>
            <p>Seu login foi validado! Agora você pode acessar as reservas.</p>
            <button onClick={() => navigate("/")}>Sair</button>
        </div>
    );
};

export default Reservas;
