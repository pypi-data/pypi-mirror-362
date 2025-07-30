# Robot Kinematics Documentation

This directory contains the documentation for the Robot Kinematics library, designed to be served via GitHub Pages.

## Files

- `index.html` - Main landing page with overview and features
- `API_REFERENCE.html` - Complete API documentation
- `QUICK_START.html` - Getting started guide
- `TUTORIALS.html` - Advanced tutorials and use cases
- `styles.css` - CSS styling for all pages
- `script.js` - JavaScript for interactive features
- `_config.yml` - Jekyll configuration for GitHub Pages

## Setting Up GitHub Pages

1. **Enable GitHub Pages**:
   - Go to your repository settings
   - Scroll down to "GitHub Pages" section
   - Select "Source" as "Deploy from a branch"
   - Choose "main" branch and "/docs" folder
   - Click "Save"

2. **Push the docs directory**:
   ```bash
   git add docs/
   git commit -m "Add GitHub Pages documentation"
   git push origin main
   ```

3. **Wait for deployment**:
   - GitHub will automatically build and deploy your site
   - You can monitor the deployment in the "Actions" tab
   - Your site will be available at: `https://yourusername.github.io/robot-kinematics`

## Customization

### Updating Content
- Edit the HTML files to update content
- Modify `styles.css` to change appearance
- Update `script.js` for interactive features

### Adding New Pages
1. Create a new HTML file in the docs directory
2. Include the same header structure as existing pages
3. Add navigation links in the navbar
4. Update the footer links if needed

### Styling
The site uses a modern cyberpunk theme with:
- Dark background with neon accents
- Responsive design for mobile devices
- Smooth animations and transitions
- Interactive code copy buttons

## Features

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Interactive Elements**: Code copy buttons, smooth scrolling, animations
- **Modern UI**: Dark theme with neon blue and pink accents
- **Comprehensive Documentation**: API reference, tutorials, and examples
- **Search Engine Optimized**: Proper meta tags and structure

## Local Development

To test the site locally:

1. **Simple HTTP Server**:
   ```bash
   cd docs
   python -m http.server 8000
   ```
   Then visit `http://localhost:8000`

2. **Using Jekyll** (if you have Ruby installed):
   ```bash
   cd docs
   bundle install
   bundle exec jekyll serve
   ```
   Then visit `http://localhost:4000`

## Troubleshooting

### Common Issues

1. **Site not updating**: GitHub Pages can take a few minutes to deploy changes
2. **Styling issues**: Make sure all CSS and JS files are properly linked
3. **Broken links**: Check that all internal links use relative paths

### GitHub Pages Limitations

- Only static content is supported (HTML, CSS, JS)
- No server-side processing
- Limited to 1GB repository size
- Build time limits apply

## Contributing

To contribute to the documentation:

1. Fork the repository
2. Make your changes in the docs directory
3. Test locally to ensure everything works
4. Submit a pull request

## License

The documentation is licensed under the same MIT license as the main project. 