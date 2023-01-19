import { Accordion } from "react-bootstrap";
import Paper, { IPaper } from "./Paper";

export default function PaperList(
  papers: Array<IPaper> | undefined,
  terms: Array<string> | undefined,
) {
  if (!papers) return;

  // Set degree of match
  const fields = [
    "title_en",
    "abstract_en",
    "keywords_en",
    "title_ru",
    "abstract_ru",
    "keywords_ru",
  ];
  for (const paper of papers) {
    paper.match = 0;
    if (!terms) continue;

    for (const term of terms) {
      for (const field of fields) {
        const value = paper[field as keyof IPaper] || "";
        if (("" + value).includes(term)) {
          paper.match++;
          break;
        }
      }
    }
  }

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
  papers.sort((a, b) => {
    const aVal = (a.match || 0) * 10 + a.rate;
    const bVal = (b.match || 0) * 10 + b.rate;
    return bVal - aVal;
  });

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
