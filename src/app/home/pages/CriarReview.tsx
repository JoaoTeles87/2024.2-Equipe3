import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Button from "../../../shared/components/Button";
import Input from "../../../shared/components/Input";
import ErrorMessage from "../../../shared/components/ErrorMessage";
import styles from "/src/app/home/styles/CriarReview.module.css"; // Estilos específicos
import globalStyles from "../../../shared/components/LoginCadastro.module.css"; // Estilos compartilhados
import StarRating from "../../../shared/components/StarRating/StarRating";
import stylesSideBar from "../../../shared/components/SideBar/SideBar.module.css";
import SideBar from "../../../shared/components/SideBar/SideBar";

const AvaliarSala = () => {
    const [reservaId, setReservaId] = useState("");
    const [salaId, setSalaId] = useState("");
    const [usuarioId, setUsuarioId] = useState("");
    const [nota, setNota] = useState("");
    const [comentario, setComentario] = useState("");
    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");

    const navigate = useNavigate();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        if (!reservaId) {
            setError("A ID da Reserva é obrigatória.");
            return;
        }
        else if (!salaId) {
            setError("A ID da Sala é obrigatória.");
            return;
        }
        else if (!usuarioId) {
            setError("A ID do Usuário é obrigatória.");
            return;
        }
        else if (!nota) {
            setError("A Nota é obrigatória.");
            return;
        }

        const payload = {
            reserva_id: parseInt(reservaId),
            sala_id: parseInt(salaId),
            usuario_id: parseInt(usuarioId),
            nota: parseInt(nota),
            comentario,
        };

        console.log(payload);

        try {
            const response = await fetch("http://127.0.0.1:5000/api/reviews", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(payload),
            });

            const data = await response.json();

            if (!response.ok) {
                setError(data.error || "Erro ao enviar avaliação.");
                return;
            }

            setSuccess("Avaliação enviada com sucesso!");

            setReservaId("");
            setSalaId("");
            setUsuarioId("");
            setNota("");
            setComentario("");
            setError("");

        } catch (err) {
            setError("Erro ao conectar com o servidor. Tente novamente.");
        }
    };

    return (
        <div className={stylesSideBar.layoutContainer}>
            {/* Sidebar fixa à esquerda */}
            <div className={stylesSideBar.sidebarWrapper}>
                <SideBar />
            </div>

            {/* Conteúdo da página */}
            <div className={stylesSideBar.contentWrapper}>
                <div className={globalStyles.container}>
                    <div className={globalStyles.card}>
                        <h2 className={styles.title}>Avaliar Sala</h2>
                        <p className={styles.subtitle}>Envie sua avaliação para a sala reservada</p>

                        {error && <ErrorMessage message={error} />}
                        {success && <p className={styles.successMessage}>{success}</p>}

                        <form onSubmit={handleSubmit} className={styles.form}>
                            <Input
                                type="text"
                                placeholder="ID da Reserva"
                                value={reservaId}
                                onValueChange={setReservaId}
                            />
                            <Input
                                type="text"
                                placeholder="ID da Sala"
                                value={salaId}
                                onValueChange={setSalaId}
                            />
                            <Input
                                type="text"
                                placeholder="ID do Usuário"
                                value={usuarioId}
                                onValueChange={setUsuarioId}
                            />
                            <div className={styles.starsWrapper}>
                                <label className={styles.label}>Nota:</label>
                                <StarRating
                                    rating={parseInt(nota) || 0}
                                    onRatingChange={(newRating) => {
                                        setNota(newRating.toString());
                                    }}
                                    editable={true}
                                />
                            </div>

                            <textarea
                                className={styles.textarea}
                                placeholder="Comentário (opcional)"
                                value={comentario}
                                onChange={(e) => setComentario(e.target.value)}
                            ></textarea>

                            <div className={styles.footer}>
                                <span className={styles.link} onClick={() => navigate("/avaliacoes")}>
                                    Voltar para o painel
                                </span>
                                <Button
                                    type="submit"
                                    className={styles.button}
                                    style={{ backgroundColor: "#6200ea", color: "#fff", borderRadius: "5px" }}
                                >
                                    Enviar Avaliação
                                </Button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default AvaliarSala;