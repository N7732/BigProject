{
  "name": "{{ project_name }}-frontend",
  "version": "{{ version|default:'1.0.0' }}",
  "description": "{{ description|default:'React frontend application' }}",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1",
    "react-router-dom": "^6.8.0",
    "axios": "^1.3.0",
    "react-query": "^3.39.3",
    "framer-motion": "^8.5.0",
    "clsx": "^1.2.1",
    "react-toastify": "^9.1.1",
    "prop-types": "^15.8.1"
  },
  "devDependencies": {
    "@types/react": "^18.0.28",
    "@types/react-dom": "^18.0.11",
    "tailwindcss": "^3.2.0",
    "autoprefixer": "^10.4.13",
    "postcss": "^8.4.21",
    "eslint": "^8.36.0",
    "eslint-plugin-react": "^7.32.2",
    "eslint-plugin-react-hooks": "^4.6.0"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject",
    "lint": "eslint src/**/*.js",
    "lint:fix": "eslint src/**/*.js --fix"
  },
  "eslintConfig": {
    "extends": [
      "react-app",
      "react-app/jest"
    ],
    "rules": {
      "react-hooks/exhaustive-deps": "warn",
      "no-unused-vars": "warn"
    }
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  },
  "proxy": "http://localhost:8000",
  "keywords": [
    "react",
    "frontend",
    "webapp"
  ],
  "author": "{{ author|default:'Your Name' }}",
  "license": "{{ license|default:'MIT' }}"
}