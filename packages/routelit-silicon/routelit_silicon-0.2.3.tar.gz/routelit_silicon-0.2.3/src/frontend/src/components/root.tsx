import { PropsWithChildren } from "react";

interface Props {
  className?: string;
}

function Root({ children, className = "" }: PropsWithChildren<Props>) {
  return <div className={"root "+className}>{children}</div>;
}

export default Root;
