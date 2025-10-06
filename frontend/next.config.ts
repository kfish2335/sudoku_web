import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  output: 'export',
  images: { unoptimized: true },
  trailingSlash: true, 
  env: {
    NEXT_PUBLIC_SUDOKU_BASE: process.env.NEXT_PUBLIC_SUDOKU_BASE,
  },
};

export default nextConfig;
