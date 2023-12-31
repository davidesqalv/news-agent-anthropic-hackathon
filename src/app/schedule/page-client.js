"use client";

import React, { useState } from "react";
import { motion } from "framer-motion";
import { redirect } from "next/navigation";

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

const API_URL = process.env.API_URL;

export default function ScheduleClient() {
  const [isDaily, setIsDaily] = useState(true);
  const [selectedTime, setSelectedTime] = useState("");
  const [selectedDay, setSelectedDay] = useState("");

  const [redirectPage, setRedirectPage] = useState(false);

  const handleDoneClick = () => {
    console.log("selectedTime");
    console.log(selectedTime);

    // Convert selectedTime to HH:mm format
    const [hours, minutes] = selectedTime.split(":");
    let formattedHours = parseInt(hours);
    if (formattedHours === 12 && selectedTime.includes("AM")) {
      formattedHours = 0;
    } else if (formattedHours !== 12 && selectedTime.includes("PM")) {
      formattedHours += 12;
    }
    const formattedTime = `${formattedHours
      .toString()
      .padStart(2, "0")}:${minutes}`;

    // const data = {
    //   is_daily: isDaily,
    //   reminder_time: formattedTime,
    //   day: selectedDay,
    // };

    const data = {
      is_daily: isDaily,
      reminder_time: formattedTime,
      day: selectedDay,
    };

    const options = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    };

    console.log("sending over");
    console.log(data);

    fetch(`${API_URL}/schedule`, options)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        setRedirectPage(true);
      })
      .then((data) => {
        console.log("Success:", data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  if (redirectPage) {
    redirect("/feed-settings");
  }

  return (
    <motion.div
      className="w-full h-screen bg-black flex items-center justify-center flex-col space-y-6 animate-all"
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      <h1 className="text-white text-3xl font-serif">Choose Your Schedule</h1>
      <div className="flex justify-center mt-8">
        <div className="flex rounded-md shadow-md">
          <button
            className={`${
              isDaily ? "bg-gray-500 text-white" : "bg-gray-200 text-gray-500"
            } px-4 py-2 rounded-l-md focus:outline-none`}
            onClick={() => setIsDaily(true)}
          >
            Daily
          </button>
          <button
            className={`${
              !isDaily ? "bg-gray-500 text-white" : "bg-gray-200 text-gray-500"
            } px-4 py-2 rounded-r-md focus:outline-none`}
            onClick={() => setIsDaily(false)}
          >
            Weekly
          </button>
        </div>
      </div>
      <div className="flex justify-center mt-8">
        <div className="flex flex-col items-center">
          <label htmlFor="time-selector" className="text-gray-400 font-sans">
            Select time:
          </label>
          <input
            type="time"
            id="time-selector"
            value={selectedTime}
            onChange={(e) => setSelectedTime(e.target.value)}
            className="mt-2 px-2 py-1 rounded-md border-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:border-transparent"
          />
        </div>
        {!isDaily && (
          <div className="flex flex-col items-center ml-8">
            <label htmlFor="day-selector" className="text-gray-400 font-sans">
              Select day:
            </label>
            <select
              id="day-selector"
              value={selectedDay}
              onChange={(e) => setSelectedDay(e.target.value)}
              className="mt-2 px-2 py-1 rounded-md border-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:border-transparent"
            >
              <option value="">Select a day</option>
              <option value="monday">Monday</option>
              <option value="tuesday">Tuesday</option>
              <option value="wednesday">Wednesday</option>
              <option value="thursday">Thursday</option>
              <option value="friday">Friday</option>
              <option value="saturday">Saturday</option>
              <option value="sunday">Sunday</option>
            </select>
          </div>
        )}
      </div>
      <div className="flex justify-center mt-8">
        <button
          className="bg-gray-500 text-white px-4 py-2 rounded-md focus:outline-none"
          onClick={handleDoneClick}
        >
          Done
        </button>
      </div>
    </motion.div>
  );
}
