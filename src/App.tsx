import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "../src/app/home/pages/Login";  // Importe a página de Login
import Cadastro from "../src/app/home/pages/Cadastro";  // Importe a página de Cadastro
import Reservas from "../src/app/home/pages/Reservas";  
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
                <Route path="/reservas" element={<Reservas />} /> {/* Rota para Reservas */}
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
