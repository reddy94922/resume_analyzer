# Push Project to GitHub - Step by Step Guide

## Option 1: Using Git Command Line (Recommended)

### Step 1: Install Git
If you don't have Git installed, download it from: https://git-scm.com/download/win

After installation, restart your terminal.

### Step 2: Navigate to Project
```bash
cd c:\Users\NXTWAVE\Downloads\resume_analyzer
```

### Step 3: Initialize Repository
```bash
git config --global user.name "reddy94922"
git config --global user.email "your_email@example.com"

git init
```

### Step 4: Add Files
```bash
git add .
```

### Step 5: Create Initial Commit
```bash
git commit -m "Initial commit: Resume Analyzer with Gemini AI integration"
```

### Step 6: Add Remote Repository
```bash
git remote add origin https://github.com/reddy94922/resume_analyzer.git
```

### Step 7: Push to GitHub
```bash
git branch -M main
git push -u origin main
```

You'll be prompted to enter your GitHub credentials or use a Personal Access Token.

---

## Option 2: Using GitHub Desktop (Easier)

1. Download **GitHub Desktop** from: https://desktop.github.com/
2. Sign in with your GitHub account
3. Click "File" → "Clone Repository"
4. Enter: `https://github.com/reddy94922/resume_analyzer.git`
5. Choose local path: `c:\Users\NXTWAVE\Downloads\resume_analyzer`
6. Click "Clone"
7. Make changes locally, then:
   - Right-click files → "Changes"
   - Add a commit message
   - Click "Commit to main"
   - Click "Push origin"

---

## Option 3: Using VS Code Git Integration

1. Open VS Code
2. Open the project folder: `c:\Users\NXTWAVE\Downloads\resume_analyzer`
3. Click "Source Control" icon (left sidebar)
4. Click "Initialize Repository"
5. Stage changes (click "+" on files)
6. Add commit message: "Initial commit"
7. Click commit icon
8. Click "..." menu → "Push to"
9. Enter: `https://github.com/reddy94922/resume_analyzer.git`

---

## Important: Sensitive Files

Before pushing, ensure these files are in `.gitignore` (already included):

```
.env
.streamlit/secrets.toml
__pycache__/
*.pyc
.pytest_cache/
venv/
*.egg-info/
```

**DO NOT** commit API keys or sensitive data!

---

## What Gets Pushed

✅ Code files (Python, Streamlit, LangChain)
✅ Configuration files (requirements.txt, README.md)
✅ Tests
✅ Documentation

❌ .env file (contains API keys)
❌ Virtual environment (venv/)
❌ Cache files (__pycache__)
❌ Vector store index

---

## GitHub Authentication

### Method 1: Personal Access Token (Recommended)
1. Go to: https://github.com/settings/tokens
2. Click "Generate new token"
3. Select: repo, read:user, write:repo_hook
4. Copy token
5. When prompted for password, paste the token

### Method 2: SSH Key
1. Generate SSH key: `ssh-keygen -t rsa`
2. Add to GitHub: https://github.com/settings/keys
3. Use SSH URL: `git@github.com:reddy94922/resume_analyzer.git`

---

## Verify Push Success

After pushing, verify at: https://github.com/reddy94922/resume_analyzer

You should see all your files listed there!

---

## Future Updates

To update your GitHub repository with changes:

```bash
cd c:\Users\NXTWAVE\Downloads\resume_analyzer
git add .
git commit -m "Description of changes"
git push origin main
```

---

## Troubleshooting

### Error: "fatal: not a git repository"
```bash
git init
```

### Error: "fatal: Authentication failed"
- Use Personal Access Token instead of password
- Or check SSH keys are properly configured

### Error: "The repository already exists"
- The GitHub repo is empty, that's fine
- Use: `git push -u origin main` with `-u` flag

### Branches not showing
- Use: `git branch -M main` to rename to main branch

---

Good luck pushing your project! 🚀
