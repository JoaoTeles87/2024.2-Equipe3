// src/shared/components/Input.tsx
import React from "react";

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
    onValueChange: (value: string) => void;
}

const Input: React.FC<InputProps> = ({ onValueChange, ...props }) => {
    return (
        <input
            {...props}
            onChange={(e) => onValueChange(e.target.value)}
            style={{
                width: "100%",
                padding: "10px",
                marginBottom: "10px",
                border: "1px solid #ccc",
                borderRadius: "5px",
                fontSize: "16px",
            }}
        />
    );
};

export default Input;
