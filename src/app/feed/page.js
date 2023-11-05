import FeedClient from "./page-client";

export const metadata = {
  title: "RituAI Feed",
  description: "An AI-curated daily digest of the news you care about.",
};

export default function Feed() {
  return <FeedClient />;
}
