import { BaseSyntheticEvent, useState } from "react";
import { Accordion } from "react-bootstrap";
import { StarFill, Clipboard2Fill } from "react-bootstrap-icons";
import HighlightedText from "components/HighlightedText";
import { CopyToClipboard } from "helper";
import { useAlert } from "react-alert";

import "./Paper.scss";

export interface IPaper {
  id: number;
  title_ru?: string;
  authors_ru?: string;
  keywords_ru?: string;
  abstract_ru?: string;
  citation_ru?: string;
  page_ru?: string;
  title_en?: string;
  authors_en?: string;
  keywords_en?: string;
  abstract_en?: string;
  citation_en?: string;
  page_en?: string;
  citedcount: number;
  pdf?: string;
  year: number;
  rate: number;
  match?: number;
}

export default function Paper({
  paper,
  terms,
}: {
  paper: IPaper;
  terms: Array<string>;
}) {
  const alert = useAlert();
  const [loaded, setLoaded] = useState(false);

  const copyToClipboard = (event: BaseSyntheticEvent, lang: string) => {
    event.preventDefault();
    event.stopPropagation();
    let data = "";
    if (lang === "ru") {
      if (paper.citation_ru) {
        data = paper.citation_ru;
      } else {
        const title = paper.title_ru || paper.title_en;
        const authors = paper.authors_ru || paper.authors_en;
        data = `${title} (${authors})`;
      }
      const page = paper.page_ru || paper.page_en;
      data += `\n[${page}]`;
    } else {
      if (paper.citation_en) {
        data = paper.citation_en;
      } else {
        const title = paper.title_en || paper.title_ru;
        const authors = paper.authors_en || paper.authors_ru;
        data = `${title} (${authors})`;
      }
      const page = paper.page_en || paper.page_ru;
      data += `\n[${page}]`;
    }
    CopyToClipboard(data);
    alert.show("Info copied", { type: "success" });
  };

  const title = paper.title_ru || paper.title_en || "";
  const authors = paper.authors_ru || paper.authors_en || "";

  // Identificate importance
  let mark;
  if (paper.rate) {
    const stars = [];
    let color = "green";
    let title = "Published in the last 3 years";
    if (paper.rate === 2) {
      color = "orange";
      title = "Close to the current Hirsh-index";
    } else if (paper.rate === 3) {
      color = "red";
      title = "Has no citations";
    }

    for (let i = 0; i < paper.rate; i++) {
      stars.push(<StarFill key={i} color={color} />);
    }

    mark = (
      <span className="me-1" title={title}>
        {stars}
      </span>
    );
  }

  let infoRu;
  if (paper.title_ru) {
    infoRu = (
      <>
        <div className="field small bolder">Abstract</div>
        <HighlightedText text={paper.abstract_ru || ""} terms={terms} />
        <div className="field small bolder">Keywords</div>
        <HighlightedText text={paper.keywords_ru || ""} terms={terms} />
      </>
    );
  }

  let infoEn;
  if (paper.title_en) {
    infoEn = (
      <>
        {!!paper.title_ru && (
          <>
            <div className="field small bolder">Title</div>
            <HighlightedText text={paper.title_en || ""} terms={terms} />
            <div className="field small bolder">Authors</div>
            <HighlightedText text={paper.authors_en || ""} terms={terms} />
          </>
        )}
        <div className="field small bolder">Abstract</div>
        <HighlightedText text={paper.abstract_en || ""} terms={terms} />
        <div className="field small bolder">Keywords</div>
        <HighlightedText text={paper.keywords_en || ""} terms={terms} />
      </>
    );
  }

  let citationRu;
  if (paper.citation_ru) {
    citationRu = (
      <>
        <div className="field small bolder">Citation Ru</div>
        <div
          className="cursor-pointer"
          title="Copy to clipboard"
          onClick={event => copyToClipboard(event, "ru")}
        >
          <Clipboard2Fill color="cornflowerblue" className="me-1" />
          {paper.citation_ru}
        </div>
      </>
    );
  }

  let citationEn;
  if (paper.citation_en) {
    citationEn = (
      <>
        <div className="field small bolder">Citation En</div>
        <div
          className="cursor-pointer"
          title="Copy to clipboard"
          onClick={event => copyToClipboard(event, "en")}
        >
          <Clipboard2Fill color="cornflowerblue" className="me-1" />
          {paper.citation_en}
        </div>
      </>
    );
  }

  let pdf;
  if (paper.pdf) {
    const src = `/pdfjs/web/viewer.html?file=${process.env.REACT_APP_BACKEND}/pdf-co/${paper.id}`;

    pdf = (
      <>
        <div className="field small bolder">PDF Version</div>
        <div>
          <a
            href={paper.pdf}
            target="_blank"
            rel="noreferrer"
            title="Open in a new tab"
          >
            {paper.pdf}
          </a>
        </div>

        {loaded && (
          <iframe
            src={src}
            title={"" + paper.id}
            className="pdfpreview mt-4"
          ></iframe>
        )}
      </>
    );
  }

  return (
    <Accordion.Item key={paper.id} eventKey={"" + paper.id} className="paper">
      <Accordion.Header>
        <div className="w-100">
          <div className="float-end me-3 mt-2 cursor-pointer">
            {(!!citationRu || !!infoRu) && (
              <div
                className="cb-btn"
                title="Copy to clipboard"
                onClick={event => copyToClipboard(event, "ru")}
              >
                <Clipboard2Fill color="cornflowerblue" size={28} />
                <span>Ru</span>
              </div>
            )}

            {(!!citationEn || !!infoEn) && (
              <div
                className="cb-btn"
                title="Copy to clipboard"
                onClick={event => copyToClipboard(event, "en")}
              >
                <Clipboard2Fill color="cornflowerblue" size={28} />
                <span>En</span>
              </div>
            )}
          </div>

          <div>
            {paper.match}
            {mark}
            <HighlightedText text={title} terms={terms} />
          </div>
          <div className="small text-muted">{authors}</div>
        </div>
      </Accordion.Header>
      <Accordion.Body onEnter={() => setLoaded(true)}>
        {infoRu}
        {!!infoRu && !!infoEn && <hr />}
        {infoEn}
        <hr />
        {citationRu}
        {citationEn}
        {pdf}
      </Accordion.Body>
    </Accordion.Item>
  );
}
