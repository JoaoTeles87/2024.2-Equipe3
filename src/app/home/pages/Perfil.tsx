import SideBar from "../../../shared/components/SideBar/SideBar";
import styles from "../../../shared/components/SideBar/SideBar.module.css";
import { useNavigate } from "react-router-dom";


const Perfil = () => {
    const navigate = useNavigate();       
    return (
        <div className={styles.layoutContainer}>
            {/* Sidebar fixa à esquerda */}
            <div className={styles.sidebarWrapper}>
                <SideBar />
            </div>
            
            {/* Conteúdo da página */}
            <div className={styles.contentWrapper}>
                <h1>Perfil</h1>
                <p>Este é o restante da sua aplicação</p>
                <button onClick={() => navigate("/")}>Sair</button>
                </div>
            </div>
    );
};

export default Perfil;
