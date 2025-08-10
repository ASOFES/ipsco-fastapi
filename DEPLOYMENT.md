# 🚀 Guide de Déploiement IPSCO FastAPI sur Render

## 📋 Prérequis

1. **Compte GitHub** avec votre code
2. **Compte Render** (gratuit)
3. **Base Supabase** configurée

## 🔗 Étape 1: Pousser sur GitHub

```bash
# Créer un nouveau repository sur GitHub
# Puis pousser votre code :

git remote add origin https://github.com/VOTRE_USERNAME/ipsco-fastapi.git
git branch -M main
git push -u origin main
```

## 🌐 Étape 2: Déployer sur Render

### 1. Aller sur Render Dashboard
- Visiter [dashboard.render.com](https://dashboard.render.com)
- Cliquer sur **"New +"** → **"Web Service"**

### 2. Connecter GitHub
- Cliquer sur **"Connect account"** si pas encore connecté
- Sélectionner votre repository `ipsco-fastapi`

### 3. Configuration du Service

```yaml
Name: ipsco-fastapi
Region: Frankfurt (EU) # Plus proche de vous
Branch: main
Root Directory: ./
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
```

### 4. Variables d'Environnement

```bash
# Cliquer sur "Environment" et ajouter :

DATABASE_URL=postgresql://postgres:ALcX66APUxYltilK@db.ruejckvikpewirrfzfhy.supabase.co:5432/postgres?sslmode=require
SECRET_KEY=votre_cle_secrete_tres_longue
DEBUG=False
PORT=8000
```

### 5. Déploiement
- Cliquer sur **"Create Web Service"**
- Render va automatiquement :
  - Cloner votre code
  - Installer les dépendances
  - Démarrer le service

## ✅ Vérification

### 1. Logs de Déploiement
- Dans Render, aller dans **"Logs"**
- Vérifier que l'installation se passe bien

### 2. Test de l'API
- Votre API sera disponible sur : `https://ipsco-fastapi.onrender.com`
- Documentation : `https://ipsco-fastapi.onrender.com/docs`

### 3. Test de Connexion
```bash
curl https://ipsco-fastapi.onrender.com/health
```

## 🔧 Dépannage

### Erreur de Build
```bash
# Vérifier requirements.txt
# Vérifier la version Python (3.11)
# Vérifier les dépendances
```

### Erreur de Connexion DB
```bash
# Vérifier DATABASE_URL
# Vérifier que Supabase est accessible
# Vérifier les permissions
```

### Erreur de Port
```bash
# Render utilise $PORT automatiquement
# Ne pas hardcoder le port 8000
```

## 📱 Frontend React

### Déployer sur Vercel
1. Pousser le code React sur GitHub
2. Connecter Vercel au repository
3. Configurer l'URL de l'API :
   ```bash
   REACT_APP_API_URL=https://ipsco-fastapi.onrender.com
   ```

## 🎯 URLs Finales

- **Backend API** : `https://ipsco-fastapi.onrender.com`
- **Documentation** : `https://ipsco-fastapi.onrender.com/docs`
- **Frontend** : `https://ipsco-react.vercel.app`

## 🚀 Avantages Render

- ✅ **Gratuit** pour commencer
- ✅ **Déploiement automatique** depuis GitHub
- ✅ **SSL automatique** (HTTPS)
- ✅ **Monitoring** et logs
- ✅ **Scaling** facile
- ✅ **Support** PostgreSQL si besoin

---

🎉 **Votre IPSCO FastAPI est maintenant déployé et accessible partout !** 🎉
