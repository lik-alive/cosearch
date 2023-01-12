import { Container, Col, Row } from "react-bootstrap";

import "./Footer.scss";

export default function Footer() {
  const year = new Date().getFullYear();
  return (
    <footer className="text-white py-2">
      <Container>
        <Row>
          <Col xs={9}>Computer Optics Search 2023-{year}</Col>
          <Col xs={3} className="text-end">©LIK</Col>
        </Row>
      </Container>
    </footer>
  );
}
