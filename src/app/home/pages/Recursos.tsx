import { useState, useEffect } from "react";
import SideBar from "../../../shared/components/SideBar/SideBar";
import styles from "../../../shared/components/SideBar/SideBar.module.css";
import ConfirmacaoPopup from "../../../shared/components/ConfirmacaoPopup/ConfirmacaoPopup";

type Reserva = {
    id: number;
    sala_id: string;
    data: string;
    start_time: string;
    end_time: string;
    status: string;
};

// constante declarada antes com a refatoração
const RECURSOS_DISPONIVEIS = [
    ["Cabo USB", "Cabo P2", "Cabo HDMI", "Cabo VGA"],
    ["Extensão", "Microfone", "Mesa de som", "Passador"],
    ["Televisor", "Projetor", "Carregador", "Pen Drive"],
    ["Mouse", "Teclado", "Monitor", "USB-C HDMI"],
    ["Cafeteira", "Gelágua", "Apagador", "Piloto"],
];

const PegarReservaAtiva = async (): Promise<Reserva[]> => {
    try {
        const resposta = await fetch("http://127.0.0.1:5000/api/reservas");
        const reservas: Reserva[] = await resposta.json();
        return reservas.filter((reserva) => reserva.status === "ativa");
    } catch (erro) {
        console.error("Erro ao buscar reservas ativas:", erro);
        return [];
    }
};

