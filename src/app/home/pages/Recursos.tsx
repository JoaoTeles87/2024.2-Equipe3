import { useState, useEffect } from "react";
import SideBar from "../../../shared/components/SideBar/SideBar";
import styles from "../../../shared/components/SideBar/SideBar.module.css";
// import { useNavigate } from "react-router-dom";
// import Button from "../../../shared/components/Button";
// import Input from "../../../shared/components/Input";
// import ErrorMessage from "../../../shared/components/ErrorMessage";
//import styles from "../styles/Cadastro.module.css"; 
//import globalStyles from "../../../shared/components/LoginCadastro.module.css";

type Reserva = {
    id: number;
    sala_id: string;
    data: string;
    start_time: string;
    end_time: string;
    status: string;
};

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
            id: number; // Adicionado o ID da solicitação
            recursos: string;
            itens_nao_listados: string;
            observacoes: string;
            reserva_id: number;
        }
    }>({});
    const [showConfirmacaoExclusao, setShowConfirmacaoExclusao] = useState(false); // Estado para controlar o popup
    const [editando, setEditando] = useState(false); // Estado para controlar o modo de edição

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
        setEditando(false); // Sai do modo de edição ao trocar de reserva
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
                // Modo de edição: envia uma requisição PUT para atualizar a solicitação
                const idSolicitacao = solicitacoesCriadas[reservaSelecionada.id].id;
                resposta = await fetch(`http://127.0.0.1:5000/solicitacoes/recursos/${idSolicitacao}`, {
                    method: "PUT",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(dados),
                });

                const resultado = await resposta.json();
                if (resposta.ok) {
                    alert("Solicitação de recursos alterada.");
                    // Atualiza o estado com os novos dados
                    setSolicitacoesCriadas((prev) => ({
                        ...prev,
                        [reservaSelecionada.id]: { ...dados, id: idSolicitacao }, // Mantém o mesmo ID
                    }));
                    setSelectedItems([]);
                    setOutrosItens("");
                    setObservacoes("");
                    setEditando(false);
                } else {
                    alert(`Erro: ${resultado.erro || "Erro ao editar solicitação"}`);
                }
            } else {
                // Modo de criação: envia uma requisição POST para criar uma nova solicitação
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
                        [reservaSelecionada.id]: { ...dados, id: resultado.id }, // Salva o novo ID
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
                    // Remove a solicitação do estado
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
        setShowConfirmacaoExclusao(false); // Fecha o popup após a exclusão
    };

    const handleAlterar = () => {
        if (reservaSelecionada && solicitacoesCriadas[reservaSelecionada.id]) {
            const solicitacao = solicitacoesCriadas[reservaSelecionada.id];
            setSelectedItems(solicitacao.recursos.split(", "));
            setOutrosItens(solicitacao.itens_nao_listados);
            setObservacoes(solicitacao.observacoes);
            setEditando(true); // Entra no modo de edição
        } else {
            alert("Solicitação não encontrada.");
        }
    };

    const solicitacaoCriada = reservaSelecionada ? solicitacoesCriadas[reservaSelecionada.id] : null;

    return (
        <div className={styles.layoutContainer}>
            {/* Sidebar fixa à esquerda */}
            <div className={styles.sidebarWrapper}>
                <SideBar />
            </div>

            {/* Conteúdo da página */}
            <div className={styles.contentWrapper}>
                <div style={{ padding: "20px", maxWidth: "600px", margin: "auto" }}>
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
                                        onClick={() => setShowConfirmacaoExclusao(true)} // Abre o popup de confirmação
                                        style={{ marginRight: "10px", padding: "10px 20px", fontSize: "16px" }}
                                    >
                                        Excluir
                                    </button>
                                    <button onClick={handleAlterar} style={{ padding: "10px 20px", fontSize: "16px" }}>Alterar</button>
                                </>
                            ) : (
                                <>
                                    <div style={{ display: "flex", gap: "20px", flexWrap: "wrap", marginBottom: "20px" }}>
                                        {[
                                            ["Cabo USB", "Cabo P2", "Cabo HDMI", "Cabo VGA"],
                                            ["Extensão", "Microfone", "Mesa de som", "Passador"],
                                            ["Televisor", "Projetor", "Carregador", "Pen Drive"],
                                            ["Mouse", "Teclado", "Monitor", "USB-C HDMI"],
                                            ["Cafeteira", "Gelágua", "Apagador", "Piloto"],
                                        ].map((coluna, colIndex) => (
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

                    {/* Popup de confirmação de exclusão */}
                    {showConfirmacaoExclusao && (
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
                                <p style={{ marginBottom: "20px", fontSize: "18px" }}>Tem certeza que deseja excluir essa solicitação?</p>
                                <div style={{ display: "flex", justifyContent: "center", gap: "10px" }}>
                                    <button
                                        onClick={() => setShowConfirmacaoExclusao(false)} // Fecha o popup sem excluir
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
                                        onClick={handleExcluir} // Executa a exclusão
                                        style={{
                                            padding: "10px 20px",
                                            background: "#ff4d4d",
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
        </div>
    );
};

export default SolicitacaoRecursos;