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

const API_URL = process.env.API_URL;

export default function FeedClient() {
  const [articles, setArticles] = useState([]);
  const [votes, setVotes] = useState([]);
  const [images, setImages] = useState([]);
  const [response, setResponse] = useState("");
  const [responseRequested, setResponseRequested] = useState(false);

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

  useEffect(() => {
    function fetchArticles() {
      setResponseRequested(true);
      const options = {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({}),
      };
      fetch(`${API_URL}/generate-digest`, options)
        .then((response) => {
          if (!response.ok) {
            throw new Error(
              `Error: ${response.status} - ${response.statusText}`
            );
          }
          return response.json();
        })
        .then((responseJson) => {
          console.log("repsonse");
          console.log(responseJson);
          // setArticles(responseJson.digest);
          // setVotes(responseJson.digest.map(() => 0));
          // const newImages = [];
          // for (let i = 0; i < responseJson.digest.length; i++) {
          //   const imageUrl = await getArticleImage(responseJson.digest[i].link);
          //   newImages.push(imageUrl);
          // }
          // setImages(newImages);
          setResponse(responseJson);
        })
        .catch((error) => {
          console.error(error);
        });
    }
    if (!responseRequested) {
      fetchArticles();
    }
  }, [responseRequested]);

  const handleVote = (index, value) => {
    const newVotes = [...votes];
    newVotes[index] += value;
    setVotes(newVotes);
  };

  return (
    <motion.div
      className="w-full h-screen bg-black flex items-center justify-center flex-col space-y-6 animate-all"
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      <h1 className="text-3xl font-bold text-white font-serif pt-12">Feed</h1>

      {response === "" ? (
        <div className="flex justify-center items-center">
          <svg
            className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            ></circle>
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647zM12 20.735A7.962 7.962 0 0112 12v-4H8.063l3.647-3.646 1.414 1.414L10.891 7H12a6 6 0 100 12z"
            ></path>
          </svg>
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-4 max-w-5xl max-h-[80vh]">
          {/* {articles.map((article, index) => (
            <motion.div
              key={article.title}
              className="bg-white rounded-lg shadow-lg overflow-hidden"
              variants={articleVariants}
            >
              <div className="relative h-48">
                <Image
                  src={images[index]}
                  alt={article.title}
                  layout="fill"
                  objectFit="cover"
                />
              </div>
              <div className="p-4">
                <h2 className="text-xl font-bold mb-2">{article.title}</h2>
                <p className="text-gray-700 text-base">{article.description}</p>
                <div className="flex justify-between items-center mt-4">
                  <button
                    className="text-gray-500 hover:text-gray-900"
                    onClick={() => handleVote(index, 1)}
                  >
                    <FaArrowUp />
                  </button>
                  <span className="text-gray-700 font-bold">
                    {votes[index]}
                  </span>
                  <button
                    className="text-gray-500 hover:text-gray-900"
                    onClick={() => handleVote(index, -1)}
                  >
                    <FaArrowDown />
                  </button>
                </div>
              </div>
            </motion.div>
          ))} */}
          <div
            className="text-lg text-gray-100 overflow-y-auto"
            style={{ whiteSpace: "pre-wrap" }}
          >
            {response}
          </div>
        </div>
      )}
    </motion.div>
  );
}