const SolicitacaoRecursos = () => {
    const [reservasAtivas, setReservasAtivas] = useState<Reserva[]>([]);
    const [reservaSelecionada, setReservaSelecionada] = useState<Reserva | null>(null);
    const [selectedItems, setSelectedItems] = useState<string[]>([]);
    const [outrosItens, setOutrosItens] = useState("");
    const [observacoes, setObservacoes] = useState("");
    const [solicitacoesCriadas, setSolicitacoesCriadas] = useState<{
        [key: number]: {
            id: number;
            recursos: string;
            itens_nao_listados: string;
            observacoes: string;
            reserva_id: number;
        }
    }>({});
    const [showConfirmacaoExclusao, setShowConfirmacaoExclusao] = useState(false);
    const [editando, setEditando] = useState(false);

    useEffect(() => {
        const fetchReservas = async () => {
            const reservas = await PegarReservaAtiva();
            setReservasAtivas(reservas);
            if (reservas.length > 0) setReservaSelecionada(reservas[0]);
        };
        fetchReservas();
    }, []);

    const handleReservaChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
        const reservaId = parseInt(event.target.value);
        const reserva = reservasAtivas.find((res) => res.id === reservaId) || null;
        setReservaSelecionada(reserva);
        setSelectedItems([]);
        setOutrosItens("");
        setObservacoes("");
        setEditando(false);
    };

    const handleSubmit = async () => {
        if (!reservaSelecionada) {
            alert("Selecione uma reserva ativa!");
            return;
        }

        const dados = {
            recursos: selectedItems.join(", "),
            itens_nao_listados: outrosItens,
            observacoes,
            reserva_id: reservaSelecionada.id,
        };

        try {
            let resposta;
            if (editando && solicitacoesCriadas[reservaSelecionada.id]) {
                const idSolicitacao = solicitacoesCriadas[reservaSelecionada.id].id;
                resposta = await fetch(`http://127.0.0.1:5000/solicitacoes/recursos/${idSolicitacao}`, {
                    method: "PUT",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(dados),
                });

                const resultado = await resposta.json();
                if (resposta.ok) {
                    alert("Solicitação de recursos alterada.");
                    setSolicitacoesCriadas((prev) => ({
                        ...prev,
                        [reservaSelecionada.id]: { ...dados, id: idSolicitacao },
                    }));
                    setSelectedItems([]);
                    setOutrosItens("");
                    setObservacoes("");
                    setEditando(false);
                } else {
                    alert(`Erro: ${resultado.erro || "Erro ao editar solicitação"}`);
                }
            } else {
                resposta = await fetch("http://127.0.0.1:5000/solicitacoes/recursos", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(dados),
                });

                const resultado = await resposta.json();
                if (resposta.ok) {
                    alert("Parabéns, sua solicitação de recursos foi criada!");
                    setSolicitacoesCriadas((prev) => ({
                        ...prev,
                        [reservaSelecionada.id]: { ...dados, id: resultado.id },
                    }));
                    setSelectedItems([]);
                    setOutrosItens("");
                    setObservacoes("");
                } else {
                    alert(`Erro: ${resultado.erro || "Erro ao criar solicitação"}`);
                }
            }
        } catch (erro) {
            console.error("Erro ao enviar solicitação:", erro);
            alert("Erro ao enviar solicitação. Verifique a conexão com o servidor.");
        }
    };

    const handleExcluir = async () => {
        if (reservaSelecionada && solicitacoesCriadas[reservaSelecionada.id]) {
            const idSolicitacao = solicitacoesCriadas[reservaSelecionada.id].id;
            try {
                const resposta = await fetch(`http://127.0.0.1:5000/solicitacoes/recursos/${idSolicitacao}`, {
                    method: "DELETE",
                });

                if (resposta.ok) {
                    alert("Solicitação excluída com sucesso!");
                    setSolicitacoesCriadas((prev) => {
                        const newSolicitacoes = { ...prev };
                        delete newSolicitacoes[reservaSelecionada.id];
                        return newSolicitacoes;
                    });
                } else {
                    const resultado = await resposta.json();
                    alert(`Erro: ${resultado.erro || "Erro ao excluir solicitação"}`);
                }
            } catch (erro) {
                console.error("Erro ao excluir solicitação:", erro);
                alert("Erro ao excluir solicitação. Verifique a conexão com o servidor.");
            }
        }
        setShowConfirmacaoExclusao(false);
    };

    const handleAlterar = () => {
        if (reservaSelecionada && solicitacoesCriadas[reservaSelecionada.id]) {
            const solicitacao = solicitacoesCriadas[reservaSelecionada.id];
            setSelectedItems(solicitacao.recursos.split(", "));
            setOutrosItens(solicitacao.itens_nao_listados);
            setObservacoes(solicitacao.observacoes);
            setEditando(true);
        } else {
            alert("Solicitação não encontrada.");
        }
    };

    const solicitacaoCriada = reservaSelecionada ? solicitacoesCriadas[reservaSelecionada.id] : null;

    return (
        <div className={styles.layoutContainer}>
            <div className={styles.sidebarWrapper}>
                <SideBar />
            </div>

            <div className={styles.contentWrapper}>
                <div style={{ padding: "20px", maxWidth: "800px", marginLeft: "20px" }}>
                    <h2 style={{ marginBottom: "20px", fontSize: "24px" }}>Próximas Reservas</h2>

                    {reservasAtivas.length > 0 ? (
                        <>
                            <label style={{ display: "block", marginBottom: "10px", fontSize: "16px" }}>Selecione a reserva:</label>
                            <select
                                onChange={handleReservaChange}
                                value={reservaSelecionada?.id || ""}
                                style={{ width: "100%", padding: "10px", marginBottom: "20px", fontSize: "16px" }}
                            >
                                {reservasAtivas.map((reserva) => (
                                    <option key={reserva.id} value={reserva.id}>
                                        Sala {reserva.sala_id} - {reserva.data} {reserva.start_time} às {reserva.end_time}
                                    </option>
                                ))}
                            </select>

                            {reservaSelecionada && (
                                <>
                                    <h3 style={{ marginBottom: "10px", fontSize: "18px" }}>Sala: {reservaSelecionada.sala_id}</h3>
                                    <h3 style={{ marginBottom: "10px", fontSize: "18px" }}>Data: {reservaSelecionada.data}</h3>
                                    <h3 style={{ marginBottom: "20px", fontSize: "18px" }}>Hora: {reservaSelecionada.start_time} às {reservaSelecionada.end_time}</h3>
                                </>
                            )}

                            {solicitacaoCriada && !editando ? (
                                <>
                                    <h3 style={{ marginBottom: "10px", fontSize: "18px" }}>Itens: {solicitacaoCriada.recursos || "Nenhum"}</h3>
                                    <h3 style={{ marginBottom: "10px", fontSize: "18px" }}>Itens não listados: {solicitacaoCriada.itens_nao_listados || "Nenhum"}</h3>
                                    <h3 style={{ marginBottom: "20px", fontSize: "18px" }}>Quantidades e observações: {solicitacaoCriada.observacoes || "Nenhuma"}</h3>
                                    <button
                                        onClick={() => setShowConfirmacaoExclusao(true)}
                                        style={{ marginRight: "10px", padding: "10px 20px", fontSize: "16px" }}
                                    >
                                        Excluir
                                    </button>
                                    <button onClick={handleAlterar} style={{ padding: "10px 20px", fontSize: "16px" }}>Alterar</button>
                                </>
                            ) : (
                                <>
                                    <div style={{ display: "flex", gap: "20px", flexWrap: "wrap", marginBottom: "20px" }}>
                                        {RECURSOS_DISPONIVEIS.map((coluna, colIndex) => (
                                            <div key={colIndex} style={{ flex: "1" }}>
                                                {coluna.map((item) => (
                                                    <label key={item} style={{ display: "block", marginBottom: "10px", fontSize: "16px" }}>
                                                        <input
                                                            type="checkbox"
                                                            checked={selectedItems.includes(item)}
                                                            onChange={() =>
                                                                setSelectedItems((prev) =>
                                                                    prev.includes(item) ? prev.filter((i) => i !== item) : [...prev, item]
                                                                )
                                                            }
                                                        />
                                                        {item}
                                                    </label>
                                                ))}
                                            </div>
                                        ))}
                                    </div>

                                    <input
                                        type="text"
                                        placeholder="Especificar itens não listados"
                                        value={outrosItens}
                                        onChange={(e) => setOutrosItens(e.target.value)}
                                        style={{ width: "100%", marginTop: "10px", padding: "10px", marginBottom: "20px", fontSize: "16px" }}
                                    />

                                    <input
                                        type="text"
                                        placeholder="Especificar quantidades e demais observações"
                                        value={observacoes}
                                        onChange={(e) => setObservacoes(e.target.value)}
                                        style={{ width: "100%", marginTop: "10px", padding: "10px", marginBottom: "20px", fontSize: "16px" }}
                                    />

                                    <button
                                        onClick={handleSubmit}
                                        style={{
                                            marginTop: "15px",
                                            padding: "10px 20px",
                                            background: "#6200ea",
                                            color: "white",
                                            border: "none",
                                            cursor: "pointer",
                                            fontSize: "16px",
                                        }}
                                    >
                                        {editando ? "Confirmar Alteração" : "Solicitar Recursos"}
                                    </button>
                                </>
                            )}
                        </>
                    ) : (
                        <p style={{ fontSize: "16px" }}>Nenhuma reserva ativa encontrada.</p>
                    )}

                    {showConfirmacaoExclusao && (
                        <ConfirmacaoPopup
                            mensagem="Tem certeza que deseja excluir essa solicitação?"
                            onCancel={() => setShowConfirmacaoExclusao(false)}
                            onConfirm={handleExcluir}
                            textoConfirmar="Excluir Solicitação"
                        />
                    )}
                </div>
            </div>
        </div>
    );
};

export default SolicitacaoRecursos;