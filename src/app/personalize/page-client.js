"use client";

import { motion } from "framer-motion";
import { redirect } from "next/navigation";
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

const API_URL = process.env.API_URL;

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
  const [loading, setLoading] = useState(false);

  const [redirectPage, setRedirectPage] = useState(false);

  const handlePreferenceClick = (preference) => {
    if (selectedPreferences.includes(preference)) {
      setSelectedPreferences(
        selectedPreferences.filter((p) => p !== preference)
      );
    } else {
      setSelectedPreferences([...selectedPreferences, preference]);
    }
  };

  // const handleAddTagClick = () => {
  //   if (extraTags.trim() !== "") {
  //     setSelectedTags([...selectedTags, extraTags.trim()]);
  //     setExtraTags("");
  //   }
  // };

  const handleAddTagClick = () => {
    if (extraTags.trim() !== "") {
      const newTag = extraTags
        .trim()
        .toLowerCase()
        .replace(/[^a-z0-9]/g, "");
      if (
        !selectedTags
          .map((tag) => tag.toLowerCase().replace(/[^a-z0-9]/g, ""))
          .includes(newTag)
      ) {
        setSelectedTags([...selectedTags, extraTags.trim()]);
      }
      setExtraTags("");
    }
  };

  const handleRemoveTagClick = (tag) => {
    setSelectedTags(selectedTags.filter((t) => t !== tag));
  };

  const handleDoneClick = () => {
    setLoading(true);
    const allTags = [
      ...selectedPreferences,
      ...selectedTags,
      ...extraTags.split(" ").filter((tag) => tag !== ""),
    ];
    console.log(`selected: ${selectedTags}`);
    console.log(`extra: ${extraTags}`);
    console.log(allTags);
    fetch(`${API_URL}/preferences`, {
      method: "POST",
      body: JSON.stringify(allTags),
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to upload tags");
        }
        setLoading(false);
        // handle successful response
        console.log(`response this is my change:`);
        console.log(response);
        setRedirectPage(true);
      })
      .catch((error) => {
        console.error(error);
        setLoading(false);
        // handle error
      });
  };

  if (redirectPage) {
    redirect("/schedule");
  }

  return (
    <motion.div
      className="w-full h-screen bg-black flex items-center justify-center flex-col space-y-6 animate-all"
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      <motion.div variants={itemVariants}>
        <h1 className="text-white text-3xl font-bold font-serif">
          Welcome to RituAI
        </h1>
      </motion.div>
      <motion.div variants={itemVariants}>
        <p className="text-white text-lg">
          For our specialized AI agent to start curating the best content for
          you, select your preferred categories:
        </p>
      </motion.div>
      <motion.div variants={itemVariants}>
        <div className="flex flex-wrap justify-center">
          {preferences.map((preference) => (
            <button
              key={preference}
              className={`px-4 py-2 rounded-full m-2 ${selectedPreferences.includes(preference)
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
      <motion.div variants={itemVariants}>
        <div className="flex items-center space-x-2">
          <input
            type="text"
            placeholder="Add extra preferences"
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
        {loading ? (
          <div className="flex items-center space-x-2">
            <div className="w-6 h-6 border-4 border-gray-200 rounded-full animate-spin"></div>
            <p className="text-white">Processing your preferences...</p>
          </div>
        ) : (
          <button
            className="px-4 py-2 rounded-md bg-gray-500 text-white"
            onClick={handleDoneClick}
          >
            Done
          </button>
        )}
      </motion.div>
    </motion.div>
  );
}
