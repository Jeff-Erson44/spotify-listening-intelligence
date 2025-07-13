import type { Metadata } from "next";
import ClientLayout from "@/app/clientLayout";
import "@/style/globals.css";

export const metadata: Metadata = {
  title: "Spotify Listening Intelligence",
  description: "Analyse musicale avec profil émotionnel",
};


export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
       

    <html lang="fr">
      <body>
        <ClientLayout>{children}</ClientLayout>
      </body>
    </html>
  );
}