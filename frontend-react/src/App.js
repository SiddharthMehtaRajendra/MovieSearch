import React, { useReducer, useEffect } from "react";
import "./App.css";
import Header from "./Header";
import Movie from "./Movie";
import spinner from "./ajax-loader.gif";
import Search from "./Search";

const MOVIE_API_URL = "/search_movies";

const initialState = {
  loading: true,
  movies: [],
  errorMessage: null
};

const reducer = (state, action) => {
  switch (action.type) {
    case "SEARCH_MOVIES_REQUEST":
      return {
        ...state,
        loading: true,
        errorMessage: null
      };
    case "SEARCH_MOVIES_SUCCESS":
      return {
        ...state,
        loading: false,
        movies: action.payload
      };
    case "SEARCH_MOVIES_FAILURE":
      return {
        ...state,
        loading: false,
        errorMessage: action.error
      };
    default:
      return state;
  }
};

const App = () => {
  const [state, dispatch] = useReducer(reducer, initialState);

  useEffect(() => {
    fetch('/list_top_rated')
      .then(response => response.json())
      .then(jsonResponse => {
        dispatch({
          type: "SEARCH_MOVIES_SUCCESS",
          payload: jsonResponse.result
        });
      });
  }, []);

  const refreshPage = () => {
    window.location.reload();
  };

  const search = searchValue => {

    dispatch({
      type: "SEARCH_MOVIES_REQUEST"
    });

    fetch(MOVIE_API_URL + '?query=' + searchValue)
      .then(response => response.json())
      .then(jsonResponse => {
        console.log(jsonResponse);
        if (jsonResponse) {
          dispatch({
            type: "SEARCH_MOVIES_SUCCESS",
            payload: jsonResponse.result
          });
        } else {
          dispatch({
            type: "SEARCH_MOVIES_FAILURE",
            error: jsonResponse.Error
          });
        }
      });
  };

  const ratings = [
    '0.5', '1.0', '1.5', '2.0', '2.5', '3.0', '3.5', '4.0', '4.5', '5.0'
  ];
  
  const defaultRating = ratings[5];

  const onHandleChange = (evt) => {
    fetch('/search_by_rating' + '?rating=' + evt.target.value)
      .then(response => response.json())
      .then(jsonResponse => {
        console.log(jsonResponse);
        if (jsonResponse) {
          dispatch({
            type: "SEARCH_MOVIES_SUCCESS",
            payload: jsonResponse.result
          });
        } else {
          dispatch({
            type: "SEARCH_MOVIES_FAILURE",
            error: jsonResponse.Error
          });
        }
      });
  };

  const { movies, errorMessage, loading } = state;
  const { selectedRating } = state;

  return (
    <div className="App">
      <Header text="MOVIE GROKKER" />
      <Search search={search} />
      <label className="rating-label">QUERY BY MOVIE RATING</label>
      <select value={selectedRating} onChange={onHandleChange}>
        {
          ratings.map((rating, index) => {
            if(rating == 5.0) return <option selected="selected" key={`rating${index}`} value={rating}>{rating}</option>
            else return <option key={`rating${index}`} value={rating}>{rating}</option>
          })
        }
      </select>
      <p className="App-intro">Here are your Movies!</p>
      <div className="movies">
        {loading && !errorMessage ? (
          <img className="spinner" src={spinner} alt="Loading spinner" />
        ) : errorMessage ? (
          <div className="errorMessage">{errorMessage}</div>
        ) : (
          movies.map((movie, index) => (
            <Movie key={`${index}-${movie.title}`} movie={movie} />
          ))
        )}
      </div>
    </div>
  );
};

export default App;