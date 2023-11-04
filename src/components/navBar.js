import Link from "next/link";

export default function NavBar() {
  return (
    <nav class="fixed top-0 left-0 right-0 z-10 flex items-center justify-between p-6 md:flex-row md:justify-start md:space-x-6 bg-transparent">
      <h1 class="text-white text-3xl font-serif">dAIly digest</h1>
      <div class="md:hidden">
        <button class="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 hover:bg-accent hover:text-accent-foreground h-10 px-4 py-2 text-white">
          Menu
        </button>
      </div>
      <div class="hidden md:block space-x-4">
        <Link class="text-gray-400 hover:text-white" href={"/"}>
          Home
        </Link>
        <Link class="text-gray-400 hover:text-white" href={"/"}>
          About
        </Link>
        <Link class="text-gray-400 hover:text-white" href={"/"}>
          Contact
        </Link>
      </div>
    </nav>
  );
}
