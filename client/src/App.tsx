import axios from "axios";
import { useAlert } from "react-alert";

import "./styles.scss";
import "bootstrap/dist/css/bootstrap.min.css";

// Do not change import order!
import Routes from "Routes";

export default function App() {
  const alert = useAlert();

  const errorComposer = (error: any) => {
    return () => {
      if (axios.isCancel(error)) {
        // console.log("Request canceled");
        return;
      }

      const statusCode = error.response?.status;
      if (statusCode === 401) {
        localStorage.setItem(
          "redirect",
          window.location.href.replace(window.location.origin, ""),
        );
        localStorage.removeItem("signed_in");
        window.location.href = "/login";
      } else {
        alert.show("Server error", { type: "error" });
      }
    };
  };

  axios.defaults.withCredentials = true;

  axios.interceptors.response.use(undefined, function (error) {
    error.handleGlobally = errorComposer(error);

    return Promise.reject(error);
  });

  return <Routes />;
}
