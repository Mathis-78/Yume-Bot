# 🧠 Yume Bot

Yume Bot est l’un de mes tout premiers projets de programmation.  
Je l’ai créé **au collège**, à une époque où je découvrais à peine le Python et le développement de bots Discord.  
Le code est donc **ancien, expérimental et peu structuré**, mais il représente un bon témoignage de mes débuts dans la programmation.

---

## ⚙️ Description du projet

Yume Bot est un **bot Discord multifonction** développé en Python avec la librairie `discord.py`.  
Il propose une grande variété de commandes, allant de la **modération** à des fonctions plus **ludiques** comme :
- suppression de messages (`.del`)
- changement de statut du bot (`.changestatut`)
- ajout et affichage d’images dans des catégories (`.add`, `.show`)
- classement des catégories d’images (`.toplist`)
- détection de visages ou de chats dans une image avec OpenCV (`.recognize`, `.recognize_cat`)
- sélection aléatoire (`.choisir`)
- mode “compteur” pour incrémenter automatiquement des nombres dans le chat
- gestion de commandes “secrètes” réservées à certains utilisateurs

Le bot sauvegarde ses données dans des fichiers `.txt` et utilise un fichier `token.txt` pour le jeton d’authentification Discord.

---

## 🧩 Technologies utilisées

- **Python 3**
- **discord.py**
- **OpenCV (cv2)** pour la reconnaissance faciale
- **Requests** pour télécharger des images
- **Pickle / OS / Pathlib** pour la gestion locale des fichiers

---

## 🚧 Points faibles (liés à l’époque de création)

Comme il s’agit d’un projet du collège :
- Le code est **monolithique** (tout dans un seul fichier).
- Il n’y a **pas de gestion d’erreurs centralisée**.
- Les commandes sont **codées en dur** (ID, chemins de fichiers, etc.).
- La **sécurité est faible** (pas d’environnement sécurisé pour le token, pas de contrôle d’accès avancé).
- L’utilisation de `time.sleep()` dans un bot asynchrone est **bloquante**.
- La logique pourrait être **fortement simplifiée** avec les cogs (`discord.ext.commands`).

---

## 💡 Pistes d’amélioration

Si je reprenais ce projet aujourd’hui, je pourrais :
- 🔁 **Repartir sur une architecture modulaire** avec des *cogs*.
- 🔐 **Stocker les tokens dans des variables d’environnement** plutôt qu’en clair dans un fichier.
- 🧹 **Nettoyer et typer le code** (PEP8, annotations de types).
- 🧠 **Utiliser une base de données** (SQLite ou JSON structuré) au lieu de fichiers texte.
- ⚡ **Optimiser la logique asynchrone** (remplacer `time.sleep` par `asyncio.sleep`).
- 🌐 **Héberger le bot proprement** sur un serveur ou via Docker.
- 🖼️ **Créer une interface web légère** pour suivre les catégories d’images.

---

## 📚 Conclusion

Yume Bot est un projet **nostalgique et formateur** : il m’a appris les bases du développement Python, de la logique asynchrone, et du fonctionnement d’un bot Discord.  
Même s’il n’est plus à jour aujourd’hui, il marque le début de mon intérêt pour la programmation et l’automatisation.

---

👨‍💻 *Projet d’apprentissage — créé au collège et conservé pour mémoire.*
