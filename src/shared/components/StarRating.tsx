import React from "react";
import styles from "./StarRating.module.css";

interface StarRatingProps {
  rating: number; 
  onRatingChange?: (value: number) => void;
  editable?: boolean;
}

const StarRating: React.FC<StarRatingProps> = ({ rating, onRatingChange, editable = false }) => {
  const handleClick = (index: number) => {
    if (!editable || !onRatingChange) return;
    onRatingChange(index);
  };

  return (
    <div className={styles.starContainer}>
      {[1, 2, 3, 4, 5].map((index) => (
        <span
          key={index}
          className={`${styles.star} ${index <= rating ? styles.filled : ""} ${editable ? styles.editable : ""}`}
          onClick={() => handleClick(index)}
        >
          ★
        </span>
      ))}
    </div>
  );
};

export default StarRating;
