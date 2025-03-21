// src/shared/components/ErrorMessage.tsx
import React from "react";

interface ErrorMessageProps {
    message: string;
}

const ErrorMessage: React.FC<ErrorMessageProps> = ({ message }) => {
    return (
        <p style={{ color: "red", fontSize: "14px", marginBottom: "10px" }}>
            {message}
        </p>
    );
};

export default ErrorMessage;
