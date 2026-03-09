# Deployment Guide

This guide provides step-by-step instructions for deploying your Car Image Difference Detection System to various cloud platforms.

## Quick Start

### Option 1: Streamlit Cloud (Easiest - Recommended)

1. **Create Account**: Go to [Streamlit Cloud](https://streamlit.io/cloud) and sign up for free
2. **Connect Repository**: 
   - Click "New App"
   - Connect your GitHub repository: `kittur-mk/car-image-difference-detection`
   - Select branch: `main`
   - Main file path: `app.py`
3. **Configure Settings**:
   - Python version: `3.10`
   - Requirements file: `requirements.txt`
4. **Deploy**: Click "Deploy" and wait for the build to complete
5. **Access**: Your app will be available at `https://your-username-car-image-difference-detection.streamlit.app`

### Option 2: Heroku (Free Tier Available)

1. **Install Heroku CLI**: Download from [heroku.com](https://devcenter.heroku.com/articles/heroku-cli)
2. **Login to Heroku**:
   ```bash
   heroku login
   ```
3. **Create App**:
   ```bash
   heroku create your-app-name
   ```
4. **Set Python Buildpack**:
   ```bash
   heroku buildpacks:set heroku/python
   ```
5. **Deploy**:
   ```bash
   git push heroku main
   ```
6. **Open App**:
   ```bash
   heroku open
   ```

### Option 3: Railway (Alternative to Heroku)

1. **Sign up**: Go to [Railway.app](https://railway.app) and connect your GitHub
2. **Deploy from GitHub**: Select your repository
3. **Configure**: Railway will automatically detect the Python app and requirements.txt
4. **Deploy**: Click deploy and wait for completion

## Detailed Deployment Instructions

### Streamlit Cloud Configuration

**Environment Variables** (if needed):
- No special environment variables required for basic functionality

**File Structure Requirements**:
```
car-image-difference-detection/
├── app.py              # Main application (required)
├── requirements.txt    # Dependencies (required)
├── README.md          # Documentation (optional but recommended)
└── modules/           # Your modules (included automatically)
```

**Performance Considerations**:
- Streamlit Cloud provides free tier with limited resources
- For production use, consider upgrading to paid plans
- Large image uploads may be limited on free tier

### Heroku Configuration

**Additional Files Needed**:
- `Procfile` (already created)
- `runtime.txt` (specifies Python version)

**Procfile Content**:
```
web: streamlit run app.py --server.port=$PORT
```

**Runtime.txt Content**:
```
python-3.10.12
```

**Environment Variables**:
```bash
# Optional: Set Streamlit configuration
heroku config:set STREAMLIT_SERVER_PORT=$PORT
heroku config:set STREAMLIT_SERVER_HEADLESS=true
```

**Build Process**:
1. Heroku reads `requirements.txt` and installs dependencies
2. Executes the `Procfile` command to start the application
3. Streamlit runs on the specified port

### Docker Deployment

**Build and Run Locally**:
```bash
# Build the Docker image
docker build -t car-difference-detector .

# Run the container
docker run -p 8501:8501 car-difference-detector
```

**Deploy to Docker Hub**:
```bash
# Tag your image
docker tag car-difference-detector your-dockerhub-username/car-difference-detector:latest

# Push to Docker Hub
docker push your-dockerhub-username/car-difference-detector:latest
```

**Deploy to Cloud Platforms**:
- **AWS ECS**: Use Docker image for container deployment
- **Google Cloud Run**: Deploy container directly
- **Azure Container Instances**: Simple container deployment

## Platform-Specific Considerations

### Image Processing Requirements

**Memory Requirements**:
- YOLOv8 model loading requires ~500MB-1GB RAM
- Image processing benefits from more memory
- Consider platform memory limits

**Storage**:
- Temporary file storage for uploaded images
- Most platforms provide ephemeral storage
- Consider external storage for persistent data

**Processing Power**:
- YOLOv8 inference benefits from CPU/GPU
- Free tiers may have limited processing power
- Consider upgrading for better performance

### Security Considerations

**File Uploads**:
- Validate uploaded file types (images only)
- Set size limits for uploaded files
- Consider virus scanning for production

**Environment Variables**:
- Store sensitive configuration in environment variables
- Never commit API keys or secrets to repository

**HTTPS**:
- All deployment platforms provide HTTPS by default
- Ensure your application works with HTTPS

## Troubleshooting

### Common Issues

**Import Errors**:
- Ensure all dependencies are in `requirements.txt`
- Check Python version compatibility
- Verify module paths are correct

**Memory Issues**:
- Reduce image processing batch sizes
- Consider lazy loading of models
- Monitor memory usage on deployment platform

**Performance Issues**:
- Optimize image sizes before processing
- Cache model loading when possible
- Consider model quantization for faster inference

### Debugging

**Local Testing**:
```bash
# Test locally before deploying
streamlit run app.py

# Check for import errors
python -c "import modules.detection; print('Import successful')"
```

**Platform Logs**:
- Streamlit Cloud: View logs in dashboard
- Heroku: `heroku logs --tail`
- Railway: View logs in dashboard

## Monitoring and Maintenance

### Performance Monitoring

**Key Metrics**:
- Response time for image processing
- Memory usage during processing
- Error rates and types

**Tools**:
- Platform-specific monitoring dashboards
- Custom logging in your application
- External monitoring services

### Updates and Maintenance

**Code Updates**:
- Push to GitHub triggers automatic redeployment (Streamlit Cloud)
- Manual deployment required for some platforms
- Test changes locally before pushing

**Dependency Updates**:
- Regularly update dependencies in `requirements.txt`
- Test compatibility with new versions
- Consider security updates

## Cost Considerations

### Free Tier Options
- **Streamlit Cloud**: Free tier available, limited resources
- **Heroku**: Free tier with sleep mode
- **Railway**: Generous free tier

### Paid Options
- **Streamlit Cloud Pro**: $0.30/hour
- **Heroku Hobby**: $7/month
- **Railway Hobby**: $5/month

### Cost Optimization
- Use appropriate resource tiers
- Monitor usage and scale accordingly
- Consider shutting down when not in use

## Next Steps

1. **Choose Deployment Platform**: Based on your needs and budget
2. **Test Deployment**: Ensure everything works correctly
3. **Monitor Performance**: Watch for any issues
4. **Scale as Needed**: Upgrade resources based on usage
5. **Maintain**: Keep dependencies updated and monitor for issues

For additional support:
- Check the [Streamlit Documentation](https://docs.streamlit.io)
- Review [Heroku Python Guide](https://devcenter.heroku.com/categories/python-support)
- Visit the project's [GitHub Issues](https://github.com/kittur-mk/car-image-difference-detection/issues)