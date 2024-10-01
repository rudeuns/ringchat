"use client";

import { useState } from "react";
import { HiOutlineStar, HiStar } from "react-icons/hi2";

interface RatingProps {
  onClick: (rating: number) => void;
}

export default function Rating(props: RatingProps) {
  const [currentRating, setCurrentRating] = useState<number>(0);
  const [hoverRating, setHoverRating] = useState<number>(0);
  const maxRating = 5;

  const handleClickRating = (rating: number) => {
    setCurrentRating(rating);
    props.onClick(rating);
  };

  return (
    <div className="flex-row flex-center absolute left-full top-1/2 -translate-y-1/2 space-x-1 ms-2 p-2 bg-muted rounded-full shadow-md">
      {Array.from({ length: maxRating }, (_, index) => index + 1).map(
        (rating) => (
          <div
            key={rating}
            onClick={() => handleClickRating(rating)}
            onMouseEnter={() => setHoverRating(rating)}
            onMouseLeave={() => setHoverRating(0)}
            className="flex flex-center"
          >
            {rating <= (hoverRating || currentRating) ? (
              <HiStar className="icon-base size-6 text-yellow" />
            ) : (
              <HiOutlineStar className="icon-base size-6 text-yellow" />
            )}
          </div>
        ),
      )}
    </div>
  );
}
