import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "../src/app/home/pages/Login"; 
import Cadastro from "../src/app/home/pages/Cadastro";  
import Reservar from "../src/app/home/pages/Reservar";   
import Perfil from "../src/app/home/pages/Perfil";  
import Avaliacoes from "../src/app/home/pages/Avaliacoes"; 
import Recursos from "./app/home/pages/Recursos"; 
import Manutencoes from "./app/home/pages/Manutencoes";
import 'bootstrap/dist/css/bootstrap.min.css';
import AvaliarSala from "../src/app/home/pages/CriarReview";
import ListarReviews from "../src/app/home/pages/ListarReview";
import ReviewDetalhes from "../src/app/home/pages/ObterReview";
import DeletarReview from "../src/app/home/pages/DeletarReview";
import AtualizarReview from "../src/app/home/pages/AtualizarReview";


function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Login />} />  {/* Tela inicial = Login */}
                <Route path="/cadastro" element={<Cadastro />} /> {/* Rota para Cadastro */}
                <Route path="/reservar" element={<Reservar />} /> {/* Rota para Reservas */}
                <Route path="/perfil" element={<Perfil />} /> {/* Rota para Modal */}
                <Route path="/avaliacoes" element={<Avaliacoes />} /> {/* Rota para Avaliações */}
                <Route path="/recursos" element={<Recursos />} /> {/* Rota para Recursos */}
                <Route path ="/manutencoes" element={<Manutencoes />} /> {/* Rota para Manutenções */}
                <Route path="/criar-review" element={<AvaliarSala />} /> {/* Rota para Criar Review */}
                <Route path="/reviews" element={<ListarReviews />} /> {/* Rota para Listar Review */}
                <Route path="/reviews/:id" element={<ReviewDetalhes />} /> {/* Rota para Obter Review */}
                <Route path="/reviews/:id/delete" element={<DeletarReview />} /> {/* Rota para Deletar Review */}
                <Route path="/reviews/:id/edit" element={<AtualizarReview />} /> {/* Rota para Atualizar Review */}
            </Routes>
        </Router>
    );
}

export default App;
