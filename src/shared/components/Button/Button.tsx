import React from "react";
import styles from "./Button.module.css"; // Corrigido o nome do arquivo

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger';
  children: React.ReactNode;
}

const Button: React.FC<ButtonProps> = ({ 
  variant = 'primary', 
  className, 
  children, 
  ...props 
}) => {
  const buttonClassName = `${styles.button} ${styles[variant]} ${className || ''}`.trim();

  return (
    <button 
      className={buttonClassName}
      {...props}
    >
      {children}
    </button>
  );
};

export default Button;