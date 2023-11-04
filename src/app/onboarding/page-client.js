"use client";

import { motion } from "framer-motion";
import { useState } from "react";

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

const itemVariants = {
  hidden: {
    opacity: 0,
  },
  visible: {
    opacity: 1,
    transition: {
      delay: 0.4,
    },
  },
};

const tagVariants = {
  hidden: {
    opacity: 0,
  },
  visible: {
    opacity: 1,
    transition: {
      duration: 0.5,
      delay: 0.2,
    },
  },
};

export default function OnboardingClient() {
  const [preferences, setPreferences] = useState([
    "Politics",
    "Sports",
    "Technology",
    "Entertainment",
    "Science",
    "Business",
    "Health",
  ]);
  const [selectedPreferences, setSelectedPreferences] = useState([]);
  const [extraTags, setExtraTags] = useState("");
  const [selectedTags, setSelectedTags] = useState([]);

  const handlePreferenceClick = (preference) => {
    if (selectedPreferences.includes(preference)) {
      setSelectedPreferences(
        selectedPreferences.filter((p) => p !== preference)
      );
    } else {
      setSelectedPreferences([...selectedPreferences, preference]);
    }
  };

  const handleAddTagClick = () => {
    if (extraTags.trim() !== "") {
      setSelectedTags([...selectedTags, extraTags.trim()]);
      setExtraTags("");
    }
  };

  const handleRemoveTagClick = (tag) => {
    setSelectedTags(selectedTags.filter((t) => t !== tag));
  };

  return (
    <motion.div
      className="w-full h-screen bg-black flex items-center justify-center flex-col space-y-6 animate-all"
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      <motion.div variants={itemVariants}>
        <h1 className="text-white text-3xl font-bold">Welcome to News Agent</h1>
      </motion.div>
      <motion.div variants={itemVariants}>
        <p className="text-white text-lg">
          Select your preferred news categories:
        </p>
      </motion.div>
      <motion.div variants={itemVariants}>
        <div className="flex flex-wrap justify-center">
          {preferences.map((preference) => (
            <button
              key={preference}
              className={`px-4 py-2 rounded-full m-2 ${
                selectedPreferences.includes(preference)
                  ? "bg-gray-500 text-white"
                  : "bg-white text-gray-500"
              }`}
              onClick={() => handlePreferenceClick(preference)}
            >
              {preference}
            </button>
          ))}
        </div>
      </motion.div>
      <motion.div variants={itemVariants}>
        <div className="flex items-center space-x-2">
          <input
            type="text"
            placeholder="Add extra tags"
            className="border border-gray-300 rounded-md px-4 py-2 w-64"
            value={extraTags}
            onChange={(e) => setExtraTags(e.target.value)}
          />
          <button
            className="px-4 py-2 rounded-md bg-gray-500 text-white"
            onClick={handleAddTagClick}
          >
            Add
          </button>
        </div>
      </motion.div>
      <motion.div variants={itemVariants}>
        <div className="flex flex-wrap justify-center">
          {selectedTags.map((tag) => (
            <motion.div
              key={tag}
              className="px-4 py-2 rounded-full m-2 bg-gray-500 text-white relative"
              variants={tagVariants}
              initial="hidden"
              animate="visible"
            >
              {tag}
              <button
                className="absolute top-0 right-0 px-2 py-1 text-center"
                style={{ padding: "2px 6px", margin: "2px" }}
                onClick={() => handleRemoveTagClick(tag)}
              >
                x
              </button>
            </motion.div>
          ))}
        </div>
      </motion.div>
    </motion.div>
  );
}
