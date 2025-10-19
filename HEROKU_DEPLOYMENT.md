# Heroku Deployment Guide for VODE

## Prerequisites
- Heroku CLI installed: https://devcenter.heroku.com/articles/heroku-cli
- Git installed
- Heroku account created

## Deployment Steps

### 1. Login to Heroku
```bash
heroku login
```

### 2. Create Heroku App
```bash
heroku create your-app-name
```

Or let Heroku generate a name:
```bash
heroku create
```

### 3. Add PostgreSQL Database
```bash
heroku addons:create heroku-postgresql:essential-0
```

### 4. Set Environment Variables
```bash
# Required for Django
heroku config:set SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
heroku config:set DEBUG=False

# Required for AI features
heroku config:set GEMINI_API_KEY=your_gemini_api_key_here
heroku config:set ELEVENLABS_API_KEY=your_elevenlabs_api_key_here

# Optional: Cloudflare for video storage
heroku config:set CLOUDFLARE_API_KEY=your_cloudflare_key_here
heroku config:set CLOUDFLARE_ACCOUNT_ID=your_cloudflare_account_id_here
```

### 5. Push to Heroku
```bash
git push heroku heroku-deployment:main
```

Or if you're on main branch:
```bash
git push heroku main
```

### 6. Run Migrations
```bash
heroku run python manage.py migrate
```

### 7. Create Superuser (Optional)
```bash
heroku run python manage.py createsuperuser
```

### 8. Collect Static Files (Done automatically by WhiteNoise)
Static files are automatically collected and served by WhiteNoise.

### 9. Open Your App
```bash
heroku open
```

## View Logs
```bash
heroku logs --tail
```

## Useful Commands

### Check Config Variables
```bash
heroku config
```

### Restart App
```bash
heroku restart
```

### Run Django Shell
```bash
heroku run python manage.py shell
```

### Scale Dynos
```bash
heroku ps:scale web=1
```

## Troubleshooting

### Static Files Not Loading
- WhiteNoise is configured to serve static files automatically
- Check that `STATIC_ROOT` is set correctly in settings.py
- Verify WhiteNoise is in MIDDLEWARE

### Database Issues
- Check DATABASE_URL: `heroku config:get DATABASE_URL`
- Run migrations: `heroku run python manage.py migrate`
- Check database connection: `heroku pg:info`

### Application Errors
- Check logs: `heroku logs --tail`
- Ensure all environment variables are set
- Verify Procfile is correct

### Memory Issues
- Upgrade dyno: `heroku ps:type web=standard-1x`
- Check memory usage: `heroku ps`

## Important Files

- **Procfile**: Defines process types (web, release)
- **runtime.txt**: Specifies Python version
- **requirements.txt**: Lists Python dependencies
- **app.json**: App configuration for Heroku
- **.python-version**: Python version for local development

## Cost Optimization

### Free/Eco Dyno
- App sleeps after 30 minutes of inactivity
- First request after sleep takes longer
- Good for testing and development

### Upgrading
```bash
heroku ps:type web=basic
```

## Domain Setup (Optional)

### Add Custom Domain
```bash
heroku domains:add www.yourdomain.com
```

### Configure DNS
Point your domain's CNAME to the DNS target provided by Heroku.

## Monitoring

### Enable Logging
```bash
heroku logs --tail
```

### Papertrail (Optional)
```bash
heroku addons:create papertrail
```

## Security Checklist

- ✅ DEBUG=False in production
- ✅ SECRET_KEY is unique and secret
- ✅ HTTPS enforced (SECURE_SSL_REDIRECT=True)
- ✅ Secure cookies (SESSION_COOKIE_SECURE=True)
- ✅ ALLOWED_HOSTS configured
- ✅ CSRF protection enabled
- ✅ Database uses SSL

## Next Steps After Deployment

1. Test all interview features
2. Verify AI integration works
3. Test video recording and upload
4. Check static files load correctly
5. Monitor logs for any errors
6. Set up custom domain (optional)
7. Configure CDN for better performance (optional)

## Support

For issues with Heroku deployment, check:
- Heroku Dev Center: https://devcenter.heroku.com/
- Django deployment docs: https://docs.djangoproject.com/en/stable/howto/deployment/
- GitHub issues: https://github.com/DanielOnGitHub17/vode/issues
