import "./globals.css";

export const metadata = {
  title: "Storage System Console",
  description: "Business console for SQLite-backed company analysis storage."
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
