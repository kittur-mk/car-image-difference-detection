# Streamlit Cloud Deployment Guide

This guide provides specific instructions for deploying your Car Image Difference Detection System to Streamlit Cloud.

## Quick Fix Applied

**Issue**: `ModuleNotFoundError: No module named 'cv2'`
**Solution**: Updated numpy version from 1.24.3 to 1.26.4 to resolve OpenCV dependency conflicts

## Deployment Steps

### 1. Automatic Redeployment (Recommended)

Since the code has been pushed to GitHub, Streamlit Cloud should automatically detect the changes and redeploy. If it doesn't:

1. Go to your Streamlit Cloud dashboard
2. Find your app: `car-image-difference-detection-breay2cg7nvbmaepzpvqgz`
3. Click "Redeploy this app"
4. Wait for the build to complete

### 2. Manual Redeployment

If automatic redeployment doesn't work:

1. **Delete and Recreate**:
   - Delete the existing app
   - Create a new app with the same settings
   - Streamlit will use the updated requirements.txt

2. **Force Rebuild**:
   - Go to app settings
   - Click "Rebuild environment"
   - This forces Streamlit to reinstall all dependencies

## Troubleshooting

### Common Issues and Solutions

#### Issue: OpenCV Installation Failures
**Error**: `ModuleNotFoundError: No module named 'cv2'`
**Solution**: ✅ Fixed - Updated numpy to 1.26.4 for compatibility

#### Issue: YOLOv8 Model Download
**Error**: Model download timeouts or failures
**Solution**: 
- Ensure stable internet connection
- Model will be cached after first download
- Consider using a smaller model if needed

#### Issue: Memory Limitations
**Error**: App crashes or slow performance
**Solution**:
- Reduce image processing batch sizes
- Use smaller input images
- Consider upgrading to paid plan for more resources

### Environment Variables (Optional)

If needed, you can add environment variables in Streamlit Cloud settings:

```
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_HEADLESS=true
```

## Verification

### Test Your Deployment

1. **Check App Status**: Ensure the app shows "Running" status
2. **Test Basic Functionality**: Upload test images and verify processing works
3. **Monitor Logs**: Check for any error messages in the logs

### Pre-Deployment Test

Run this locally to verify dependencies:
```bash
python test_deployment.py
```

## Performance Optimization

### For Better Performance

1. **Image Size**: Keep uploaded images under 2MB for faster processing
2. **Model Caching**: YOLOv8 model is cached after first use
3. **Memory Management**: App automatically manages memory usage

### Resource Usage

- **CPU**: Moderate usage during image processing
- **Memory**: ~500MB-1GB during peak processing
- **Storage**: Temporary file storage for uploaded images

## Support

### If Issues Persist

1. **Check Logs**: Review Streamlit Cloud logs for specific error messages
2. **Test Locally**: Run `python test_deployment.py` to verify dependencies
3. **Create Issue**: Report issues on GitHub repository
4. **Streamlit Support**: Contact Streamlit Cloud support for platform issues

### Contact Information

- **GitHub Repository**: https://github.com/kittur-mk/car-image-difference-detection
- **Documentation**: See DEPLOYMENT.md and README.md
- **Test Script**: Use test_deployment.py for verification

## Success Indicators

✅ **Deployment Successful When**:
- App shows "Running" status in Streamlit Cloud
- No error messages in logs
- Images upload and process correctly
- Similarity scores and visualizations display properly

## Next Steps

1. **Share Your App**: Get the live URL and share with your team
2. **Monitor Usage**: Watch for any performance issues
3. **Gather Feedback**: Collect user feedback for improvements
4. **Scale as Needed**: Upgrade plan if usage increases

---

**🎉 Your Car Image Difference Detection System should now be working on Streamlit Cloud!**

The numpy version fix should resolve the OpenCV import issues. If you continue to experience problems, please check the logs and contact support.