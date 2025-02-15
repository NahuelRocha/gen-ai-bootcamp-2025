import { Link, useLocation } from 'react-router-dom';
import { cn } from "@/lib/utils";
import { NAV_ITEMS } from '@/utils/routes';


export const Sidebar = () => {
  const location = useLocation();

  return (
    <aside className="w-64 border-r h-[calc(100vh-4rem)] p-4">
      <nav className="space-y-2">
        {NAV_ITEMS.map((item) => (
          <Link
            key={item.path}
            to={item.path}
            className={cn(
              "flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors",
              location.pathname === item.path
                ? "bg-primary text-primary-foreground"
                : "hover:bg-muted"
            )}
          >
            <span>{item.icon}</span>
            {item.title}
          </Link>
        ))}
      </nav>
    </aside>
  );
};
