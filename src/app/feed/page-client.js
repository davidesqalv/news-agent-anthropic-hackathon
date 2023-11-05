"use client";

import { motion } from "framer-motion";
import Image from "next/image";
import { useState } from "react";
import { FaArrowUp, FaArrowDown } from "react-icons/fa";

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

const articles = [
  {
    title: "Article 1",
    description: "Description for article 1",
    link: "https://example.com/article1",
  },
  {
    title: "Article 2",
    description: "Description for article 2",
    link: "https://example.com/article2",
  },
  {
    title: "Article 3",
    description: "Description for article 3",
    link: "https://example.com/article3",
  },
];

export default function FeedClient() {
  const [votes, setVotes] = useState(articles.map(() => 0));
  const [images, setImages] = useState(articles.map(() => ""));

  const handleVote = (index, value) => {
    const newVotes = [...votes];
    newVotes[index] += value;
    setVotes(newVotes);
  };

  const handleImageLoad = (index, src) => {
    const newImages = [...images];
    newImages[index] = src;
    setImages(newImages);
  };

  return (
    <motion.div
      className="w-full h-screen bg-black flex flex-col items-center justify-center space-y-6 animate-all"
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      <h1 className="text-3xl font-bold text-white font-serif">News Feed</h1>
      <div className="grid grid-cols-1 gap-4 w-full max-w-6xl">
        {articles.map((article, index) => (
          <div
            key={index}
            className="bg-gray-800 rounded-lg overflow-hidden shadow-md flex flex-row items-center space-x-4 p-4"
          >
            <div className="relative h-16 w-16">
              {images[index] ? (
                <Image
                  src={images[index]}
                  alt={article.title}
                  layout="fill"
                  objectFit="cover"
                />
              ) : (
                <img
                  src="https://via.placeholder.com/200x300.png?text=Loading..."
                  alt="Loading..."
                  className="w-full h-full object-cover"
                />
              )}
              <img
                src={article.link + "/og-image.jpg"}
                alt={article.title}
                className="hidden"
                onLoad={() =>
                  handleImageLoad(index, article.link + "/og-image.jpg")
                }
              />
            </div>
            <div className="flex flex-col w-full">
              <a href={article.link} target="_blank" rel="noopener noreferrer">
                <h2 className="text-lg font-bold text-white font-serif">
                  {article.title}
                </h2>
              </a>
              <a href={article.link} target="_blank" rel="noopener noreferrer">
                <p className="text-gray-400">{article.description}</p>
              </a>
              <div className="flex justify-between items-center mt-4">
                <div className="flex space-x-2">
                  <button
                    className="text-gray-500 hover:text-gray-400"
                    onClick={() => handleVote(index, 1)}
                  >
                    <FaArrowUp />
                  </button>
                  <button
                    className="text-gray-500 hover:text-gray-400"
                    onClick={() => handleVote(index, -1)}
                  >
                    <FaArrowDown />
                  </button>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </motion.div>
  );
}
