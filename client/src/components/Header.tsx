import { Nav } from "react-bootstrap";
import { Link } from "react-router-dom";

import "./Header.scss";

export default function Header() {
  return (
    <header>
      <Nav className="navbar navbar-dark bg-dark">
        <Link className="navbar-brand" to={"/"}>
          <img className="logo mx-3" src="logo.svg" alt="Logo" height={60} />
          <span className="title">
            Computer Optics <span className="sub">[Search]</span>
          </span>
        </Link>
      </Nav>
    </header>
  );
}
