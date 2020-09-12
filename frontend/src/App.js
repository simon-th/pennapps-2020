import React from "react";
import axios from "axios";
import "./App.css";

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      isLoggedIn: false,
    };
  }

  async login() {
    window.location.replace("http://localhost:5000/login");
  }

  async logout() {
    window.location.replace("http://localhost:5000/logout");
  }

  async componentDidMount() {
    // this.login();
    const params = new URLSearchParams(
      window.location.href.replace("http://localhost:3000/?", "")
    );
    if (params.has("login")) {
      await axios
        .get("/get_user")
        .then(async (result) => {
          console.log(result.data);
          await this.setState({
            isLoggedIn: true,
            user: result.data,
          });
        })
        .catch((err) => {
          console.error(err);
        });
    } else if (params.has("logout")) {
      await this.setState({
        isLoggedIn: false,
      });
    }
  }

  render() {
    let link;
    let welcome;
    if (this.state.isLoggedIn) {
      welcome = <p>Welcome {this.state.user.display_name}!</p>;
      link = <p onClick={this.logout}>Logout</p>;
    } else {
      link = <p onClick={this.login}>Login</p>;
    }

    return (
      <div className="App">
        <header className="App-header">
          {welcome}
          {link}
        </header>
      </div>
    );
  }
}

export default App;
