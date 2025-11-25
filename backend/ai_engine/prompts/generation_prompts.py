CODE_GENERATION_PROMPT = """
Based on the following project specifications:

{specifications}

Generate complete, working code for the project. Structure your response with clear sections:

**FRONTEND_SETUP**
Create the main frontend application structure with:
- Package.json with all dependencies
- Main App component
- Routing setup if needed
- Basic styling configuration

**BACKEND_SETUP** 
Create the backend application structure with:
- Main application entry point
- Database models and configuration
- API routes and controllers
- Middleware and security setup

**AUTHENTICATION_SYSTEM**
Implement complete authentication with:
- User model and registration
- Login/logout functionality
- Protected routes/components
- Token/session management

**KEY_COMPONENTS**
Create the main UI components with:
- Clean, modern design
- Responsive layout
- Proper state management
- Error handling

**DATABASE_SCHEMA**
Define complete database structure with:
- Model definitions
- Relationships and constraints
- Migration scripts if applicable

**DEPLOYMENT_CONFIG**
Provide deployment configuration with:
- Environment variables
- Build scripts
- Server configuration

Ensure all code is production-ready, follows best practices, includes error handling, and is properly documented.
"""