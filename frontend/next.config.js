/** @type {import('next').NextConfig} */
const nextConfig = {
  // The FastAPI backend runs on port 8000 in development.
  // Requests to /api/* are proxied so the frontend never exposes the raw backend URL.
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/:path*`,
      },
    ];
  },
};

module.exports = nextConfig;
