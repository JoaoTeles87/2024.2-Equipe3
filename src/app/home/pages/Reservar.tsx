import { useState } from "react";
import SideBar from "../../../shared/components/SideBar/SideBar";
import styles from "../../../shared/components/SideBar/SideBar.module.css";
import SalaCard from "../components/SalaCard";



const Reservar = () => {
    //const navigate = useNavigate();

    const [tipoSala, setTipoSala] = useState("Reunião");
    const [data, setData] = useState("");
    const [horaInicio, setHoraInicio] = useState("");
    const [horaFim, setHoraFim] = useState("");
    const [equipamentosSelecionados, setEquipamentosSelecionados] = useState<string[]>([]);
    const [showEquipamentosDropdown, setShowEquipamentosDropdown] = useState(false);
    const [salasFiltradas, setSalasFiltradas] = useState<any[]>([]);
    const [buscaFeita, setBuscaFeita] = useState(false);
    const EQUIPAMENTOS = [
        "Ar-condicionado", "Cabo P2", "Cabo HDMI", "Cabo VGA", "Microfone", "Extensão",
        "Mesa de som", "Passador", "Televisor", "Projetor", "Carregador", "Pen Drive",
        "Mouse", "Teclado", "Monitor", "USB-C", "Cafeteira", "Gelágua"
    ];

    const handleReserva = async (salaId: number) => {
        const professorId = 3; // Mockado mesmo
      
        const reservaData = {
          sala_id: salaId,
          data: data,
          start_time: horaInicio,
          end_time: horaFim,
        };
      
        try {
          const response = await fetch(`http://127.0.0.1:5000/api/reservas/${professorId}`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify(reservaData)
        });
      
          const resultado = await response.json();
      
          if (response.ok) {
            alert("Reserva criada com sucesso!");
          } else {
            alert(resultado.erro || "Erro ao criar reserva.");
          }
        } catch (error) {
          console.error("Erro na requisição:", error);
          alert("Erro ao conectar com o servidor.");
        }
    };


    const handleProcurarSalas = async () => {
        if (!data || !horaInicio || !horaFim) {
            alert("Data e horários são obrigatórios");
            return;
        }
    
        const params = new URLSearchParams();
        params.append("data", data);
        params.append("start_time", horaInicio);
        params.append("end_time", horaFim);
        params.append("tipo", tipoSala);
        equipamentosSelecionados.forEach(eq => params.append("equipamentos", eq));
    
        try {
            const response = await fetch(`http://127.0.0.1:5000/api/salas?${params.toString()}`);
            const data = await response.json();
    
            if (response.ok) {
                setSalasFiltradas(data);
                setBuscaFeita(true);
            } else {
                alert(data.mensagem || "Erro ao buscar salas");
            }
        } catch (error) {
            console.error("Erro ao buscar salas:", error);
        }
    };

    const inputStyle: React.CSSProperties = {
        padding: "10px 12px",
        border: "2px solid #cfd8dc", // Light gray-blue
        borderRadius: "6px",
        fontSize: "16px",
        minWidth: "150px",
    };

    const selectorStyle: React.CSSProperties = {
        padding: "10px 12px",
        border: "2px solid #cfd8dc",
        borderRadius: "6px",
        fontSize: "16px",
        minWidth: "150px",
        backgroundColor: "white",
        color: "#333",
        cursor: "pointer",
        textAlign: "left",
        appearance: "none", // removes native browser button styles
        WebkitAppearance: "none",
        MozAppearance: "none"
    };
    
    return (
        <div className={styles.layoutContainer}>
            {/* Sidebar fixa à esquerda */}
            <div className={styles.sidebarWrapper}>
                <SideBar />
            </div>
            
            {/* Conteúdo da página */}
            <div className={styles.contentWrapper}>

                <div
                style={{
                    display: "flex",
                    flexWrap: "wrap",
                    gap: "12px",
                    marginBottom: "30px",
                    alignItems: "flex-end",
                }}
                >
                    {/* Tipo de Sala */}
                    <div style={{ display: "flex", flexDirection: "column" }}>
                        <label>Tipo de sala</label>
                        <div style={{ position: "relative" }}>
                        <select
                            value={tipoSala}
                            onChange={(e) => setTipoSala(e.target.value)}
                            style={{ ...selectorStyle, paddingRight: "30px" }}
                        >
                            <option value="Reunião">Reunião</option>
                            <option value="Auditório">Auditório</option>
                        </select>
                        <span
                            style={{
                            position: "absolute",
                            right: "10px",
                            top: "55%",
                            transform: "translateY(-50%)",
                            pointerEvents: "none",
                            fontSize: "11px",
                            color: "#666"
                            }}
                        >
                            ▼
                        </span>
                        </div>
                    </div>

                    {/* Data */}
                    <div style={{ display: "flex", flexDirection: "column" }}>
                        <label>Data</label>
                        <input
                        name="data"
                        type="date"
                        value={data}
                        onChange={(e) => setData(e.target.value)}
                        style={inputStyle}
                        />
                    </div>

                    {/* Hora Início */}
                    <div style={{ display: "flex", flexDirection: "column" }}>
                        <label>Hora Início</label>
                        <input
                        type="time"
                        value={horaInicio}
                        onChange={(e) => setHoraInicio(e.target.value)}
                        style={inputStyle}
                        />
                    </div>

                    {/* Hora Fim */}
                    <div style={{ display: "flex", flexDirection: "column" }}>
                        <label>Hora Fim</label>
                        <input
                        type="time"
                        value={horaFim}
                        onChange={(e) => setHoraFim(e.target.value)}
                        style={inputStyle}
                        />
                    </div>

                    {/* Equipamentos */}
                    <div style={{ display: "flex", flexDirection: "column", position: "relative", minWidth: "250px" }}>
                        <label>Equipamentos</label>
                        <div style={{ position: "relative", width: "100%", minWidth: "250px" }}>
                        <button
                            type="button"
                            onClick={() => setShowEquipamentosDropdown((prev) => !prev)}
                            style={{ ...selectorStyle, width: "100%", paddingRight: "30px" }}
                        >
                            {equipamentosSelecionados.length > 0
                            ? `${equipamentosSelecionados.length} selecionado${equipamentosSelecionados.length > 1 ? 's' : ''}`
                            : "Selecione"}
                        </button>
                        <span
                            style={{
                            position: "absolute",
                            right: "12px",
                            top: "55%",
                            transform: "translateY(-50%)",
                            pointerEvents: "none",
                            fontSize: "11px",
                            color: "#555",
                            }}
                        >
                            ▼
                        </span>
                        </div>

                        {showEquipamentosDropdown && (
                        <div
                            style={{
                            position: "absolute",
                            zIndex: 10,
                            top: "100%",
                            left: 0,
                            backgroundColor: "#fff",
                            border: "1px solid #ccc",
                            padding: "10px",
                            width: "100%",
                            maxHeight: "200px",
                            overflowY: "auto",
                            }}
                        >
                            {EQUIPAMENTOS.map((equipamento) => (
                            <label key={equipamento} style={{ display: "block", marginBottom: "5px" }}>
                                <input
                                type="checkbox"
                                checked={equipamentosSelecionados.includes(equipamento)}
                                onChange={() => {
                                    setEquipamentosSelecionados((prev) =>
                                    prev.includes(equipamento)
                                        ? prev.filter((e) => e !== equipamento)
                                        : [...prev, equipamento]
                                    );
                                }}
                                />
                                {" "}{equipamento}
                            </label>
                            ))}
                        </div>
                        )}
                    </div>
                        
                    {/* Botão Procurar */}
                    <button
                    onClick={handleProcurarSalas}
                    style={{
                        padding: "10px 20px",
                        backgroundColor: "#6c47ff",
                        color: "white",
                        fontWeight: "bold",
                        border: "none",
                        borderRadius: "6px",
                        fontSize: "16px",
                        height: "42px"
                    }}
                    >
                        Procurar
                    </button>
                </div>
                
                <h1>Salas Disponíveis</h1>

                <div style={{ marginTop: "30px" }}>
                    {buscaFeita && salasFiltradas.length === 0 ? (
                        <div style={{
                            display: "flex",
                            flexDirection: "column",
                            alignItems: "center",
                            justifyContent: "center",
                            marginTop: "50px",
                            color: "#789",
                        }}>
                            <p style={{
                                maxWidth: "400px",
                                textAlign: "center",
                                fontSize: "16px",
                                lineHeight: "1.5",
                            }}>
                                Não temos sala disponível que atenda às condições.
                                Tente remover alguns filtros ou procure em outras datas e horários.
                            </p>
                        </div>
                    ) : (
                        salasFiltradas.map((sala) => (
                            <SalaCard
                                key={sala.id}
                                sala={sala}
                                onReservar={() => handleReserva(sala.id)}
                            />
                        ))
                    )}
                </div>
            </div>
        </div>
    );
};

export default Reservar;
