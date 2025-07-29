import { useState, type PropsWithChildren } from "react";

interface SidebarProps extends React.HTMLAttributes<HTMLDivElement> {
  defaultOpen?: boolean;
}

interface ToggleButtonProps {
  isOpen: boolean;
  toggle: () => void;
}

function ToggleButton({ isOpen, toggle }: ToggleButtonProps) {
  return (
    <button className="sidebar-toggle" onClick={toggle}>
      {isOpen ? "x" : ">"}
    </button>
  );
}

function Sidebar({ defaultOpen, children, className, ...props }: PropsWithChildren<SidebarProps>) {
  const [isOpen, setIsOpen] = useState(defaultOpen || false);
  return (
    <aside className={className} {...props}>
      <div className={`content ${isOpen ? "" : "hidden"}`}>
        {children}
      </div>
      <ToggleButton isOpen={isOpen} toggle={() => setIsOpen(!isOpen)} />
    </aside>
  );
}

export default Sidebar;
