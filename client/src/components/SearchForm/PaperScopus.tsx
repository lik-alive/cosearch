import { BaseSyntheticEvent, useState } from "react";
import { Accordion } from "react-bootstrap";
import { Clipboard2Fill } from "react-bootstrap-icons";
import HighlightedText from "components/HighlightedText";
import { CopyToClipboard } from "helper";
import { useAlert } from "react-alert";

import "./Paper.scss";
import { info } from "console";

export interface IPaperScopus {
  id: string;
  title_en: string;
  creator_en: string;
  source: string;
  year?: string;
  volume?: string;
  issue?: string;
  pages?: string;
  link?: string;
  citedcount: number;
}

export default function PaperScopus({
  paper,
  terms,
}: {
  paper: IPaperScopus;
  terms: Array<string>;
}) {
  const alert = useAlert();
  const [loaded, setLoaded] = useState(false);

  const sourceInfo = () => {
    let info = paper.source;
    if (paper.year) info += `, ${paper.year}`;
    if (paper.volume) info += `, Vol. ${paper.volume}`;
    if (paper.issue) info += `, Iss. ${paper.issue}`;
    if (paper.pages) info += `, P. ${paper.pages}`;

    return info;
  };

  const copyToClipboard = (event: BaseSyntheticEvent) => {
    event.preventDefault();
    event.stopPropagation();
    let data = `${paper.title_en} (${paper.creator_en} et al.)`;
    data += `\n${sourceInfo()}`;
    if (paper.link) data += `\n[${paper.link}]`;

    CopyToClipboard(data);
    alert.show("Info copied", { type: "success" });
  };

  return (
    <Accordion.Item key={paper.id} eventKey={"" + paper.id} className="paper">
      <Accordion.Header>
        <div className="w-100">
          <div className="float-end me-3 mt-2 cursor-pointer">
            <div
              className="cb-btn"
              title="Copy to clipboard English info"
              onClick={event => copyToClipboard(event)}
            >
              <Clipboard2Fill color="cornflowerblue" size={28} />
              <span>En</span>
            </div>
          </div>

          <div>
            <HighlightedText text={paper.title_en} terms={terms} />
          </div>
          <div className="small text-muted">{paper.creator_en}</div>
        </div>
      </Accordion.Header>
      <Accordion.Body onEnter={() => setLoaded(true)}>
        <>
          <div className="field small bolder">Source</div>
          <div>{sourceInfo()}</div>
          <div className="field small bolder">Cited count</div>
          <div>{paper.citedcount}</div>
          <div className="field small bolder">Link</div>
          <div>
            <a
              href={paper.link}
              target="_blank"
              rel="noreferrer"
              title="Open in a new tab"
            >
              {paper.link}
            </a>
          </div>
        </>
        <hr />
      </Accordion.Body>
    </Accordion.Item>
  );
}
