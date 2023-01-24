import { useState, useEffect, useCallback } from "react";
import { Form, Container, Row, Col } from "react-bootstrap";
import axios from "axios";
import Keywords from "./SearchForm/Keywords";
import PaperList from "./SearchForm/PaperList";
import { useNavigate, useLocation } from "react-router-dom";
import COSpinner from "./COSpinner";

let searchTimeout: any;
const cancelToken = axios.CancelToken;
let cancelTokenSource: any;

export default function SearchForm(pars: any) {
  const [data, setData] = useState({
    papers: undefined,
    terms: undefined,
    keywords: undefined,
  });

  const navigate = useNavigate();
  const type = window.location.pathname === "/" ? "co" : "scopus";

  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);

  const updateQuery = useCallback(
    (newQuery: string, immediate = false, newstate = true) => {
      setQuery(newQuery);
      if (query.trim() === newQuery.trim()) return;

      setData({
        papers: undefined,
        terms: undefined,
        keywords: undefined,
      });

      // Stop previous request
      if (searchTimeout) clearTimeout(searchTimeout);
      if (cancelTokenSource) cancelTokenSource.cancel();

      // Check empty string
      if (newQuery.length === 0) {
        setTimeout(() => {
          navigate({
            search: "",
          });
        }, 100);
        return;
      }

      // Check minimum length
      const terms = newQuery.split(",");
      let flagTermLength = false;
      for (const term of terms) {
        if (term.trim().length >= 3) {
          flagTermLength = true;
          break;
        }
      }
      if (!flagTermLength) return;

      const timeout = immediate ? 0 : 1000;
      setLoading(true);

      searchTimeout = setTimeout(() => {
        cancelTokenSource = cancelToken.source();

        // Update get-parameters
        if (newstate) {
          navigate({
            search: newQuery ? `?query=${newQuery}` : "",
          });
        }

        axios
          .post(
            `${process.env.REACT_APP_BACKEND}/search-${type}`,
            { query: newQuery },
            {
              cancelToken: cancelTokenSource.token,
            },
          )
          .then(resp => {
            setData(resp.data);
          })
          .catch(function (error) {
            error.handleGlobally && error.handleGlobally();
          })
          .finally(() => {
            setLoading(false);
          });
      }, timeout);
    },
    [query, type, navigate],
  );

  // Handle history change
  let location = useLocation();
  // NOTE: do not add updateQuery as dependency!
  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const getQuery = urlParams.get("query") || "";

    updateQuery(getQuery, true, false);
    // eslint-disable-next-line
  }, [location]);

  return (
    <div className="search-form mt-4">
      <Container>
        <form onSubmit={e => e.preventDefault()}>
          <Form.Control
            type="text"
            value={query}
            onChange={event => updateQuery(event.target.value)}
            id="inputTerm"
            placeholder="Place your terms here..."
          />
        </form>
      </Container>

      <Container className="mt-3 px-md-2 px-xl-4" fluid>
        {loading && (
          <div className="d-flex justify-content-center">
            <COSpinner />
          </div>
        )}

        {!loading && (
          <Row className="m-0 flex-wrap-reverse justify-content-around">
            <Col sm={12} lg={8} xxl={9}>
              {PaperList(data.papers, data.terms, type)}
            </Col>

            {type === "co" && (
              <Col className="mb-2">
                {Keywords(data.keywords, data.terms || [], updateQuery)}
              </Col>
            )}
          </Row>
        )}
      </Container>
    </div>
  );
}
