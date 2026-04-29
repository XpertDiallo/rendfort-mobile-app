# Choix Fournisseurs - MVP V1

## Decision actuelle

Le MVP V1 utilisera Groq pour les premieres briques d'assistance.

| Besoin | Fournisseur | Modele / endpoint | Statut |
|---|---|---|---|
| Generation de texte et raisonnement | Groq | `openai/gpt-oss-20b` | Valide pour MVP |
| Lecture d'image et OCR ponctuel | Groq | `meta-llama/llama-4-scout-17b-16e-instruct` | Valide pour tests, attention modele preview |
| Text to speech | Groq | `https://api.groq.com/openai/v1/audio/speech` | Endpoint valide, voix francaise a confirmer |
| Speech to text | Groq | `whisper-large-v3-turbo` | A ajouter pour questions vocales |

## Regle de secret

La cle fournisseur ne doit jamais etre committee dans le depot.

Utiliser uniquement une variable d'environnement :

```env
TUTOR_API_KEY=
```

Si une cle a ete partagee dans un canal de discussion, elle doit etre regeneree avant toute mise en production.

## Points a valider

1. Voix francaise
   - L'endpoint TTS Groq est correct.
   - Les voix documentees cote Groq doivent etre verifiees pour le francais.
   - Fallback recommande en MVP : voix native Android/iOS en francais.

2. Verification mathematique
   - Le modele de raisonnement doit etre complete par des corrections validees.
   - Ajouter SymPy pour verifier certains calculs.

3. Embeddings et recherche
   - Choisir un modele d'embeddings.
   - Stockage recommande MVP : PostgreSQL + pgvector.

4. Quotas
   - Limiter le nombre de questions gratuites.
   - Logger les couts par utilisateur.

5. OCR de masse
   - Le modele vision peut aider sur des pages ou extraits.
   - Pour traiter de gros supports scannes, garder un pipeline OCR dedie avec nettoyage et validation humaine.

## Regle produit

Dans l'application, ne jamais afficher les termes interdits documentes dans `docs/legal/sources-and-rights.md`.
