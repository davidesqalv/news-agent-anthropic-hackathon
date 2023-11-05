"use client";

import { motion } from "framer-motion";
import Image from "next/image";
import { useState, useEffect } from "react";
import { FaArrowUp, FaArrowDown } from "react-icons/fa";

const containerVariants = {
  hidden: {
    opacity: 0,
  },
  visible: {
    opacity: 1,
    transition: {
      delay: 0.2,
      staggerChildren: 0.2, // add stagger effect
    },
  },
};

const articleVariants = {
  hidden: {
    opacity: 0,
    // y: 20,
  },
  visible: {
    opacity: 1,
    // y: 0,
  },
};

const articles = [
  {
    title: "Article 1",
    description: "Description for article 1",
    link: "https://www.reuters.com/world/middle-east/arab-world-us-split-gaza-ceasefire-israeli-offensive-presses-2023-11-05/",
  },
  {
    title: "Article 2",
    description: "Description for article 2",
    link: "https://www.nytimes.com/2023/11/04/us/politics/trump-desantis-florida.html",
  },
  {
    title: "Article 3",
    description: "Description for article 3",
    link: "https://www.bbc.co.uk/news/uk-england-devon-67311250",
  },
];

async function getArticleImage(articleUrl) {
  const apiKey = "pk_70fe81f7aea300606721c526258fd22558ca2738";
  const apiUrl = `https://jsonlink.io/api/extract?url=${articleUrl}&api_key=${apiKey}`;

  const response = await fetch(apiUrl);
  if (!response.ok) {
    throw new Error(`Error: ${response.status} - ${response.statusText}`);
  }
  const responseJson = await response.json();

  //   console.log(responseJson);
  return responseJson.images[0];
}

export default function FeedClient() {
  const [votes, setVotes] = useState(articles.map(() => 0));
  const [images, setImages] = useState(articles.map(() => ""));

  useEffect(() => {
    async function fetchImages() {
      const newImages = [];
      for (let i = 0; i < articles.length; i++) {
        const imageUrl = await getArticleImage(articles[i].link);
        newImages.push(imageUrl);
      }
      setImages(newImages);
    }
    fetchImages();
  }, []);

  useEffect(() => {
    console.log(images);
  }, [images]);

  const handleVote = (index, value) => {
    const newVotes = [...votes];
    newVotes[index] += value;
    setVotes(newVotes);
  };

  return (
    <motion.div
      className="w-full h-screen bg-black flex flex-col items-center justify-center space-y-6 animate-all"
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      <h1 className="text-3xl font-bold text-white font-serif">Feed</h1>

      <div className="grid grid-cols-1 gap-4 w-full max-w-6xl">
        <p className="text-white text-center">
          Here's your ritual AI curated feed. You can upvote or downvote
          articles to help us learn your preferences.
        </p>
        {articles.map((article, index) => (
          <motion.div // wrap article in motion.div
            key={index}
            className="bg-gray-800 rounded-lg overflow-hidden shadow-md flex flex-row items-center space-x-4 p-4"
            variants={articleVariants} // add variants
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
            </div>
            <div className="flex flex-col w-full">
              <a href={article.link} target="_blank" rel="noopener noreferrer">
                <h2 className="text-xl font-bold text-white font-serif">
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
          </motion.div>
        ))}
      </div>
    </motion.div>
  );
}
