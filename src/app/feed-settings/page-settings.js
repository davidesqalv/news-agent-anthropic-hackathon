"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { FiCopy } from "react-icons/fi";

function generateRandomId(length = 10) {
  const charset =
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
  let result = "";
  let crypto = window.crypto || window.msCrypto;
  let values = new Uint32Array(length);
  crypto.getRandomValues(values);
  values.forEach((value) => (result += charset[value % charset.length]));
  return result;
}

const containerVariants = {
  hidden: {
    opacity: 0,
  },
  visible: {
    opacity: 1,
    transition: {
      delay: 0.2,
    },
  },
};

const rssFeeds = [
  {
    name: "The New York Times",
    url: "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
    description:
      "Breaking news, multimedia, reviews & opinion on Washington, business, sports, movies, travel, books, jobs, education, real estate, cars & more.",
  },
  {
    name: "The Guardian",
    url: "https://www.theguardian.com/world/rss",
    description:
      "Latest news, sport, business, comment, analysis and reviews from the Guardian, the world's leading liberal voice.",
  },
  {
    name: "BBC News",
    url: "https://www.bbc.com/news/world/rss.xml",
    description:
      "Visit BBC News for up-to-the-minute news, breaking news, video, audio and feature stories. BBC News provides trusted World and UK news as well as local and regional perspectives. Also entertainment, business, science, technology and health news.",
  },
  {
    name: "Al Jazeera",
    url: "https://www.aljazeera.com/xml/rss/all.xml",
    description:
      "News, analysis from the Middle East & worldwide, multimedia & interactives, opinions, documentaries, podcasts, long reads and broadcast schedule.",
  },
  {
    name: "Reuters",
    url: "https://www.reuters.com/tools/rss",
    description:
      "Reuters.com brings you the latest news from around the world, covering breaking news in markets, business, politics, entertainment, technology, video and pictures.",
  },
];

export default function FeedSettingsClient() {
  const [selectedFeeds, setSelectedFeeds] = useState([]);
  const [randomEmail, setRandomEmail] = useState("");
  const [isCopied, setIsCopied] = useState(false);

  const handleFeedSelection = (feed) => {
    if (selectedFeeds.includes(feed)) {
      setSelectedFeeds(selectedFeeds.filter((f) => f !== feed));
    } else {
      setSelectedFeeds([...selectedFeeds, feed]);
    }
  };

  const generateRandomEmail = () => {
    const id = generateRandomId();
    setRandomEmail(`newsletter-${id}@example.com`);
  };

  const handleCopyEmail = () => {
    navigator.clipboard.writeText(randomEmail);
    setIsCopied(true);
    setTimeout(() => {
      setIsCopied(false);
    }, 2000);
  };

  const handleDone = () => {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ selectedFeeds, randomEmail }),
    };
    fetch("/api/subscribe", requestOptions)
      .then((response) => response.json())
      .then((data) => console.log(data));
  };

  useEffect(() => {
    generateRandomEmail();
  }, []);

  return (
    <motion.div
      className="w-full h-screen bg-black flex items-center justify-center flex-col space-y-6 animate-all"
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      <div className="flex flex-row w-full justify-center p-4">
        <div className="w-1/2 p-4">
          <h2 className="text-white text-2xl font-bold mb-4 font-serif">
            RSS Feeds
          </h2>
          <p className="text-white text-lg mb-2">
            Based on your preferences, here are some popular RSS feeds you may
            like. Select the ones you want to integrate into your AI digest.
          </p>
          <div className="space-y-2">
            {rssFeeds.slice(0, 5).map((feed) => (
              <button
                key={feed.url}
                className={`w-full py-2 px-4 rounded-md text-left ${
                  selectedFeeds.includes(feed.url)
                    ? "bg-gray-500 text-white"
                    : "bg-gray-200 text-gray-800"
                }`}
                onClick={() => handleFeedSelection(feed.url)}
              >
                <div className="flex flex-col">
                  <span className="text-lg font-bold">{feed.name}</span>
                  <span className="text-sm">{feed.description}</span>
                </div>
              </button>
            ))}
          </div>
        </div>
        <div className="w-1/2 p-4">
          <h2 className="text-white text-2xl font-bold mb-4 font-serif">
            Use a Random Email
          </h2>
          <p className="text-white text-lg mb-2">
            To integrate newsletters into your AI digest, please use the
            following email address for your subscriptions:
          </p>
          <div className="flex flex-row items-center space-x-2">
            <p
              className="text-white text-lg mt-2 cursor-pointer"
              onClick={handleCopyEmail}
            >
              Your new email is:{" "}
              <strong className="select-all">{randomEmail}</strong>
            </p>
            <FiCopy
              className="text-white text-lg cursor-pointer"
              onClick={handleCopyEmail}
            />
            {isCopied && <p className="text-green-500 text-sm ml-2">Copied!</p>}
          </div>
        </div>
      </div>
      <button
        className="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded"
        onClick={handleDone}
      >
        Done
      </button>
    </motion.div>
  );
}
