import HomeClient from "./page-client";

export const metadata = {
  title: "Daily Digest Onboarding",
  description: "A daily digest of the news you care about.",
};

export default function Home() {
  return <HomeClient />;
}
