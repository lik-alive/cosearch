import { useState } from "react";
import { useNavigate, Navigate } from "react-router-dom";
import { Button, Form, Card, Container, Row, Col } from "react-bootstrap";
import { useAlert } from "react-alert";
import axios from "axios";

import "./Login.scss";

export default function Login() {
  const [username, setUsername] = useState(process.env.NODE_ENV === 'development' ? "test" : "");
  const [password, setPassword] = useState(process.env.NODE_ENV === 'development' ? "123" : "");
  const [isLoading, setLoading] = useState(false);
  const navigate = useNavigate();
  const alert = useAlert();

  const onSubmit = async (e: any) => {
    e.preventDefault();

    setLoading(true);

    try {
      await axios.post(`${process.env.REACT_APP_BACKEND}/login`, {
        username,
        password,
      });
      localStorage.setItem("signed_in", "1");

      const href = localStorage.getItem("redirect") || "/";
      localStorage.removeItem("redirect");
      navigate(href);
    } catch (error) {
      alert.show("Server error", { type: "error" });
    } finally {
      setLoading(false);
    }
  };

  const isLoggedIn = localStorage.getItem("signed_in");

  return isLoggedIn ? (
    <Navigate to="/" replace />
  ) : (
    <>
      <div className="auth">
        <Container className="d-flex vh-100">
          <Row className="mx-auto">
            <Col>
              <Card
                className="text-center px-4 pt-4 pb-2"
                style={{ maxWidth: "300px" }}
              >
                <Card.Img src="logo.svg" height={50} />
                <Card.Body>
                  <Form onSubmit={e => onSubmit(e)}>
                    <Form.Control
                      className="mb-3"
                      type="text"
                      placeholder="Username"
                      value={username}
                      required
                      onChange={e => setUsername(e.target.value)}
                    />
                    <Form.Control
                      className="mb-3"
                      type="password"
                      placeholder="Password"
                      value={password}
                      required
                      onChange={e => setPassword(e.target.value)}
                    />
                    <div className="d-grid mt-4">
                      <Button
                        disabled={isLoading}
                        variant="primary"
                        type="submit"
                      >
                        Login
                      </Button>
                    </div>
                  </Form>
                </Card.Body>
              </Card>
            </Col>
          </Row>
        </Container>
      </div>
    </>
  );
}
