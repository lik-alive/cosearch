import { Nav, Navbar, Container } from "react-bootstrap";
import { NavLink, useLocation } from "react-router-dom";

import "./Header.scss";

export default function Header() {
  const { search } = useLocation();

  return (
    <header>
      <Navbar collapseOnSelect expand="sm" bg="dark" variant="dark">
        <Container>
          <Navbar.Brand href="/">
            <img className="logo mx-3" src="logo.svg" alt="Logo" height={50} />
            {/* Mobile */}
            <span className="title d-sm-none">
              COptics <span className="sub">[Search]</span>
            </span>
            {/* Desktop */}
            <span className="title d-none d-sm-block">
              Computer Optics <span className="sub">[Search]</span>
            </span>
          </Navbar.Brand>
          <Navbar.Toggle aria-controls="responsive-navbar-nav" />
          <Navbar.Collapse id="responsive-navbar-nav">
            <Nav defaultActiveKey="/" className="me-auto">
              <NavLink className="nav-link" to={`/${search}`}>
                Home
              </NavLink>
              <NavLink className="nav-link" to={`/scopus${search}`}>
                Scopus
              </NavLink>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
    </header>
  );
}
