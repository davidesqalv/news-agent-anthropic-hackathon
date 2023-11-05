import Link from "next/link";

const links = [
  { href: "/", label: "Home" },
  { href: "/schedule", label: "Schedule" },
  { href: "/personalize", label: "Personalize" },
  { href: "/feed-settings", label: "Settings" },
];

export default function NavBar() {
  return (
    <nav className="fixed top-0 left-0 right-0 z-10 flex items-center justify-between p-6 md:flex-row md:justify-between md:space-x-6 bg-transparent">
      <h1 className="text-white text-3xl font-serif">RituAI</h1>
      <div className="md:hidden">
        <button className="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 hover:bg-accent hover:text-accent-foreground h-10 px-4 py-2 text-white">
          Menu
        </button>
      </div>
      <div className="hidden md:flex space-x-4 ml-auto">
        {links.map(({ href, label }) => (
          <Link
            key={`${href}${label}`}
            href={href}
            className="text-gray-400 hover:text-white"
          >
            {label}
          </Link>
        ))}
      </div>
    </nav>
  );
}
