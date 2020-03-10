import React, { useState, useEffect } from "react";
import "./App.css";

function App() {
  const [products, setProducts] = useState([]);
  fetch("http://localhost:5000/product").then(res => console.log(res));
  return <div className="App"></div>;
}

export default App;
