import React, { Component } from "react";
import axios from "axios";
import qs from "qs";
import Button from "@material-ui/core/Button";
import { storage } from "./firebase";
import "./App.css";
import Logo from './assets/logo.png';

class App extends Component {

  constructor(props) {
    super(props);
    this.state = {
      isLoggedIn: false,
      user: null,
      image: null
    };
    this.handleChange = this.handleChange.bind(this);
    this.upload = this.upload.bind(this);
    this.setURL= this.setURL.bind(this);
    this.imageURL = 'https://www.escj.org/sites/default/files/default_images/noImageUploaded.png';
    this.playlistIDs = [];
    this.recommendations = [];
    this.uploaded = false;


  }

  setURL(url) {
      this.imageURL = url;
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
            axios.post(`/create_playlist`, {
              image_url: url, // TODO: Pass in selected playlists
              playlists: ["dummy"],
            }).then(res =>
              {this.recommendations = res.json}
            );
            console.log(url);

            this.setURL(url);

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
      this.uploaded = true;
    }
  }

  async componentDidMount() {
    // TODO: Replace localhost with Firebase hosted site URL
    // this.get_all_playlists_ids();
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
    let logo = <img src={Logo} alt='website logo' className="logo topleft"/>;
    let message;
    let recs;

    if (this.state.isLoggedIn) {
      if (this.user == null) {
        message = <p className = "message">Welcome Test!</p>;
      } else {
        message = <p className = "message">Welcome {this.state.user.display_name}!</p>;
      }

      if (this.uploaded) {
        recs = <div className="grey padding"> <p className = "instructions">Your Recommendations</p>
        <p className = "small">{this.recommendations}</p> </div>
      }


      upload = (

        <span>
        <div className="grey padding">
        <p className = "instructions">Please upload a picture to hear what it sounds like.</p>
          <input type="file" style={{"margin": "10px 5px"}} onChange={this.handleChange} />
          <Button style={{background: "white", "border-radius": "8px", color: "black", "font-family": "sans-serif",

          "font-size": "40px", top:"0px", "margin-bottom": "20px", "margin-right": "5px", "margin-left": "5px", "border": "2px solid black"}} onClick={this.upload}>Upload</Button>

        </div>



        <img src={this.imageURL} alt='image' className="image bottomright"/>;
        </span>
      );

      link = <Button style={{background: "white", "border-radius": "8px", color: "black", "font-family": "sans-serif",

      "font-size": "10px", "bottom": "0px"}} onClick={this.logout}>Logout</Button>;
    } else {
      message = <p className = "message">What does your picture sing?</p>;
      link = <Button style={{background: "white", "border-radius": "8px", color: "black", "font-family": "sans-serif",
      "font-size": "40px", top:"0px", bottom: "0px"}} onClick={this.login}>Login to Spotify♩</Button>;
    }


    return (
      <div className="background">
            <header className="App-header center">
              {logo}
              {message}
              {upload}
              {recs}
              {link}
            </header>
      </div>

    );
  }
}

export default App;
