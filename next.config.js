/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'api.mangaupdates.com',
      },
      {
        protocol: 'https',
        hostname: 'cdn.mangaupdates.com',
      },
    ],
  },
};

module.exports = nextConfig;