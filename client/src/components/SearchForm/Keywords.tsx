import { BaseSyntheticEvent } from "react";
import { Button } from "react-bootstrap";

export default function Keywords(
  keywords: Array<string> | undefined,
  terms: Array<string>,
  updateQuery: Function
) {
  if (!keywords) return;

  const handleClick = (event: BaseSyntheticEvent, keyword: string) => {
    updateQuery(keyword, true);
  };

  const list = keywords.map(keyword => (
    <Button
      variant="outline-secondary"
      size="sm"
      className={"m-1 " + (terms.includes(keyword) ? "active" : "")}
      key={keyword}
      onClick={event => handleClick(event, keyword)}
    >
      {keyword}
    </Button>
  ));

  return (
    <>
      <div className="sticky-top">
        <div className="mb-2">
          Tags{" "}
          {!!keywords.length && (
            <span className="text-muted">({keywords.length} keywords)</span>
          )}
        </div>
        {!keywords.length && <div>No keywords found</div>}
        <div>{list}</div>
      </div>
    </>
  );
}
