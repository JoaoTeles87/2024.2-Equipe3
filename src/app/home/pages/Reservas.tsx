// TESTE PARA VER INTEGRAÇÃO COM O BACKEND

// import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

const Reservas = () => {
    const navigate = useNavigate();

  

    return (
        <div>
            <h2>Reservas</h2>
            <p>Seu login foi validado! Agora você pode acessar as reservas.</p>
            <button onClick={() => navigate("/")}>Sair</button>
        </div>
    );
};

export default Reservas;
