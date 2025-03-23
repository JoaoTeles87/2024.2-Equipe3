import React from "react";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
    children: React.ReactNode;
}

const Button: React.FC<ButtonProps> = ({ children, ...props }) => {
    return (
        <button 
            style={{
                padding: "10px 20px",
                fontSize: "16px",
                backgroundColor: props.disabled ? "#ccc" : "#007bff",
                color: "#fff",
                border: "none",
                borderRadius: "5px",
                cursor: props.disabled ? "not-allowed" : "pointer",
                transition: "background 0.3s",
                fontWeight: "bold",
            }}
            {...props}
        >
            {children}
        </button>
    );
};

export default Button;