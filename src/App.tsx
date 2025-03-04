import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "../src/app/home/pages/Login";  // Importe a página de Login
//import Reservas from "../src/app/home/pages/Reservas";  // Importe a página de Login
import Cadastro from "../src/app/home/pages/Cadastro";  // Importe a página de Cadastro
import Reservas from "../src/app/home/pages/Reservas";   

function App() {
  

    return (
        <Router>
            <Routes>
                <Route path="/" element={<Login />} />  {/* Tela inicial = Login */}
                <Route path="/cadastro" element={<Cadastro />} /> {/* Rota para Cadastro */}
                <Route path="/reservas" element={<Reservas />} /> {/* Rota para Reservas */}
            </Routes>
        </Router>
    );
}

export default App;
