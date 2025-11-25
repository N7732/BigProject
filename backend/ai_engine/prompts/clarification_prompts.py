CLARIFICATION_PROMPT = """
Based on the current project specifications:

{current_specs}

Generate 3-5 specific, technical clarifying questions to fill in the missing information. 
Focus on questions that will significantly impact the technical implementation.

Consider asking about:
- Specific technology preferences (frameworks, databases, etc.)
- Authentication and authorization requirements
- Data models and relationships
- UI/UX design preferences
- Performance and scalability requirements
- Integration with external services
- Deployment environment constraints

Format your response as a list of clear, concise questions, one per line.
Each question should be technical and specific to web development.
"""