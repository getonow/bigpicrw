# Railway Deployment Guide for BIGPICTURE AI Agent

This guide will help you deploy your BIGPICTURE AI Agent to Railway so it can be accessed over the internet.

## Prerequisites

1. **Railway Account**: Sign up at [railway.app](https://railway.app)
2. **GitHub Repository**: Your code should be in a GitHub repository
3. **Environment Variables**: You'll need your API keys and database credentials

## Step 1: Prepare Your Repository

Your repository should now include these new files:
- `Procfile` - Tells Railway how to run your app
- `runtime.txt` - Specifies Python version
- `railway.json` - Railway-specific configuration
- `RAILWAY_DEPLOYMENT_GUIDE.md` - This guide

## Step 2: Deploy to Railway

### Option A: Deploy via Railway Dashboard

1. **Connect Repository**:
   - Go to [railway.app](https://railway.app)
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

2. **Configure Environment Variables**:
   - In your Railway project dashboard, go to "Variables" tab
   - Add the following environment variables:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   DATABASE_URL=your_database_connection_string
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_key
   ```

3. **Deploy**:
   - Railway will automatically detect it's a Python project
   - It will install dependencies from `requirements.txt`
   - The app will start using the command in `Procfile`

### Option B: Deploy via Railway CLI

1. **Install Railway CLI**:
   ```bash
   npm install -g @railway/cli
   ```

2. **Login and Deploy**:
   ```bash
   railway login
   railway init
   railway up
   ```

3. **Set Environment Variables**:
   ```bash
   railway variables set OPENAI_API_KEY=your_openai_api_key_here
   railway variables set DATABASE_URL=your_database_connection_string
   railway variables set SUPABASE_URL=your_supabase_url
   railway variables set SUPABASE_KEY=your_supabase_key
   ```

## Step 3: Configure Database (if using Supabase)

If you're using Supabase as your database:

1. **Create Supabase Project** (if you haven't already):
   - Go to [supabase.com](https://supabase.com)
   - Create a new project
   - Get your project URL and API key

2. **Set Database Variables in Railway**:
   ```
   DATABASE_URL=postgresql+asyncpg://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres
   SUPABASE_URL=https://[YOUR-PROJECT-REF].supabase.co
   SUPABASE_KEY=[YOUR-ANON-KEY]
   ```

## Step 4: Test Your Deployment

Once deployed, Railway will provide you with a URL like:
`https://your-app-name.railway.app`

Test your endpoints:
- Health check: `https://your-app-name.railway.app/health`
- Root endpoint: `https://your-app-name.railway.app/`
- Analyze endpoint: `https://your-app-name.railway.app/analyze-part/`

## Step 5: Update Frontend Integration

Update your frontend application to use the new Railway URL:

```javascript
// Replace your local URL
const API_BASE_URL = 'https://your-app-name.railway.app';

// Example API call
const response = await fetch(`${API_BASE_URL}/analyze-part/`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    message: 'Supplier requesting 15% increase for part PA-10197'
  })
});
```

## Step 6: Configure Custom Domain (Optional)

1. **Add Custom Domain**:
   - In Railway dashboard, go to "Settings" → "Domains"
   - Add your custom domain
   - Configure DNS records as instructed

2. **Update CORS Settings**:
   - Update `app/main.py` to include your frontend domain:
   ```python
   allow_origins=["https://your-frontend-domain.com"]
   ```

## Environment Variables Reference

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | Yes |
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `SUPABASE_URL` | Your Supabase project URL | Yes |
| `SUPABASE_KEY` | Your Supabase anon key | Yes |
| `PORT` | Port number (set automatically by Railway) | No |

## Troubleshooting

### Common Issues:

1. **Build Failures**:
   - Check that all dependencies are in `requirements.txt`
   - Ensure Python version in `runtime.txt` is supported

2. **Environment Variables**:
   - Verify all required variables are set in Railway dashboard
   - Check variable names match exactly (case-sensitive)

3. **Database Connection**:
   - Ensure `DATABASE_URL` is correctly formatted
   - Check if your database allows external connections

4. **CORS Issues**:
   - Update `allow_origins` in `app/main.py` with your frontend domain
   - Test with browser developer tools

### Logs and Debugging:

- View logs in Railway dashboard under "Deployments"
- Use Railway CLI: `railway logs`
- Check application logs for specific error messages

## Monitoring and Maintenance

1. **Health Checks**: Your app includes a `/health` endpoint for monitoring
2. **Logs**: Monitor logs in Railway dashboard
3. **Scaling**: Railway can auto-scale based on traffic
4. **Updates**: Push to GitHub to trigger automatic deployments

## Security Considerations

1. **Environment Variables**: Never commit API keys to your repository
2. **CORS**: Update `allow_origins` to only include your frontend domain
3. **Database**: Use connection pooling and secure database credentials
4. **API Keys**: Rotate API keys regularly

## Cost Optimization

Railway pricing is based on usage:
- Free tier available for development
- Pay-as-you-go for production
- Monitor usage in Railway dashboard
- Consider using Railway's sleep feature for development projects

## Next Steps

After successful deployment:
1. Test all API endpoints thoroughly
2. Update your frontend to use the new URL
3. Set up monitoring and alerts
4. Configure custom domain if needed
5. Set up CI/CD for automatic deployments

Your BIGPICTURE AI Agent is now accessible over the internet at your Railway URL! 