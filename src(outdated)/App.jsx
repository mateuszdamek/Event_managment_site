//import { useState } from "react";
import axios from "axios";
import React from "react";
import "./App.css";

class App extends React.Component {
  state = { details: [] };

  componentDidMount() {
    let data;
    axios
      .get("http://localhost:8000")
      .then((res) => {
        data = res.data;
        this.setState({
          details: data,
        });
      })
      .catch((err) => {});
  }

  render() {
    return (
      <div>
        <h1>Data from Django</h1>
        <hr></hr>
        {this.state.details.map((output, id) => (
          <div key={id}>
            <div>
              <h3>{output.user_ID}</h3>
              <h3>{output.username}</h3>
              <h3>{output.email}</h3>
              <h3>{output.role}</h3>
            </div>
          </div>
        ))}
      </div>
    );
  }
}

export default App;
