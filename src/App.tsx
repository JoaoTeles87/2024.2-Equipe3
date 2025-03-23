import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./app/home/pages/Login";
import Cadastro from "./app/home/pages/Cadastro";
import Perfil from "./app/home/pages/Perfil"; 
import Reservas from "./app/home/pages/Reservas";


function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Login />} />
                <Route path="/cadastro" element={<Cadastro />} />
                <Route path="/perfil" element={<Perfil />} />
                {/* <Route path="/reservas" element={<Reservas />} /> */}
            </Routes>
        </Router>
    );
}

export default App;