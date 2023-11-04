"use client";

import Image from "next/image";
import Link from "next/link";
import { motion } from "framer-motion";

export default function HomeClient() {
  return (
    <div className="w-full h-screen bg-[#000000] flex items-center justify-center flex-col space-y-6">
      <div>
        {/* <h1 className="text-white text-3xl font-serif">Daily Digest Agent</h1> */}
        {/* <p className="text-gray-400 font-sans">
                                        Please login below.
                                </p> */}
      </div>
      <div className="bg-[#1c1c1c] p-10 w-80 space-y-6 rounded-none">
        <h1 className="text-white text-3xl font-serif">Login</h1>
        <p className="text-gray-400 font-sans">
          Please enter your credentials to proceed.
        </p>
        <motion.div
          className="space-y-2"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1, transition: { delay: 0.2 } }}
        >
          <label
            className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 text-gray-300 font-sans"
            htmlFor="email"
          >
            Email
          </label>
          <input
            className="flex h-10 w-full border border-input px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 bg-[#2d2d2d] text-white font-mono rounded-none"
            id="email"
            placeholder="m@example.com"
            required=""
            type="email"
          />
        </motion.div>
        <motion.div
          className="space-y-2"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1, transition: { delay: 0.2 } }}
        >
          <label
            className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 text-gray-300 font-sans"
            htmlFor="password"
          >
            Password
          </label>
          <input
            className="flex h-10 w-full border border-input px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 bg-[#2d2d2d] text-white font-mono rounded-none"
            id="password"
            required=""
            type="password"
          />
        </motion.div>
        <motion.div
          className="flex flex-col items-center justify-center animate-all p-1"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1, transition: { delay: 0.2 } }}
        >
          <Link
            className="w-full bg-[#333333] hover:bg-[#4d4d4d] text-white font-bold rounded-none flex justify-center items-center"
            // type="submit"
            href={"/onboarding"}
          >
            Sign in
          </Link>
        </motion.div>
        <motion.div
          className="flex justify-between items-center mt-4"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1, transition: { delay: 0.2 } }}
        >
          <hr className="border-gray-600 w-full" />
          <span className="px-2 text-gray-400">or</span>
          <hr className="border-gray-600 w-full" />
        </motion.div>
        <motion.button
          className="w-full text-white border-gray-400 hover:border-gray-500 font-bold rounded-none mt-4"
          type="button"
          variant="outline"
          whileHover={{ backgroundColor: "#4d4d4d" }}
          whileTap={{ backgroundColor: "#333333" }}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1, transition: { delay: 0.2 } }}
        >
          Sign up
        </motion.button>
      </div>
    </div>
  );
}
