# 11Labs ConvAI Agent - Web Application

A modern web application featuring the 11Labs ElevenLabs ConvAI agent for real-time conversational AI interactions.

## Features

🤖 **AI-Powered Conversations** - Real-time chat with advanced AI
🎙️ **Voice Support** - Natural speech interaction
⚡ **Fast & Responsive** - Optimized performance
🎨 **Modern Design** - Beautiful UI with glassmorphism effects
📱 **Mobile Friendly** - Fully responsive layout

## Agent Configuration

- **Agent ID**: `agent_4101kne33jyvef3rjxyfhd1kyyp0`
- **Service**: 11Labs ConvAI Widget

## Deploy to GitHub Pages

Follow these steps to deploy this application to GitHub Pages:

### Step 1: Create a GitHub Repository

1. Go to [GitHub](https://github.com/new) and create a new repository
2. Name it `11labsAgent` (or your preferred name)
3. Choose public repository
4. Don't initialize with README (we already have one)

### Step 2: Initialize Git and Push

```bash
cd /home/soumarshinagbiswas/11labsAgent

# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Add 11Labs ConvAI agent app"

# Add remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/11labsAgent.git

# Push to GitHub main branch
git branch -M main
git push -u origin main
```

### Step 3: Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** → **Pages**
3. Under "Source", select **Deploy from a branch**
4. Select **main** branch and **/(root)** folder
5. Click **Save**

Your app will be live at: `https://YOUR_USERNAME.github.io/11labsAgent`

## Alternative: Deploy to Vercel (Recommended)

Vercel offers better performance and additional features.

1. Go to [Vercel](https://vercel.com/new) and click "New Project"
2. Import your GitHub repository
3. Click "Deploy"
4. Your app will be live instantly with a custom domain

## Alternative: Deploy to Netlify

1. Go to [Netlify](https://app.netlify.com/start) and click "New site from Git"
2. Connect your GitHub account
3. Select your repository
4. Click "Deploy site"

## Local Development

Simply open `index.html` in your browser or use:

```bash
# Using Python
python -m http.server 8000

# Using Node.js
npx http-server
```

Visit `http://localhost:8000` (or displayed port)

## File Structure

```
11labsAgent/
├── index.html          # Main HTML page with ConvAI widget
├── styles.css          # Styling and responsive design
├── README.md          # This file
└── .gitignore         # Git ignore rules
```

## Customization

### Change Agent ID

Edit `index.html` and replace the agent ID:
```html
<elevenlabs-convai agent-id="YOUR_NEW_AGENT_ID"></elevenlabs-convai>
```

### Customize Colors

Edit `styles.css` and modify the CSS variables:
```css
:root {
    --primary-color: #00d4ff;
    --secondary-color: #1a1a2e;
    --accent-color: #16213e;
    --text-color: #ffffff;
}
```

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers

## Troubleshooting

### Widget not showing?
- Check that your agent ID is correct
- Verify the 11Labs script is loading
- Clear browser cache

### Styled incorrectly?
- Make sure `styles.css` is in the same directory as `index.html`
- Clear cache or hard refresh (Ctrl+Shift+R / Cmd+Shift+R)

## Support

- 11Labs Documentation: https://elevenlabs.io/docs
- GitHub Pages Help: https://docs.github.com/en/pages

## License

This project is open source and available under the MIT License.

---

**Last Updated**: 2026 | Made with ❤️ for AI conversations
