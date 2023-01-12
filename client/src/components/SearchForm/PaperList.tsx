import { Accordion } from "react-bootstrap";
import Paper, { IPaper } from "./Paper";

export default function PaperList(
  papers: Array<IPaper> | undefined,
  terms: Array<string> | undefined
) {
  if (!papers) return;

  // Set rate
  for (const paper of papers) {
    if (paper.citedcount === 0) paper.rate = 3;
    else if (paper.citedcount >= 33 && paper.citedcount < 36)
      // H-index = 35
      paper.rate = 2;
    else if (paper.year >= 2020) paper.rate = 1;
    else paper.rate = 0;
  }

  // Sort papers by rate
  papers.sort((a, b) => b.rate - a.rate);

  // Create list of papers
  const list = papers.map(paper => (
    <Paper key={paper.id} paper={paper} terms={terms || []} />
  ));

  return (
    <>
      <div className="mb-2">
        Results{" "}
        {!!papers.length && (
          <span className="text-muted">({papers.length} papers)</span>
        )}
      </div>
      {!papers.length && <div>No papers found</div>}
      <Accordion alwaysOpen>{list}</Accordion>
    </>
  );
}
