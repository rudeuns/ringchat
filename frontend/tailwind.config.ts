import type { Config } from "tailwindcss";
import { PluginAPI } from "tailwindcss/types/config";
const plugin = require("tailwindcss/plugin");

const config: Config = {
  content: [
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    colors: {
      transparent: "transparent",
      current: "currentColor",
      black: "#333333",
      white: "#FEFEFE",
      yellow: "#F3AF27",
      gray: "#D2D2D2",
      muted: "#F3F4F7",
      red: "#e85d5d",
      primary: {
        DEFAULT: "#4B6387",
        light: "#6582AA",
        dark: "#334663",
      },
    },
  },
  plugins: [
    plugin(function ({ addBase, theme }: PluginAPI) {
      addBase({
        ":root": {
          "--color-transparent": theme("colors.transparent"),
          "--color-primary": theme("colors.primary.DEFAULT"),
          "--color-primary-light": theme("colors.primary.light"),
          "--color-muted": theme("colors.muted"),
          "--color-yellow": theme("colors.yellow"),
          "--color-white": theme("colors.white"),
          "--color-black": theme("colors.black"),
          "--color-gray": theme("colors.gray"),
        },
      });
    }),
  ],
};

export default config;
