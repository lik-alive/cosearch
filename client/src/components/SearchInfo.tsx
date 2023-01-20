import { Container } from "react-bootstrap";
import { useLocation } from "react-router-dom";

export default function SearchInfo() {
  const location = useLocation();
  const brand = location.pathname === "/" ? "Computer Optics" : "Scopus";

  return (
    <div className="info">
      <Container>
        {/* <h1 className="display-6">Welcome, friend!</h1> */}
        <div>
          This page provides a handy service for smart paper search in{" "}
          <span className="brand">{brand}</span>.
        </div>
        <div>
          The search is case-insensitive and covers the following paper's
          meta-data: <span className="bolder">title</span>,{" "}
          <span className="bolder">abstract</span>,{" "}
          <span className="bolder">keywords</span>.
        </div>
        <div>
          Please specify <span className="bolder">one or more terms</span>{" "}
          (maximum 10) separated by comma in the form below. You can use both{" "}
          <span className="bolder">Russian</span> and{" "}
          <span className="bolder">English</span> language.
        </div>
      </Container>
    </div>
  );
}
