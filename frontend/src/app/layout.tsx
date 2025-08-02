import type { Metadata } from "next";
import ClientLayout from "@/app/clientLayout";
import "@/style/globals.css";
import { SessionProvider } from "@/context/SessionContext";

export const metadata: Metadata = {
  title: "Spotify Listening Intelligence",
  description: "Analyse musicale avec profil émotionnel",
  openGraph: {
    title: "Spotify Listening Intelligence",
    description: "Découvrez votre profil émotionnel à travers votre musique",
    url: "https://spotify-listening-gray.vercel.app",
    siteName: "Spotify Listening Intelligence",
    images: [
      {
        url: "https://spotify-listening-gray.vercel.app/images/preview.png", 
        width: 1200,
        height: 630,
        alt: "Aperçu Spotify Listening Intelligence",
      },
    ],
    locale: "fr_FR",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "Spotify Listening Intelligence",
    description: "Analysez vos écoutes musicales pour révéler votre profil émotionnel",
    images: ["https://spotify-listening-gray.vercel.app/images/preview.png"],
  },
};


export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="fr">
      <head>
        <link rel="icon" type="image/png" sizes="32x32" href="/icone/favicon-32x32.png" />
        <link rel="icon" type="image/png" sizes="16x16" href="/icone/favicon-16x16.png" />
        <link rel="icon" href="/favicon.ico" sizes="any" />
        <link rel="apple-touch-icon" href="/icone/apple-touch-icon.png" />
        <link rel="icon" type="image/png" sizes="192x192" href="/icone/android-chrome-192x192.png" />
        <link rel="icon" type="image/png" sizes="512x512" href="/icone/android-chrome-512x512.png" />

      </head>
      <body>
        <SessionProvider>
          <ClientLayout>
            {children}
          </ClientLayout>
        </SessionProvider>
      </body>
    </html>
  );
}