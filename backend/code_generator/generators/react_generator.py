import os
from typing import Dict, List, Any
from .base_generator import BaseGenerator
from ..templates.react import (
    REACT_PACKAGE_JSON, REACT_APP_JS, REACT_INDEX_HTML,
    REACT_COMPONENT, REACT_STYLES, REACT_ROUTER_SETUP
)

class ReactGenerator(BaseGenerator):
    """React.js frontend generator"""
    
    def __init__(self):
        super().__init__()
        self.framework_name = "react"
        self.supported_features = [
            'components', 'routing', 'state_management', 'api_integration',
            'authentication', 'responsive_design'
        ]
    
    def generate_project_structure(self, specifications: Dict[str, Any]) -> Dict[str, str]:
        """Generate complete React project structure"""
        files = {}
        
        # Package.json
        files['package.json'] = self._generate_package_json(specifications)
        
        # Main app files
        files.update(self.generate_main_files(specifications))
        
        # Components
        files.update(self._generate_components(specifications))
        
        # Styles
        files.update(self._generate_styles(specifications))
        
        # Configuration files
        files.update(self.generate_config_files(specifications))
        
        return files
    
    def generate_main_files(self, specifications: Dict[str, Any]) -> Dict[str, str]:
        """Generate main React application files"""
        files = {}
        
        project_name = specifications.get('project_name', 'my-react-app')
        
        # Public/index.html
        files['public/index.html'] = REACT_INDEX_HTML.format(
            project_name=project_name,
            title=specifications.get('title', 'React App')
        )
        
        # Source files
        files['src/App.js'] = REACT_APP_JS.format(
            components=self._get_component_imports(specifications),
            routes=self._get_routes_setup(specifications)
        )
        
        files['src/index.js'] = """
import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
"""
        
        files['src/index.css'] = REACT_STYLES.format(
            primary_color=specifications.get('primary_color', '#007acc')
        )
        
        return files
    
    def _generate_package_json(self, specifications: Dict[str, Any]) -> str:
        """Generate package.json content"""
        dependencies = {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-scripts": "5.0.1"
        }
        
        # Add additional dependencies based on features
        if 'routing' in specifications.get('features', []):
            dependencies["react-router-dom"] = "^6.8.0"
        
        if 'state_management' in specifications.get('features', []):
            dependencies["redux"] = "^4.2.1"
            dependencies["react-redux"] = "^8.0.5"
        
        return REACT_PACKAGE_JSON.format(
            project_name=specifications.get('project_name', 'my-react-app'),
            dependencies=self._format_dependencies(dependencies),
            additional_scripts=self._get_additional_scripts(specifications)
        )
    
    def _generate_components(self, specifications: Dict[str, Any]) -> Dict[str, str]:
        """Generate React components based on specifications"""
        components = {}
        features = specifications.get('features', [])
        
        if 'authentication' in features:
            components['src/components/Login.js'] = REACT_COMPONENT.format(
                component_name="Login",
                props="",
                content="""
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    
    const handleSubmit = (e) => {
        e.preventDefault();
        // Authentication logic here
        console.log('Login attempted:', email, password);
    };
    
    return (
        <div className="login-container">
            <h2>Login</h2>
            <form onSubmit={handleSubmit}>
                <input 
                    type="email" 
                    placeholder="Email" 
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required 
                />
                <input 
                    type="password" 
                    placeholder="Password" 
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required 
                />
                <button type="submit">Login</button>
            </form>
        </div>
    );
"""
            )
        
        if 'dashboard' in features:
            components['src/components/Dashboard.js'] = REACT_COMPONENT.format(
                component_name="Dashboard",
                props="",
                content="""
    const [data, setData] = useState([]);
    
    useEffect(() => {
        // Fetch dashboard data
        // fetchData().then(setData);
    }, []);
    
    return (
        <div className="dashboard">
            <h1>Dashboard</h1>
            <div className="stats-grid">
                <div className="stat-card">Total Users: 0</div>
                <div className="stat-card">Revenue: $0</div>
                <div className="stat-card">Growth: 0%</div>
            </div>
        </div>
    );
"""
            )
        
        # Default components
        components['src/components/Header.js'] = REACT_COMPONENT.format(
            component_name="Header",
            props="",
            content="""
    return (
        <header className="app-header">
            <h1>{props.title || 'My React App'}</h1>
            <nav>
                <a href="/">Home</a>
                <a href="/about">About</a>
                <a href="/contact">Contact</a>
            </nav>
        </header>
    );
"""
        )
        
        components['src/components/Footer.js'] = REACT_COMPONENT.format(
            component_name="Footer",
            props="",
            content="""
    return (
        <footer className="app-footer">
            <p>&copy; 2024 My React App. All rights reserved.</p>
        </footer>
    );
"""
        )
        
        return components
    
    def _generate_styles(self, specifications: Dict[str, Any]) -> Dict[str, str]:
        """Generate CSS styles"""
        styles = {}
        
        primary_color = specifications.get('primary_color', '#007acc')
        secondary_color = specifications.get('secondary_color', '#6c757d')
        
        styles['src/App.css'] = f"""
/* Main App Styles */
.app {{
  text-align: center;
}}

.app-header {{
  background-color: {primary_color};
  padding: 20px;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
}}

.app-footer {{
  background-color: {secondary_color};
  color: white;
  padding: 10px;
  position: fixed;
  bottom: 0;
  width: 100%;
}}

/* Component Styles */
.login-container {{
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
}}

.login-container input {{
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  border: 1px solid #ccc;
  border-radius: 4px;
}}

.login-container button {{
  width: 100%;
  padding: 10px;
  background-color: {primary_color};
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}}

.dashboard {{
  padding: 20px;
}}

.stats-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin: 20px 0;
}}

.stat-card {{
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  text-align: center;
}}
"""
        return styles
    
    def _get_component_imports(self, specifications: Dict[str, Any]) -> str:
        """Generate component imports based on features"""
        imports = []
        features = specifications.get('features', [])
        
        if 'authentication' in features:
            imports.append("import Login from './components/Login';")
        
        if 'dashboard' in features:
            imports.append("import Dashboard from './components/Dashboard';")
        
        imports.extend([
            "import Header from './components/Header';",
            "import Footer from './components/Footer';"
        ])
        
        return '\n'.join(imports)
    
    def _get_routes_setup(self, specifications: Dict[str, Any]) -> str:
        """Generate React Router setup"""
        features = specifications.get('features', [])
        
        if 'routing' not in features:
            return """
      <div className="app">
        <Header title="My React App" />
        <main>
          <h1>Welcome to React App</h1>
          <p>This is your generated React application.</p>
        </main>
        <Footer />
      </div>
"""
        
        return """
      <Router>
        <div className="app">
          <Header title="My React App" />
          <main>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/about" element={<About />} />
              <Route path="/contact" element={<Contact />} />
            </Routes>
          </main>
          <Footer />
        </div>
      </Router>
"""
    
    def _format_dependencies(self, dependencies: Dict[str, str]) -> str:
        """Format dependencies for package.json"""
        items = []
        for dep, version in dependencies.items():
            items.append(f'    "{dep}": "{version}"')
        return ',\n'.join(items)
    
    def _get_additional_scripts(self, specifications: Dict[str, Any]) -> str:
        """Get additional npm scripts"""
        scripts = []
        if 'testing' in specifications.get('features', []):
            scripts.append('    "test": "react-scripts test",')
            scripts.append('    "test:coverage": "react-scripts test --coverage",')
        
        scripts.append('    "build": "react-scripts build",')
        scripts.append('    "eject": "react-scripts eject"')
        
        return ',\n'.join(scripts)