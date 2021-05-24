import React from "react";
import './index.css'

const DEFAULT_PLACEHOLDER_IMAGE =
  "https://karlkwin.files.wordpress.com/2017/08/movie-reel.jpeg?w=1094";

const Movie = ({ movie }) => {
  const poster = DEFAULT_PLACEHOLDER_IMAGE;
  return (
    <div className="card">
      <h2>{movie.title}</h2>
      <div>
        <img
          width="200"
          alt={`The movie titled: ${movie.title}`}
          src={poster}
        />
      </div>
      <p>({movie.year})</p>
      <p>({movie.genres})</p>
    </div>
  );
};

export default Movie;
