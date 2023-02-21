import { useState } from "react";
import { Accordion, Container } from "react-bootstrap";
import { useLocation } from "react-router-dom";

import "./SearchInfo.scss"

export default function SearchInfo() {
  const location = useLocation();
  const brand = location.pathname === "/" ? "Computer Optics" : "Scopus";

  return (
    <div className="info">
      <Container>
        <h1 className="display-6">
          <span className="brand">{brand} DB</span>
        </h1>
        <Accordion flush>
          <Accordion.Item eventKey="0">
            <Accordion.Header className="d-md-none"># Search info</Accordion.Header>
            <Accordion.Body>
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
              {
                location.pathname === "/" &&
                (<div>Use an exclamation mark ("!") in your query for a global search.</div>)
              }
            </Accordion.Body>
          </Accordion.Item>
        </Accordion>
      </Container>
    </div>
  );
}
