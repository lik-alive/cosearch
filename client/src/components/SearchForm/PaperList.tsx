import { Accordion } from "react-bootstrap";
import Paper, { IPaper } from "./Paper";
import PaperScopus, { IPaperScopus } from "./PaperScopus";

export default function PaperList(
  papers: Array<IPaper | IPaperScopus> | undefined,
  terms: Array<string> | undefined,
  type: string,
) {
  if (!papers) return;

  if (type === "co") {
    const copapers = papers as Array<IPaper>;

    // Set degree of match
    const fields = [
      "title_en",
      "abstract_en",
      "keywords_en",
      "title_ru",
      "abstract_ru",
      "keywords_ru",
    ];
    for (const paper of copapers) {
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
    for (const paper of copapers) {
      if (paper.citedcount === 0) paper.rate = 3;
      else if (paper.citedcount >= 30 && paper.citedcount < 36)
        // H-index = 35
        paper.rate = 2;
      else if (paper.year >= 2020) paper.rate = 1;
      else paper.rate = 0;
    }
    
    // Sort papers by rate
    copapers.sort((a, b) => {
      const aVal = (a.match || 0) * 10 + a.rate;
      const bVal = (b.match || 0) * 10 + b.rate;
      return bVal - aVal;
    });
  }

  // Create list of papers
  let list = [];
  if (type === "co") {
    list = (papers as Array<IPaper>).map(paper => (
      <Paper key={paper.id} paper={paper} terms={terms || []} />
    ));
  } else {
    list = (papers as Array<IPaperScopus>).map(paper => (
      <PaperScopus key={paper.id} paper={paper} terms={terms || []} />
    ));
  }

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
