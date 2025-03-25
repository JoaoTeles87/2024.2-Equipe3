import React from "react";

type ConfirmacaoPopupProps = {
    mensagem: string;
    onCancel: () => void;
    onConfirm: () => void;
    textoCancelar?: string;
    textoConfirmar?: string;
};

const ConfirmacaoPopup: React.FC<ConfirmacaoPopupProps> = ({
    mensagem,
    onCancel,
    onConfirm,
    textoCancelar = "Cancelar",
    textoConfirmar = "Confirmar",
}) => {
    return (
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
            zIndex: 1000,
        }}>
            <div style={{
                backgroundColor: "white",
                padding: "20px",
                borderRadius: "8px",
                textAlign: "center",
            }}>
                <p style={{ marginBottom: "20px", fontSize: "18px" }}>{mensagem}</p>
                <div style={{ display: "flex", justifyContent: "center", gap: "10px" }}>
                    <button
                        onClick={onCancel}
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
                        {textoCancelar}
                    </button>
                    <button
                        onClick={onConfirm}
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
                        {textoConfirmar}
                    </button>
                </div>
            </div>
        </div>
    );
};

export default ConfirmacaoPopup;