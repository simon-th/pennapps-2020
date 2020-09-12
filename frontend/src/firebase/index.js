import firebase from "firebase/app";
import "firebase/storage";
import config from "./config.json";

firebase.initializeApp(config);
const storage = firebase.storage();

export { storage, firebase as default };
