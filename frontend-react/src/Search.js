import React, { useState } from "react";
import './index.css'

const Search = ({ search }) => {
  const [searchValue, setSearchValue] = useState("");

  const handleSearchInputChanges = e => {
    setSearchValue(e.target.value);
  };

  const resetInputField = () => {
    setSearchValue("");
  };

  const callSearchFunction = e => {
    e.preventDefault();
    search(searchValue);
    resetInputField();
  };

    return (
      <form className="form">
        <label className="label" htmlFor="query">Query on Movie, Year or Genre</label>
        <input className="input" type="text" name="query" value={searchValue}
                onChange={handleSearchInputChanges} placeholder="i.e. Jurassic Park, 1995 or Horror"/>
        <button className="button" onClick={callSearchFunction} type="submit">Search</button>
      </form>
    );
};

export default Search;