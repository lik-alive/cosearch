// import InfoIcon from './icons/InfoIcon'
// import SuccessIcon from './icons/SuccessIcon'
// import ErrorIcon from './icons/ErrorIcon'
// import CloseIcon from './icons/CloseIcon'

import { InfoCircle, CheckCircle, XCircle } from "react-bootstrap-icons";

const alertStyle = {
  backgroundColor: "#001a3a",
  color: "white",
  padding: "10px",
  borderRadius: "3px",
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
  boxShadow: "0px 2px 2px 2px rgba(0, 0, 0, 0.03)",
  fontFamily: "Arial",
  width: "300px",
  boxSizing: "border-box",
  margin: "10px 30px",
};

const buttonStyle = {
  marginLeft: "20px",
  border: "none",
  backgroundColor: "transparent",
  cursor: "pointer",
  color: "#FFFFFF",
};

const AlertTemplate = ({
  message,
  options,
  style,
  close,
}: {
  message: any;
  options: any;
  style: any;
  close: any;
}) => {
  return (
    <div style={{ ...alertStyle, ...style }}>
      {options.type === "info" && <InfoCircle className="me-2" />}
      {options.type === "success" && <CheckCircle className="me-2" />}
      {options.type === "error" && <XCircle className="me-2" />}
      <span style={{ flex: 2 }}>{message}</span>
      <button onClick={close} style={buttonStyle}>
        <span aria-hidden="true">&times;</span>
      </button>
    </div>
  );
};

export default AlertTemplate;
