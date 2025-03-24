import { useEffect, useState } from "react";
import styles from "/src/app/home/styles/Avaliacoes.module.css";
import { useNavigate } from "react-router-dom";
import StarRating from "../../../shared/components/StarRating/StarRating";
import stylesSideBar from "../../../shared/components/SideBar/SideBar.module.css";
import SideBar from "../../../shared/components/SideBar/SideBar";

interface Review {
    id: number;
    reserva_id: number;
    sala_id: number;
    usuario_id: number;
    nota: number;
    comentario: string;
    data_avaliacao: string;
}

const ListarReviews = () => {
    const [reviews, setReviews] = useState<Review[]>([]);
    const [error, setError] = useState("");
    const navigate = useNavigate();

    useEffect(() => {
        const fetchReviews = async () => {
            try {
                const response = await fetch("http://localhost:5000/api/reviews");
                if (!response.ok) {
                    const data = await response.json();
                    setError(data.error || "Erro ao buscar avaliações.");
                    return;
                }

                const data = await response.json();
                setReviews(data);
            } catch (err) {
                setError("Erro ao conectar com o servidor.");
            }
        };

        fetchReviews();
    }, []);

    const handleReviewClick = (reviewId: number) => {
        navigate(`/avaliacoes/${reviewId}`);
    };

    return (
        <div className={styles.pageContainer}>
            <div className={stylesSideBar.layoutContainer}>
                {/* Sidebar */}
                <div className={stylesSideBar.sidebarWrapper}>
                    <SideBar />
                </div>

                {/* Conteúdo da página */}
                <div className={stylesSideBar.contentWrapper}>
                    <h2 className={styles.title}>Avaliações de Usuários</h2>

                    {/* Botão Adicionar Avaliação */}
                    <div className={styles.addButtonWrapper}>
                        <button
                            onClick={() => navigate("/criar-avaliacao")}
                            className={styles.addButton}
                        >
                            Adicionar Avaliação
                        </button>
                    </div>

                    {error && <p className={styles.error}>{error}</p>}

                    {!error && reviews.length === 0 && (
                        <p className={styles.subtitle}>Nenhuma avaliação encontrada.</p>
                    )}

                    <div className={styles.gridContainer}>
                        {reviews.map((review) => (
                            <div
                                key={review.id}
                                className={styles.card}
                                onClick={() => handleReviewClick(review.id)}
                            >
                                <h3 className={styles.reviewTitle}>Avaliação #{review.id}</h3>
                                <p><strong>ID da Reserva:</strong> {review.reserva_id}</p>
                                <p><strong>ID da Sala:</strong> {review.sala_id}</p>
                                <p><strong>ID do Usuário:</strong> {review.usuario_id}</p>

                                <div className={styles.reviewItem}>
                                    <h3>Nota:</h3>
                                    <div className={styles.starsWrapper}>
                                        <StarRating rating={review.nota} editable={false} />
                                    </div>
                                </div>

                                <div className={styles.reviewItem}>
                                    <strong>Comentário:</strong>
                                    <p className={styles.comment}>{review.comentario || "Sem comentário."}</p>
                                </div>
                                <p><strong>Data da Avaliação:</strong> {new Date(review.data_avaliacao).toLocaleDateString()}</p>
                            </div>
                        ))}
                    </div>

                    <div className={styles.footer}>
                        <button
                            onClick={() => navigate("/perfil")}
                            className={styles.button}
                        >
                            Voltar ao Início
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ListarReviews;
