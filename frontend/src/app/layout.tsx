import type { Metadata } from "next";
import "@/style/globals.css";

export const metadata: Metadata = {
  title: "Spotify Listening Intelligence",
  description: "Analyse musicale avec profil émotionnel",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="fr">
      <body>
        {children}
      </body>
    </html>
  );
}
