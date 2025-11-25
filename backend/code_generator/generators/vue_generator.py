from typing import Dict, Any
from .base_generator import BaseGenerator

class VueGenerator(BaseGenerator):
    """Vue.js frontend generator"""
    
    def __init__(self):
        super().__init__()
        self.framework_name = "vue"
        self.supported_features = [
            'components', 'routing', 'state_management', 'composition_api'
        ]
    
    def generate_project_structure(self, specifications: Dict[str, Any]) -> Dict[str, str]:
        """Generate complete Vue project structure"""
        return {
            'package.json': self._generate_package_json(specifications),
            'src/main.js': self._generate_main_js(specifications),
            'src/App.vue': self._generate_app_vue(specifications),
            'public/index.html': self._generate_index_html(specifications)
        }
    
    def generate_main_files(self, specifications: Dict[str, Any]) -> Dict[str, str]:
        """Generate main Vue application files"""
        return {}
    
    def _generate_package_json(self, specifications: Dict[str, Any]) -> str:
        """Generate Vue package.json"""
        return """{
  "name": "vue-app",
  "version": "1.0.0",
  "scripts": {
    "serve": "vue-cli-service serve",
    "build": "vue-cli-service build"
  },
  "dependencies": {
    "vue": "^3.3.0",
    "vue-router": "^4.2.0"
  },
  "devDependencies": {
    "@vue/cli-service": "^5.0.0"
  }
}"""
    
    def _generate_main_js(self, specifications: Dict[str, Any]) -> str:
        """Generate main.js"""
        return """import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

createApp(App).use(router).mount('#app')
"""
    
    def _generate_app_vue(self, specifications: Dict[str, Any]) -> str:
        """Generate App.vue"""
        return """<template>
  <div id="app">
    <nav>
      <router-link to="/">Home</router-link>
      <router-link to="/about">About</router-link>
    </nav>
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
}
</style>
"""
    
    def _generate_index_html(self, specifications: Dict[str, Any]) -> str:
        """Generate index.html"""
        return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Vue App</title>
</head>
<body>
  <div id="app"></div>
</body>
</html>
"""