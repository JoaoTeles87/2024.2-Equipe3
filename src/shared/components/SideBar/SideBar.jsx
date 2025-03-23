// components/Sidebar.jsx
import { Link, useLocation } from 'react-router-dom';
import styles from './Sidebar.module.css';

const Sidebar = () => {
  const location = useLocation();

  // Configuração dos itens do menu
  const menuItems = [
    { type: 'link', path: '/perfil', label: '‣ Perfil' },
    { type: 'title', label: 'Atividades' },
    { type: 'link', path: '/reservar', label: '‣ Reservar' },
    { type: 'link', path: '/avaliacoes', label: '‣ Avaliações' },
    { type: 'title', label: 'Solicitações' },
    { type: 'link', path: '/recursos', label: '‣ Recursos' },
    { type: 'link', path: '/manutencoes', label: '‣ Manutenções' },
  ];

  return (
    <nav className={styles.sidebar}>
      <h2 className={styles.title}>SAGAA</h2>
      <ul className={styles.menu}>
        {menuItems.map((item, index) => (
          item.type === 'title' ? (
            // Renderiza título da seção
            <li key={index} className={styles.sectionTitle}>
              <h6>{item.label}</h6>
            </li>
          ) : (
            // Renderiza item clicável
            <li
              key={item.path}
              className={`${styles.menuItem} ${
                location.pathname === item.path ? styles.active : ''
              }`}
            >
              <Link to={item.path} className={styles.link}>
                {item.label}
              </Link>
            </li>
          )
        ))}
      </ul>
    </nav>
  );
};

export default Sidebar;