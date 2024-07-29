import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    colors: {
      black: '#1E1E1E',
      white: '#FEFEFE',
      primary: {
        DEFAULT: '#D1C8C2',
        light: '#E5E1D8',
        dark: '#BFB3AA',
      },
    },
  },
  plugins: [],
};
export default config;
