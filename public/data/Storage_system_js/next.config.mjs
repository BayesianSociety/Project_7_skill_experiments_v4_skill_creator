import path from "node:path";
import { fileURLToPath } from "node:url";

const projectRoot = path.dirname(fileURLToPath(import.meta.url));

const nextConfig = {
  turbopack: {
    root: projectRoot
  },
  serverExternalPackages: ["better-sqlite3"]
};

export default nextConfig;
