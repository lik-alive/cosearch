import { Container, Col, Row } from "react-bootstrap";

import "./Footer.scss";

export default function Footer() {
  const year = new Date().getFullYear();
  return (
    <footer className="text-white py-2">
      <Container>
        <Row>
          <Col sm={12} md={10}>Computer Optics Search 2023-{year}</Col>
          <Col className="text-end">©LIK</Col>
        </Row>
      </Container>
    </footer>
  );
}
