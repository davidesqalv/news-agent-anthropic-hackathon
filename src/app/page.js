import HomeClient from "./page-client";

export const metadata = {
  title: "RituAI",
  description: "An AI-curated daily digest of the news you care about.",
};

export default function Home() {
  return <HomeClient />;
}
