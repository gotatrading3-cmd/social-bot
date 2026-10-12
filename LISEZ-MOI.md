# Bot de publications (Facebook / Instagram / TikTok)
6 publications par jour (une image, une vidéo avec musique, en alternance) (toutes les ~2 h 50, entre 6 h et 22 h UTC). Appels à l'action en rotation : Telegram, ouverture de compte (lien partenaire), aucun.
Rien n'est publié tant que la variable GitHub SOCIAL_LIVE n'est pas "true". Arrêt d'urgence : SOCIAL_LIVE=false ou SOCIAL_STOP=true.
Réglages (variables du dépôt) : SOCIAL_MAX_PER_DAY, SOCIAL_GAP_MIN, SOCIAL_HOURS, SOCIAL_VIDEO_EVERY, SOCIAL_CTA_LINK, SOCIAL_ACCOUNT_LINK.
Aperçu local sans rien publier : python social_runner.py --preview 6
Connexion Meta (Facebook + Instagram) : python configurer_reseaux.py gotatrading3-cmd/social-bot
