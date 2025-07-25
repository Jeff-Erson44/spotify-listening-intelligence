import React from "react";

export default function Loading() {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-white dark:bg-black transition-opacity duration-300">
      <div className="flex flex-col items-center space-y-4">
        <div className="animate-spin rounded-full h-12 w-12 border-t-4 border-b-4 border-gray-900 dark:border-white" />
        <p className="text-gray-700 dark:text-gray-300 text-sm">Chargement du profil en cours...</p>
      </div>
    </div>
  );
}