#!/usr/bin/env python3
"""
Project Security Validator
Run comprehensive security validation on generated projects
"""

import os
import sys
import json
import argparse
from pathlib import Path

def setup_paths():
    """Setup Python paths to import validators"""
    # Get the directory containing this script
    current_dir = Path(__file__).parent
    # Add the parent directory to Python path (to import validators)
    parent_dir = current_dir.parent
    if str(parent_dir) not in sys.path:
        sys.path.insert(0, str(parent_dir))

def load_context_from_file(context_file):
    """Load context from JSON file"""
    try:
        with open(context_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading context file: {e}")
        return None

def main():
    """Main validation function"""
    parser = argparse.ArgumentParser(description='Validate generated project for security issues')
    parser.add_argument('project_path', help='Path to the generated project directory')
    parser.add_argument('--context', help='JSON context string used for generation')
    parser.add_argument('--context-file', help='Path to JSON file containing context')
    parser.add_argument('--output', '-o', help='Output file for detailed report (default: security_report.json)')
    parser.add_argument('--min-score', type=int, default=80, help='Minimum security score to pass (default: 80)')
    parser.add_argument('--no-color', action='store_true', help='Disable colored output')
    
    args = parser.parse_args()
    
    # Setup paths
    setup_paths()
    
    # Import validators (after path setup)
    try:
        from code_generator.validators import validate_complete_project
    except ImportError as e:
        print(f"Error importing validators: {e}")
        print("Make sure you're running this from the correct directory")
        sys.exit(1)
    
    # Load context
    context = {}
    if args.context_file:
        context = load_context_from_file(args.context_file)
        if context is None:
            sys.exit(1)
    elif args.context:
        try:
            context = json.loads(args.context)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON context: {e}")
            sys.exit(1)
    
    # Validate project path exists
    project_path = Path(args.project_path)
    if not project_path.exists():
        print(f"Error: Project path does not exist: {project_path}")
        sys.exit(1)
    
    if not project_path.is_dir():
        print(f"Error: Project path is not a directory: {project_path}")
        sys.exit(1)
    
    print(f"🔍 Starting security validation for: {project_path}")
    print("=" * 60)
    
    # Run comprehensive validation
    try:
        report = validate_complete_project(str(project_path), context)
    except Exception as e:
        print(f"Error during validation: {e}")
        sys.exit(1)
    
    # Display results
    display_results(report, args.min_score, args.no_color)
    
    # Save detailed report
    output_file = args.output or project_path / 'security_report.json'
    save_detailed_report(report, output_file)
    
    # Exit with appropriate code
    summary = report['summary']
    if summary['passed'] and summary['security_score'] >= args.min_score:
        sys.exit(0)
    else:
        sys.exit(1)

def display_results(report, min_score, no_color):
    """Display validation results in a user-friendly format"""
    summary = report['summary']
    
    print("\n📊 VALIDATION RESULTS")
    print("=" * 60)
    
    # Security score with color coding
    score = summary['security_score']
    score_color = (
        "🟢" if score >= 90 else
        "🟡" if score >= 80 else
        "🟠" if score >= 70 else
        "🔴"
    )
    
    print(f"{score_color} Security Score: {score}/100 (Minimum: {min_score})")
    
    if summary['passed'] and score >= min_score:
        print("✅ PROJECT PASSED SECURITY VALIDATION")
    else:
        print("❌ PROJECT FAILED SECURITY VALIDATION")
    
    # Issues breakdown
    print(f"\n📈 ISSUES BREAKDOWN:")
    print(f"   🔴 Critical: {summary['critical_issues']}")
    print(f"   🟠 High: {len(report['security_scan'].get('high_issues', []))}")
    print(f"   🟡 Medium: {len(report['security_scan'].get('medium_issues', []))}")
    print(f"   🔵 Low: {len(report['security_scan'].get('low_issues', []))}")
    print(f"   📊 Total: {summary['total_issues']}")
    
    # Display critical issues
    critical_issues = report['security_scan'].get('critical_issues', [])
    if critical_issues:
        print(f"\n🚨 CRITICAL ISSUES ({len(critical_issues)}):")
        for i, issue in enumerate(critical_issues[:10], 1):  # Show first 10
            print(f"   {i}. {issue['message']}")
            print(f"      📁 File: {issue['file']}:{issue['line']}")
            if issue.get('code'):
                code_preview = issue['code'][:100] + '...' if len(issue['code']) > 100 else issue['code']
                print(f"      📝 Code: {code_preview}")
            print()
    
    # Display high issues (first 5)
    high_issues = report['security_scan'].get('high_issues', [])
    if high_issues:
        print(f"⚠️  HIGH ISSUES (showing first 5 of {len(high_issues)}):")
        for i, issue in enumerate(high_issues[:5], 1):
            print(f"   {i}. {issue['message']}")
            print(f"      📁 File: {issue['file']}:{issue['line']}")
            print()
    
    # Display recommendations
    recommendations = report['security_scan'].get('recommendations', [])
    if recommendations:
        print(f"💡 RECOMMENDATIONS ({len(recommendations)}):")
        for i, rec in enumerate(recommendations, 1):
            print(f"   {i}. {rec}")
    
    # Dependency issues
    dep_check = report.get('dependency_check', {})
    if dep_check:
        dep_summary = dep_check.get('summary', {})
        if dep_summary.get('vulnerable_packages', 0) > 0:
            print(f"\n📦 DEPENDENCY ISSUES:")
            print(f"   Vulnerable packages: {dep_summary.get('vulnerable_packages', 0)}")
            print(f"   Suspicious packages: {dep_summary.get('suspicious_packages', 0)}")
    
    # Syntax validation summary
    syntax_results = report.get('syntax_validation', {})
    if syntax_results:
        total_syntax_issues = sum(
            file_result.get('summary', {}).get('total_issues', 0)
            for file_result in syntax_results.values()
        )
        if total_syntax_issues > 0:
            print(f"\n🔧 SYNTAX ISSUES: {total_syntax_issues} total across {len(syntax_results)} files")

def save_detailed_report(report, output_file):
    """Save detailed report to file"""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"📄 Detailed report saved to: {output_file}")
    except Exception as e:
        print(f"Warning: Could not save report to {output_file}: {e}")

if __name__ == "__main__":
    main()