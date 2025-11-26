<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <link rel="icon" href="%PUBLIC_URL%/favicon.ico" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta
      name="description"
      content="{{ project_name }} - A modern React application"
    />
    <meta name="keywords" content="{{ keywords|default:'react,application,web' }}" />
    <meta name="author" content="{{ author|default:'Your Name' }}" />
    
    <!-- Open Graph Meta Tags -->
    <meta property="og:title" content="{{ project_name }}" />
    <meta property="og:description" content="{{ project_description|default:'A modern React application' }}" />
    <meta property="og:type" content="website" />
    
    <link rel="apple-touch-icon" href="%PUBLIC_URL%/logo192.png" />
    <link rel="manifest" href="%PUBLIC_URL%/manifest.json" />
    
    <!-- Preconnect to external domains -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    
    <title>{{ project_name }}</title>
    
    <style>
      /* Loading styles */
      .loading-spinner {
        border: 3px solid #f3f3f3;
        border-top: 3px solid #3498db;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
        margin: 20px auto;
      }
      
      @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
      }
    </style>
  </head>
  <body>
    <noscript>
      <div style="text-align: center; padding: 50px; font-family: Arial, sans-serif;">
        <h1>JavaScript Required</h1>
        <p>You need to enable JavaScript to run this application.</p>
      </div>
    </noscript>
    
    <!-- Loading screen -->
    <div id="loading-screen" style="
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: white;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      z-index: 9999;
      transition: opacity 0.3s ease;
    ">
      <div class="loading-spinner"></div>
      <p style="margin-top: 20px; color: #666; font-family: Inter, sans-serif;">
        Loading {{ project_name }}...
      </p>
    </div>
    
    <div id="root"></div>
    
    <script>
      // Hide loading screen when React app loads
      window.addEventListener('load', function() {
        const loadingScreen = document.getElementById('loading-screen');
        if (loadingScreen) {
          loadingScreen.style.opacity = '0';
          setTimeout(() => {
            loadingScreen.style.display = 'none';
          }, 300);
        }
      });
    </script>
  </body>
</html>