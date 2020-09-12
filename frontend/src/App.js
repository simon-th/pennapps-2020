import React, { Component } from "react";
import axios from "axios";
import Button from "@material-ui/core/Button";
import { storage } from "./firebase";
import "./App.css";

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isLoggedIn: false,
      user: null,
      image: null,
    };
    this.handleChange = this.handleChange.bind(this);
    this.upload = this.upload.bind(this);
  }

  async login() {
    window.location.replace("http://localhost:5000/login");
  }

  async logout() {
    window.location.replace("http://localhost:5000/logout");
  }

  async upload() {
    const uploadTask = storage
      .ref(`images/${this.state.image.name}`)
      .put(this.state.image);
    uploadTask.on(
      "state_changed",
      (snapshot) => {},
      (error) => {
        console.error(error);
      },
      () => {
        storage
          .ref("images")
          .child(this.state.image.name)
          .getDownloadURL()
          .then((url) => {
            console.log(url);
          });
      }
    );
  }

  async handleChange(event) {
    if (event.target.files[0]) {
      await this.setState({
        image: event.target.files[0],
      });
      console.log(this.state.image);
    }
  }

  async componentDidMount() {
    // TODO: Replace localhost with Firebase hosted site URL
    const params = new URLSearchParams(
      window.location.href.replace("http://localhost:3000/?", "")
    );
    if (params.has("login")) {
      await axios
        .get("/get_user")
        .then(async (result) => {
          console.log(result.data);
          this.setState({
            isLoggedIn: true,
            user: result.data,
          });
        })
        .catch((err) => {
          console.error(err);
        });
    } else if (params.has("logout")) {
      this.setState({
        isLoggedIn: false,
        user: null,
      });
    }
  }

  render() {
    let link;
    let welcome;
    let upload;

    if (this.state.isLoggedIn) {
      welcome = <p>Welcome {this.state.user.display_name}!</p>;
      upload = (
        <div>
          <input type="file" onChange={this.handleChange} />;
          <Button onClick={this.upload}>Upload</Button>;
        </div>
      );
      link = <Button onClick={this.logout}>Logout</Button>;
    } else {
      link = <Button onClick={this.login}>Login</Button>;
    }

    return (
      <div className="App">
        <header className="App-header">
          {welcome}
          {upload}
          {link}
        </header>
      </div>
    );
  }
}

export default App;
