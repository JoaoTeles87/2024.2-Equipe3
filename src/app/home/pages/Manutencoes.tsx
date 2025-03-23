//import { useEffect } from "react";
//import { useNavigate } from "react-router-dom";
import SideBar from "../../../shared/components/SideBar/SideBar";
import styles from "../../../shared/components/SideBar/SideBar.module.css";

const Manutencoes = () => {
    //const navigate = useNavigate();
    return (
        <div className={styles.layoutContainer}>
            {/* Sidebar fixa à esquerda */}
            <div className={styles.sidebarWrapper}>
                <SideBar />
            </div>
            
            {/* Conteúdo da página */}
            <div className={styles.contentWrapper}>
                <h1>Manutenções</h1>
                <p>Este é o restante da sua aplicação</p>
            </div>
        </div>
    );
};

export default Manutencoes;