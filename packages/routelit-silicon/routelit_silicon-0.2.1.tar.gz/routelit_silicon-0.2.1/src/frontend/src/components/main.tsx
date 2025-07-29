function Main({ children, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return <main {...props}>{children}</main>;
}

export default Main;
