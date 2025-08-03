# Spotify Listening Intelligence

Générez un **profil musical personnalisé** à partir d'une sélection d’artistes. Visualisez vos **émotions dominantes**, vos **genres musicaux clés** et vos **tendances d’écoute**, grâce à une interface moderne et animée.

> ⚠️ **Note importante** : en raison de nouvelles restrictions imposées par Spotify, la version connectée (OAuth) **n’est plus accessible au public**.  
> Seul le **mode simulation** (sans compte Spotify) est disponible actuellement.

## 🚀 Démo en ligne

👉 [spotify-listening](https://spotify-listening-gray.vercel.app)

---

## 🔍 Fonctionnalités

- ✅ Mode sans compte Spotify avec sélection manuelle d’artistes
- ✅ Extraction simulée des données audio (features Spotify)
- ✅ Détection des émotions musicales dominantes
- ✅ Génération d’un profil musical visuel, animé et interactif
- ❌ *(désactivé)* Connexion via Spotify (OAuth) pour extraire les écoutes réelles
- 💡 Interface moderne avec Next.js, Tailwind

---

## 🧠 Architecture Backend (AWS Serverless)

| Service        | Rôle                                                                 |
|----------------|----------------------------------------------------------------------|
| **AWS Lambda** | Fonctions : `create-session`, `extract-simulated`, `search`, `transform`, `generate-profile`, `get-profile` |
| **API Gateway**| Exposition de routes HTTP, CORS                                      |
| **Amazon S3**  | Stockage des données JSON (simulées et résultats de profil)          |
| **IAM Role**   | Gestion fine des permissions par fonction                            |
| **Amazon ECR** | Conteneurisation Docker des fonctions Lambda                         |

---

## 💻 Frontend (Next.js 14 + Tailwind)

- **Next.js App Router** (`/app`)
- **Tailwind CSS** (responsive mobile-first)
- **LocalStorage** pour le suivi des sessions (`sessionId`)
- **Pages** :
  - `/` : Landing page
  - `/simulate` : Sélection d’artistes
  - `/profile` : Visualisation du profil généré
  - `/spotify` : *(désactivée)* Connexion via Spotify (non accessible en production)

---

## 📌 Pourquoi cette limitation avec Spotify ?

Spotify a récemment **renforcé les critères de validation pour l’accès aux données utilisateurs** (écoutes récentes, audio features, etc.).  
Les applications non vérifiées par Spotify **ne peuvent plus utiliser l’authentification OAuth en production publique**, sauf à inscrire manuellement chaque testeur dans le dashboard développeur.

👉 C’est pourquoi la version actuellement en ligne est **100 % simulée** — mais suit le même pipeline de traitement que la version connectée.

---

## 🙏 Crédits & Remerciements

- API Spotify Web (en mode simulation)
- Design par [@kitana.ht](https://www.instagram.com/kitana.ht/)
- Développé par [@JeffersonK](https://www.jefferson-k.com/)

---