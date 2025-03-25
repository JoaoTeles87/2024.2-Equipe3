import { useState } from "react";
import styles from "./StarRating.module.css";

interface StarRatingProps {
  rating: number;
  editable?: boolean;
  onRatingChange?: (rating: number) => void;
}

const StarRating: React.FC<StarRatingProps> = ({ rating, editable = true, onRatingChange }) => {
  const [hovered, setHovered] = useState<number | null>(null);

  const handleClick = (value: number) => {
    if (editable && onRatingChange) {
      onRatingChange(value);
    }
  };

  return (
    <div className={styles.starContainer}>
      {[1, 2, 3, 4, 5].map((starValue) => (
        <span
        key={starValue}
        data-testid={`star-${starValue}`}
        className={`${styles.star} ${starValue <= (hovered ?? rating) ? styles.filledStar : styles.emptyStar}`}
        onMouseEnter={() => editable && setHovered(starValue)}
        onMouseLeave={() => editable && setHovered(null)}
        onClick={() => handleClick(starValue)}
      >
        ★
      </span>
      ))}
    </div>
  );
};

export default StarRating;
