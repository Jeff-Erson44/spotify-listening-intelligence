# Spotify Listening Intelligence

Générez un profil musical personnalisé à partir de vos écoutes récentes ou de vos artistes préférés. Visualisez vos émotions dominantes, vos genres musicaux clés et vos tendances d’écoute, grâce à une interface fluide et moderne.

## Démo en ligne

👉 [spotify-listening](https://spotify-listening-gray.vercel.app)

## Fonctionnalités

- Connexion sécurisée avec Spotify (OAuth)
- Mode sans compte Spotify avec sélection manuelle des artistes
- Extraction et traitement des données audio (features Spotify)
- Détection des émotions dominantes
- Génération d’un profil musical visuel et interactif
- Animation et interface moderne (Next.js, Tailwind, animations GSAP)

## Architecture Backend (AWS Serverless)

| Service | Rôle |
|--------|------|
| **AWS Lambda** | Exécution des fonctions `create-session`, `extract-user`, `extract-simulated`, `search`, `transform`, `generate-profile`, `get-profile` |
| **API Gateway (HTTP)** | Exposition de toutes les routes HTTP pour le frontend , mise en place du CORS |
| **Amazon S3** | Stockage des fichiers JSON (données extraites, transformées et profil généré) |
| **IAM Role** | Permissions spécifiques à chaque Lambda |
| **Amazon ECR** | Conteneurisation des fonctions Lambda via Docker (runtime Node.js personnalisé) |

Les fonctions sont conteneurisées avec **Docker**, déployées sur **ECR**, puis appelées via **API Gateway**.

## Frontend (Next.js + Tailwind + Animation)

- **Next.js 14** avec App Router (`/app`)
- **Tailwind CSS** + design responsive mobile-first
- State management simple avec `localStorage` et `useState`
- Gestion des sessions via `sessionId` généré automatiquement

Pages principales :
- `/` → Landing page
- `/simulate` → Sélection manuelle d’artistes
- `/spotify` → Connexion + extraction auto
- `/profile` → Visualisation du profil musical

---

### 8. **Crédits / Remerciements / Inspirations**


## Crédits

- API Spotify Web
- Design par @[Kitana.ht](https://www.instagram.com/kitana.ht/)
- Developpé par @[JeffersonK](https://www.jefferson-k.com/)
