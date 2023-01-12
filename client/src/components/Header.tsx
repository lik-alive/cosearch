import { Nav } from "react-bootstrap";
import { Link } from "react-router-dom";

import "./Header.scss";

export default function Header() {
  return (
    <header>
      <Nav className="navbar navbar-dark bg-dark">
        <Link className="navbar-brand" to={"/"}>
          <img className="logo mx-3" src="logo.svg" alt="Logo" height={50} />
          {/* Mobile */}
          <span className="title d-sm-none">
            COptics <span className="sub">[Search]</span>
          </span>
          {/* Desktop */}
          <span className="title d-none d-sm-block">
            Computer Optics <span className="sub">[Search]</span>
          </span>
        </Link>
      </Nav>
    </header>
  );
}
