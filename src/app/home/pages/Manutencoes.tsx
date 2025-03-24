import { useState, useEffect } from "react";
import SideBar from "../../../shared/components/SideBar/SideBar";
import styles from "../../../shared/components/SideBar/SideBar.module.css";

type Reserva = {
    id: number;
    sala_id: string;
    data: string;
    start_time: string;
    end_time: string;
    status: string;
};

type SolicitacaoManutencao = {
    id: number;
    reserva_id: number;
    descricao: string;
};

const PegarReservasFinalizadas = async (professorId: number): Promise<Reserva[]> => {
    try {
        const resposta = await fetch(`http://127.0.0.1:5000/api/reservas/${professorId}`);
        const reservas: Reserva[] = await resposta.json();
        return reservas.filter((reserva) => reserva.status === "finalizada" || reserva.status === "ativa");
    } catch (erro) {
        console.error("Erro ao buscar reservas finalizadas:", erro);
        return [];
    }
};

const Manutencoes = () => {
    const [reservasFinalizadas, setReservasFinalizadas] = useState<Reserva[]>([]);
    const [solicitacoesManutencao, setSolicitacoesManutencao] = useState<{
        [key: number]: SolicitacaoManutencao;
    }>({});
    const [descricaoPorReserva, setDescricaoPorReserva] = useState<{ [key: number]: string }>({});
    const [editando, setEditando] = useState<number | null>(null); // ID da reserva em edição
    const [reservaParaExcluir, setReservaParaExcluir] = useState<number | null>(null); // ID da reserva a ser excluída

    // Supondo que o ID do professor logado seja 3 (substitua pelo valor real)
    const professorId = 3;

    useEffect(() => {
        const fetchReservas = async () => {
            const reservas = await PegarReservasFinalizadas(professorId);
            setReservasFinalizadas(reservas);
        };
        fetchReservas();
    }, [professorId]);

    const handleSolicitarManutencao = async (reservaId: number) => {
        const descricao = descricaoPorReserva[reservaId] || "";
        if (!descricao.trim()) {
            alert("O campo 'O que havia de errado na sala?' não pode estar vazio.");
            return;
        }

        try {
            const resposta = await fetch("http://127.0.0.1:5000/solicitacoes/manutencao", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ reserva_id: reservaId, descricao }),
            });

            const resultado = await resposta.json();
            if (resposta.ok) {
                alert("Solicitação de manutenção criada com sucesso!");
                setSolicitacoesManutencao((prev) => ({
                    ...prev,
                    [reservaId]: { id: resultado.id, reserva_id: reservaId, descricao },
                }));
                setDescricaoPorReserva((prev) => ({ ...prev, [reservaId]: "" })); // Limpa o campo de texto
            } else {
                alert(`Erro: ${resultado.erro || "Erro ao criar solicitação"}`);
            }
        } catch (erro) {
            console.error("Erro ao enviar solicitação:", erro);
            alert("Erro ao enviar solicitação. Verifique a conexão com o servidor.");
        }
    };

    const handleEditarManutencao = async (reservaId: number) => {
        const descricao = descricaoPorReserva[reservaId] || "";
        if (!descricao.trim()) {
            alert("O campo 'O que havia de errado na sala?' não pode estar vazio.");
            return;
        }

        const solicitacaoId = solicitacoesManutencao[reservaId].id;
        try {
            const resposta = await fetch(`http://127.0.0.1:5000/solicitacoes/manutencao/${solicitacaoId}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ descricao }),
            });

            const resultado = await resposta.json();
            if (resposta.ok) {
                alert("Solicitação de manutenção atualizada com sucesso!");
                setSolicitacoesManutencao((prev) => ({
                    ...prev,
                    [reservaId]: { ...prev[reservaId], descricao },
                }));
                setDescricaoPorReserva((prev) => ({ ...prev, [reservaId]: "" })); // Limpa o campo de texto
                setEditando(null); // Sai do modo de edição
            } else {
                alert(`Erro: ${resultado.erro || "Erro ao editar solicitação"}`);
            }
        } catch (erro) {
            console.error("Erro ao editar solicitação:", erro);
            alert("Erro ao editar solicitação. Verifique a conexão com o servidor.");
        }
    };

    const handleExcluirManutencao = async (reservaId: number) => {
        const solicitacaoId = solicitacoesManutencao[reservaId].id;
        try {
            const resposta = await fetch(`http://127.0.0.1:5000/solicitacoes/manutencao/${solicitacaoId}`, {
                method: "DELETE",
            });

            if (resposta.ok) {
                alert("Solicitação de manutenção excluída com sucesso!");
                setSolicitacoesManutencao((prev) => {
                    const newSolicitacoes = { ...prev };
                    delete newSolicitacoes[reservaId];
                    return newSolicitacoes;
                });
                setDescricaoPorReserva((prev) => ({ ...prev, [reservaId]: "" })); // Limpa o campo de texto
                setEditando(null); // Sai do modo de edição
            } else {
                const resultado = await resposta.json();
                alert(`Erro: ${resultado.erro || "Erro ao excluir solicitação"}`);
            }
        } catch (erro) {
            console.error("Erro ao excluir solicitação:", erro);
            alert("Erro ao excluir solicitação. Verifique a conexão com o servidor.");
        }
        setReservaParaExcluir(null); // Fecha o popup após a exclusão
    };

    return (
        <div className={styles.layoutContainer}>
            {/* Sidebar fixa à esquerda */}
            <div className={styles.sidebarWrapper}>
                <SideBar />
            </div>

            {/* Conteúdo da página */}
            <div className={styles.contentWrapper}>
                <h1 style={{ fontSize: "24px", marginBottom: "20px" }}>Solicitação de Manutenções</h1>
                {reservasFinalizadas.length > 0 ? (
                    reservasFinalizadas.map((reserva) => (
                        <div key={reserva.id} style={{ marginBottom: "20px", padding: "20px", border: "1px solid #ccc", borderRadius: "8px" }}>
                            <h3 style={{ fontSize: "20px", fontWeight: "bold", marginBottom: "10px" }}>Sala {reserva.sala_id}</h3>
                            <p style={{ marginBottom: "5px" }}>Data: {reserva.data} | Hora: {reserva.start_time} às {reserva.end_time}</p>

                            {solicitacoesManutencao[reserva.id] && editando !== reserva.id ? (
                                <>
                                    <p style={{ fontWeight: "bold", marginBottom: "10px" }}>Solicitação realizada:</p>
                                    <p style={{ marginBottom: "15px" }}>{solicitacoesManutencao[reserva.id].descricao}</p>
                                    <div style={{ display: "flex", gap: "10px" }}>
                                        <button
                                            onClick={() => {
                                                setEditando(reserva.id); // Entra no modo de edição
                                                setDescricaoPorReserva((prev) => ({ ...prev, [reserva.id]: solicitacoesManutencao[reserva.id].descricao }));
                                            }}
                                            style={{
                                                padding: "8px 16px",
                                                background: "#4CAF50",
                                                color: "white",
                                                border: "none",
                                                borderRadius: "4px",
                                                cursor: "pointer",
                                                fontSize: "14px",
                                            }}
                                        >
                                            Editar
                                        </button>
                                        <button
                                            onClick={() => setReservaParaExcluir(reserva.id)}
                                            style={{
                                                padding: "8px 16px",
                                                background: "#f44336",
                                                color: "white",
                                                border: "none",
                                                borderRadius: "4px",
                                                cursor: "pointer",
                                                fontSize: "14px",
                                            }}
                                        >
                                            Excluir
                                        </button>
                                    </div>
                                </>
                            ) : (
                                <>
                                    <textarea
                                        placeholder="O que havia de errado na sala?"
                                        value={descricaoPorReserva[reserva.id] || ""}
                                        onChange={(e) =>
                                            setDescricaoPorReserva((prev) => ({ ...prev, [reserva.id]: e.target.value }))
                                        }
                                        style={{ width: "100%", marginBottom: "15px", padding: "10px", borderRadius: "4px", border: "1px solid #ccc" }}
                                    />
                                    <button
                                        onClick={() =>
                                            editando === reserva.id
                                                ? handleEditarManutencao(reserva.id)
                                                : handleSolicitarManutencao(reserva.id)
                                        }
                                        style={{
                                            width: "auto", // Largura automática
                                            padding: "10px 20px",
                                            background: "#555",
                                            color: "white",
                                            border: "none",
                                            borderRadius: "4px",
                                            cursor: "pointer",
                                            fontSize: "16px",
                                        }}
                                    >
                                        {editando === reserva.id ? "Confirmar Edição" : "Solicitar Manutenção"}
                                    </button>
                                </>
                            )}
                        </div>
                    ))
                ) : (
                    <p>Nenhuma reserva finalizada encontrada.</p>
                )}

                {/* Popup de confirmação de exclusão */}
                {reservaParaExcluir !== null && (
                    <div style={{
                        position: "fixed",
                        top: "0",
                        left: "0",
                        width: "100%",
                        height: "100%",
                        backgroundColor: "rgba(0, 0, 0, 0.5)",
                        display: "flex",
                        justifyContent: "center",
                        alignItems: "center",
                    }}>
                        <div style={{
                            backgroundColor: "white",
                            padding: "20px",
                            borderRadius: "8px",
                            textAlign: "center",
                        }}>
                            <p style={{ marginBottom: "20px", fontSize: "18px" }}>
                                Tem certeza que deseja excluir essa solicitação? Essa ação é irreversível.
                            </p>
                            <div style={{ display: "flex", justifyContent: "center", gap: "10px" }}>
                                <button
                                    onClick={() => setReservaParaExcluir(null)} // Fecha o popup sem excluir
                                    style={{
                                        padding: "10px 20px",
                                        background: "#ccc",
                                        color: "black",
                                        border: "none",
                                        borderRadius: "4px",
                                        cursor: "pointer",
                                        fontSize: "16px",
                                    }}
                                >
                                    Cancelar
                                </button>
                                <button
                                    onClick={() => handleExcluirManutencao(reservaParaExcluir)} // Executa a exclusão
                                    style={{
                                        padding: "10px 20px",
                                        background: "#f44336",
                                        color: "white",
                                        border: "none",
                                        borderRadius: "4px",
                                        cursor: "pointer",
                                        fontSize: "16px",
                                    }}
                                >
                                    Excluir Solicitação
                                </button>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default Manutencoes;