import { useState, useEffect, useCallback } from "react";
import { Form, Container, Row, Col } from "react-bootstrap";
import axios from "axios";
import Keywords from "./SearchForm/Keywords";
import PaperList from "./SearchForm/PaperList";
import { useAlert } from "react-alert";
import { useNavigate, useLocation } from "react-router-dom";
import COSpinner from "./COSpinner";

import "./SearchForm.scss";

let searchTimeout: any;
const cancelToken = axios.CancelToken;
let cancelTokenSource: any;

export default function SearchForm(pars: any) {
  const alert = useAlert();

  const [data, setData] = useState({
    papers: undefined,
    terms: undefined,
    keywords: undefined,
  });

  const navigate = useNavigate();

  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);

  const updateQuery = useCallback(
    (query: string, immediate = false, newstate = true) => {
      setData({
        papers: undefined,
        terms: undefined,
        keywords: undefined,
      });
      setQuery(query);

      // Update get-parameters
      if (newstate) {
        navigate({
          search: query ? `?query=${query}` : "",
        });
      }

      if (query.length < 3) return;

      if (searchTimeout) clearTimeout(searchTimeout);
      if (cancelTokenSource) cancelTokenSource.cancel();

      const timeout = immediate ? 0 : 1000;
      setLoading(true);

      searchTimeout = setTimeout(() => {
        cancelTokenSource = cancelToken.source();

        axios
          .post(
            `${process.env.REACT_APP_BACKEND}/search-co`,
            { query },
            {
              cancelToken: cancelTokenSource.token,
            }
          )
          .then(resp => {
            setData({ ...resp.data, query });
          })
          .catch(function (thrown) {
            if (axios.isCancel(thrown)) {
              // console.log("Request canceled");
            } else {
              alert.show("Server error", { type: "error" });
            }
          })
          .finally(() => {
            setLoading(false);
          });
      }, timeout);
    },
    [alert, navigate]
  );

  // Handle history change
  let location = useLocation();
  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const getQuery = urlParams.get("query") || "";

    if (getQuery !== query) {
      updateQuery(getQuery, true, false);
    }
  }, [location, query, updateQuery]);

  // window.addEventListener(
  //   "popstate",
  //   function (event) {
  //     const urlParams = new URLSearchParams(window.location.search);
  //     const getQuery = urlParams.get("query");

  //     if (getQuery !== query) {
  //       updateQuery(getQuery || "", true, false);
  //     }
  //   },
  //   { once: true }
  // );

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
          <Row className="m-0 flex-wrap-reverse">
            <Col sm={12} lg={8} xxl={9}>
              {PaperList(data.papers, data.terms)}
            </Col>

            <Col className="mb-2">
              {Keywords(data.keywords, data.terms || [], updateQuery)}
            </Col>
          </Row>
        )}
      </Container>
    </div>
  );
}
