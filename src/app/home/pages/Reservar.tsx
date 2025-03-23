//import { useEffect } from "react";
//import { useNavigate } from "react-router-dom";
import SideBar from "../../../shared/components/SideBar/SideBar";
import styles from "../../../shared/components/SideBar/SideBar.module.css";
import Dropdown from 'react-bootstrap/Dropdown';


const Reservar = () => {
    //const navigate = useNavigate();
    
    return (
        <div className={styles.layoutContainer}>
            {/* Sidebar fixa à esquerda */}
            <div className={styles.sidebarWrapper}>
                <SideBar />
            </div>
            
            {/* Conteúdo da página */}
            <div className={styles.contentWrapper}>

            <Dropdown>
            <Dropdown.Toggle variant="success" id="dropdown-basic">
                Dropdown Button
            </Dropdown.Toggle>

            <Dropdown.Menu>
                <Dropdown.Item href="#/action-1">Action</Dropdown.Item>
                <Dropdown.Item href="#/action-2">Another action</Dropdown.Item>
                <Dropdown.Item href="#/action-3">Something else</Dropdown.Item>
            </Dropdown.Menu>
            </Dropdown>
                
                <h1>Salas Disponíveis</h1>
                
            </div>
        </div>
    );
};

export default Reservar;
