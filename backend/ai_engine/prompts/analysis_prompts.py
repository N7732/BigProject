REQUIREMENT_ANALYSIS_PROMPT = """
As a full-stack web development expert, analyze the following user requirements:

{user_input}

Please provide a comprehensive analysis in JSON format with the following structure:

{{
  "project_overview": "Brief description of the project",
  "required_features": ["list", "of", "core", "features"],
  "suggested_tech_stack": {{
    "frontend": "recommended framework",
    "backend": "recommended framework", 
    "database": "recommended database",
    "authentication": "recommended method"
  }},
  "database_requirements": {{
    "models": ["list", "of", "required", "data", "models"],
    "relationships": "description of model relationships"
  }},
  "api_endpoints": ["list", "of", "required", "endpoints"],
  "ui_ux_specifications": {{
    "style_preference": "modern/classic/minimal/etc",
    "responsive_design": true/false,
    "key_components": ["list", "of", "ui", "components"]
  }},
  "missing_information": ["list", "of", "unclear", "or", "missing", "details"],
  "complexity_assessment": "low/medium/high",
  "estimated_development_time": "rough time estimate"
}}

Focus on identifying gaps in requirements and suggesting optimal technical solutions.
"""