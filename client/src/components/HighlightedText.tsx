import "./HighlightedText.scss";

interface IProps {
  text: string;
  terms: Array<string>;
}

export default function HighlightedText(props: IProps) {
  let res = props.text;
  for (const term of props.terms) {
    const regex = new RegExp(`(${term})`, "gi");
    res = res.replace(regex, `<span class='hl'>$1</span>`);
  }

  return (
    <>
      <span className="hl-text" dangerouslySetInnerHTML={{ __html: res }} />
    </>
  );
}
