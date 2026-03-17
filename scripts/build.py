#!/usr/bin/env python3
import json
import yaml
import shutil
import re
import argparse
import sys
from pathlib import Path
from collections import defaultdict

# Try to import interactive selection library
try:
    import questionary
    HAS_QUESTIONARY = True
except ImportError:
    HAS_QUESTIONARY = False
    print("Note: Install 'questionary' for interactive skill selection: pip install questionary")

def generate_readme(root_dir: Path, all_agents_data: list):
    """Generates the README.md from a template and the agent data."""
    print("Generating README.md...")
    template_path = root_dir /  'README.template.md'
    readme_path = root_dir /  'README.md'
    
    # Filter for skills only for the README
    skills_only = [a for a in all_agents_data if a.get('type') == 'skill']

    # Group skills by inferred category based on naming patterns
    skills_by_category = defaultdict(list)
    
    # Category mapping based on skill name prefixes/patterns
    category_mapping = {
        'api': 'architecture', 'database': 'architecture', 'system': 'architecture', 'tech-stack': 'architecture', 'feature-spec': 'architecture',
        'code': 'code-quality', 'documentation': 'code-quality', 'performance': 'code-quality', 'refactoring': 'code-quality', 'security': 'code-quality', 'test': 'code-quality',
        'brand': 'design', 'color': 'design', 'design-system': 'design', 'icon': 'design', 'layout': 'design', 'typography': 'design', 'ui': 'design', 'wireframe': 'design',
        'ad': 'marketing', 'blog': 'marketing', 'copy': 'marketing', 'email': 'marketing', 'landing': 'marketing', 'seo': 'marketing', 'social': 'marketing',
        'accessibility': 'product', 'competitor': 'product', 'feature-prioritizer': 'product', 'feedback': 'product', 'user-story': 'product', 'ux': 'product',
        'business': 'business', 'financial': 'business', 'market-research': 'business', 'pricing': 'business', 'privacy': 'business', 'terms': 'business',
        'backup': 'devops', 'cost': 'devops', 'deployment': 'devops', 'error': 'devops', 'monitoring': 'devops',
        'analytics': 'data', 'dashboard': 'data', 'data-visualizer': 'data', 'report': 'data', 'sql': 'data',
        'api-documenter': 'communication', 'changelog': 'communication', 'presentation': 'communication', 'support': 'communication', 'team': 'communication', 'technical-writer': 'communication',
        'best-practice': 'research', 'library': 'research', 'solution': 'research', 'technology': 'research', 'trend': 'research',
        'agile': 'project-management', 'project': 'project-management',
    }
    
    for skill in skills_only:
        skill_name = skill['name']
        # Determine category based on name patterns
        category = 'skills'  # default
        for prefix, cat in category_mapping.items():
            if skill_name.startswith(prefix) or prefix in skill_name:
                category = cat
                break
        skills_by_category[category].append(skill)
        
    # --- Generate the markdown list ---
    # Define the desired order of categories
    category_order = [
        "architecture", "code-quality", "design", "marketing", "product", 
        "business", "devops", "data", "communication", "research", "project-management", "skills"
    ]
    
    # Descriptions for each category
    category_descriptions = {
        "architecture": "The masterminds who design your digital empire",
        "code-quality": "The guardians of clean, secure, and blazing-fast code",
        "design": "The creative geniuses who make everything beautiful",
        "marketing": "The word wizards who turn features into must-haves",
        "product": "The user champions who build products people actually want",
        "business": "The suit-wearing strategists who keep the lights on",
        "devops": "The infrastructure heroes who keep your app running while you sleep",
        "data": "The number crunchers who turn chaos into insights",
        "communication": "The translators who make tech speak human",
        "research": "The curious minds who keep you ahead of the curve",
        "project-management": "The organizers who ensure on-time and on-budget delivery",
        "skills": "Specialized AI skills for common development tasks"
    }

    md_parts = ["## 🤖 Your AI Dream Team\n\n*Meet your new coding sidekicks - each one a specialist in their field:*"]
    
    total_skills = 0
    for category in category_order:
        if category in skills_by_category:
            skills = sorted(skills_by_category[category], key=lambda x: x['name'])
            total_skills += len(skills)
            md_parts.append(f"\n### 🏗️ {category.capitalize().replace('-', ' ')} ({len(skills)} skills)")
            md_parts.append(f"*{category_descriptions.get(category, '')}*")
            for skill in skills:
                # Extract first sentence of description for brief info
                desc = skill['description'].split('.')[0] if skill['description'] else f"A specialist in {skill['name'].replace('-', ' ')}"
                md_parts.append(f"- **{skill['name']}** - {desc}.")
    
    agent_list_md = "\n".join(md_parts)

    # Replace placeholder in template
    template_content = template_path.read_text(encoding='utf-8')
    readme_content = template_content.replace('{{AGENT_LIST}}', agent_list_md)
    
    # Update total agent count
    readme_content = re.sub(r'Meet \d+ specialized AI agents', f'Meet {total_skills} specialized AI skills', readme_content)
    readme_content = re.sub(r'it\'s like having \d+ AI specialists', f'it\'s like having {total_skills} AI specialists', readme_content)


    readme_path.write_text(readme_content, encoding='utf-8')
    print("Successfully generated README.md")

def generate_platform_md(dist_dir: Path, all_skills_data: list, platform: str):
    """Generates PLATFORM.md (e.g. CLAUDE.md) for the given platform."""
    filename = 'CLAUDE.md' if platform == 'claude' else f'{platform.upper()}.md'
    md_path = dist_dir / filename

    content = [f"# {filename}\n"]
    content.append(f"Master configuration for {platform.capitalize()} Code. This file indexes available Skills.\n")

    content.append("\n# Project Standards\n")
    content.append("<!-- Add project-wide standards here (e.g., framework conventions, code quality, accessibility) -->\n")
    content.append("- Follow the coding style defined in the project.\n")

    content.append("\n# Available Skills\n")
    content.append(f"*{len(all_skills_data)} skills ready to use*\n")

    # Group skills by category
    skills_by_category = defaultdict(list)
    for skill in all_skills_data:
        skills_by_category[skill['category']].append(skill)
    
    # Define category order
    category_order = [
        "architecture", "code-quality", "design", "marketing", "product", 
        "business", "devops", "data", "communication", "research", "project-management", "skills"
    ]
    
    for category in category_order:
        if category in skills_by_category:
            skills = sorted(skills_by_category[category], key=lambda x: x['name'])
            content.append(f"\n## {category.capitalize().replace('-', ' ')}\n")
            for skill in skills:
                content.append(f"- `/{skill['name']}` - {skill['description']}")

    md_path.write_text("\n".join(content), encoding='utf-8')

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Build script for AI Coding Agents Skills.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Build all skills for Claude (default)
  python3 scripts/build.py --all
  
  # Build specific skills
  python3 scripts/build.py --skills=api-designer,code-reviewer,ui-designer
  
  # Interactive skill selection (if questionary is installed)
  python3 scripts/build.py
  
  # Build all skills for Gemini
  python3 scripts/build.py --all --platform=gemini
        """
    )
    parser.add_argument(
        "--platform",
        choices=["claude", "gemini", "codex", "junie"],
        default="claude",
        help="Target AI platform for skill generation. (default: claude)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Include all skills in the build.",
    )
    parser.add_argument(
        "--skills",
        type=str,
        help="Comma-separated list of specific skills to include (e.g., 'api-designer,code-reviewer').",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all available skills and exit.",
    )
    return parser.parse_args()


def get_all_skills(skills_dir: Path) -> list:
    """Get list of all available skills from the skills directory."""
    skills = []
    if not skills_dir.exists():
        return skills
    
    for skill_dir in skills_dir.iterdir():
        if skill_dir.is_dir() and not skill_dir.name.startswith('.'):
            skill_file = skill_dir / "SKILL.md"
            if skill_file.exists():
                category = _infer_category_from_skill_name(skill_dir.name)
                skills.append({
                    'name': skill_dir.name,
                    'category': category,
                    'path': skill_dir
                })
    
    return sorted(skills, key=lambda x: (x['category'], x['name']))


def list_all_skills(skills: list):
    """Print a formatted list of all available skills."""
    print("\n" + "="*60)
    print("📋 AVAILABLE SKILLS")
    print("="*60)
    
    # Group by category
    by_category = defaultdict(list)
    for skill in skills:
        by_category[skill['category']].append(skill)
    
    category_order = [
        "architecture", "code-quality", "design", "marketing", "product", 
        "business", "devops", "data", "communication", "research", "project-management", "skills"
    ]
    
    for category in category_order:
        if category in by_category:
            cat_skills = by_category[category]
            print(f"\n📁 {category.upper().replace('-', ' ')}")
            print("-" * 40)
            for skill in cat_skills:
                print(f"   • {skill['name']}")
    
    print(f"\n{'='*60}")
    print(f"Total: {len(skills)} skills available")
    print("="*60 + "\n")


def interactive_skill_selector(skills: list) -> list:
    """Interactive skill selection using checkboxes."""
    if not HAS_QUESTIONARY:
        print("\n⚠️  Interactive selection requires 'questionary' library.")
        print("   Install it with: pip install questionary")
        print("\n   Falling back to building ALL skills...\n")
        return skills
    
    # Group skills by category for better organization
    by_category = defaultdict(list)
    for skill in skills:
        by_category[skill['category']].append(skill)
    
    category_order = [
        "architecture", "code-quality", "design", "marketing", "product", 
        "business", "devops", "data", "communication", "research", "project-management", "skills"
    ]
    
    # Build choices grouped by category
    choices = []
    for category in category_order:
        if category in by_category:
            # Add category header as separator (disabled item)
            choices.append(questionary.Separator(f"\n📁 {category.upper().replace('-', ' ')}"))
            # Add skills in this category
            for skill in sorted(by_category[category], key=lambda x: x['name']):
                choices.append({
                    'name': f"  {skill['name']}",
                    'value': skill['name'],
                    'checked': False
                })
    
    print("\n" + "="*60)
    print("🎯 SKILL SELECTOR")
    print("="*60)
    print("\nUse ↑/↓ to navigate, SPACE to select/deselect, ENTER to confirm.")
    print("Select the skills you want to include in your build:\n")
    
    try:
        selected = questionary.checkbox(
            "Select skills to build:",
            choices=choices,
            instruction="(Space: toggle, Enter: confirm, Ctrl+C: cancel)"
        ).ask()
        
        if selected is None:
            # User cancelled
            print("\n❌ Selection cancelled. No skills selected.")
            return []
        
        if not selected:
            print("\n⚠️  No skills selected. Exiting.")
            return []
        
        # Filter skills based on selection
        selected_names = set(selected)
        return [s for s in skills if s['name'] in selected_names]
        
    except KeyboardInterrupt:
        print("\n\n❌ Selection cancelled.")
        return []


def simple_skill_selector(skills: list) -> list:
    """Simple text-based skill selector as fallback."""
    print("\n" + "="*60)
    print("🎯 SKILL SELECTOR (Text Mode)")
    print("="*60)
    print("\nAvailable skills by category:\n")
    
    # Group by category
    by_category = defaultdict(list)
    for skill in skills:
        by_category[skill['category']].append(skill)
    
    category_order = [
        "architecture", "code-quality", "design", "marketing", "product", 
        "business", "devops", "data", "communication", "research", "project-management", "skills"
    ]
    
    # Display numbered list
    skill_list = []
    idx = 1
    for category in category_order:
        if category in by_category:
            print(f"\n📁 {category.upper().replace('-', ' ')}")
            for skill in sorted(by_category[category], key=lambda x: x['name']):
                print(f"   [{idx:2d}] {skill['name']}")
                skill_list.append(skill)
                idx += 1
    
    print(f"\n{'='*60}")
    print("Enter skill numbers to select (comma-separated, e.g., '1,3,5-7')")
    print("Or type 'all' to select all skills.")
    print("="*60)
    
    try:
        user_input = input("\nYour selection: ").strip()
        
        if user_input.lower() == 'all':
            return skills
        
        selected_indices = []
        for part in user_input.split(','):
            part = part.strip()
            if '-' in part:
                # Range selection (e.g., "5-7")
                try:
                    start, end = map(int, part.split('-'))
                    selected_indices.extend(range(start, end + 1))
                except ValueError:
                    print(f"⚠️  Ignoring invalid range: {part}")
            else:
                try:
                    selected_indices.append(int(part))
                except ValueError:
                    print(f"⚠️  Ignoring invalid input: {part}")
        
        # Convert to 0-based indices and filter
        selected_skills = []
        for idx in selected_indices:
            if 1 <= idx <= len(skill_list):
                selected_skills.append(skill_list[idx - 1])
            else:
                print(f"⚠️  Index {idx} out of range, skipping.")
        
        return selected_skills
        
    except KeyboardInterrupt:
        print("\n\n❌ Selection cancelled.")
        return []
    except EOFError:
        print("\n\n❌ No input provided.")
        return []


def main():
    """
    Build script for the AI Coding Agents project.
    Processes skills from the skills/ directory and generates distribution files.
    """
    args = parse_arguments()
    target_platform = args.platform

    # Setup paths
    root_dir = Path(__file__).parent.parent
    skills_dir = root_dir / 'skills'
    dist_dir = root_dir / 'dist'

    if not skills_dir.exists():
        print(f"Error: Skills directory not found at {skills_dir}")
        exit(1)
    
    # Get all available skills
    all_available_skills = get_all_skills(skills_dir)
    
    if not all_available_skills:
        print("Error: No skills found in the skills directory.")
        exit(1)
    
    # Handle --list flag
    if args.list:
        list_all_skills(all_available_skills)
        exit(0)
    
    # Determine which skills to build
    skills_to_build = []
    
    if args.all:
        # Build all skills
        skills_to_build = all_available_skills
        print(f"Building ALL {len(skills_to_build)} skills for platform: {target_platform}...")
        
    elif args.skills:
        # Build specific skills from comma-separated list
        requested_skills = [s.strip() for s in args.skills.split(',')]
        available_names = {s['name'] for s in all_available_skills}
        
        # Validate requested skills
        invalid_skills = [s for s in requested_skills if s not in available_names]
        if invalid_skills:
            print(f"\n⚠️  Warning: The following skills were not found: {', '.join(invalid_skills)}")
            print("   Run with --list to see available skills.\n")
        
        # Filter to valid skills
        skills_to_build = [s for s in all_available_skills if s['name'] in requested_skills]
        
        if not skills_to_build:
            print("❌ No valid skills selected. Exiting.")
            exit(1)
            
        print(f"Building {len(skills_to_build)} selected skills for platform: {target_platform}...")
        
    else:
        # Interactive skill selection
        print(f"No skills specified. Starting interactive selection for platform: {target_platform}...")
        
        if HAS_QUESTIONARY:
            skills_to_build = interactive_skill_selector(all_available_skills)
        else:
            skills_to_build = simple_skill_selector(all_available_skills)
        
        if not skills_to_build:
            print("❌ No skills selected. Exiting.")
            exit(0)
        
        print(f"\n✅ Selected {len(skills_to_build)} skills to build.")
    
    # Confirm before building (unless --all or --skills was used)
    if not args.all and not args.skills:
        print("\nSelected skills:")
        for skill in sorted(skills_to_build, key=lambda x: x['name']):
            print(f"  • {skill['name']}")
        
        try:
            confirm = input("\nProceed with build? [Y/n]: ").strip().lower()
            if confirm and confirm not in ('y', 'yes'):
                print("❌ Build cancelled.")
                exit(0)
        except (KeyboardInterrupt, EOFError):
            print("\n❌ Build cancelled.")
            exit(0)
    
    # Create distribution directory
    if not dist_dir.exists():
        dist_dir.mkdir()
    
    # Process selected skills
    all_skills_data, errors = _process_skills_for_platform(
        skills_dir, dist_dir, target_platform, skills_to_build
    )

    if not errors:
        manifest_path = dist_dir / 'skills.json'
        all_skills_data.sort(key=lambda x: x['name'])
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(all_skills_data, f, indent=2)
        print(f"\n✅ Successfully generated manifest at {manifest_path}")
        
        if target_platform == "claude":
            generate_readme(root_dir, all_skills_data)

        dist_skills_dir = dist_dir / f'.{target_platform}'
        generate_platform_md(dist_skills_dir, all_skills_data, target_platform)

    if errors:
        print("\n⚠️  Build process completed with errors:")
        for error in errors:
            print(f"   - {error}")
        exit(1)
    else:
        print(f"\n🎉 Build process completed successfully! {len(all_skills_data)} skills processed.")

def _process_skills_for_platform(skills_dir: Path, dist_dir: Path, target_platform: str, skills_to_build: list = None):
    """Process skills from the skills/ directory for the target platform.
    
    Args:
        skills_dir: Path to the skills directory
        dist_dir: Path to the distribution directory
        target_platform: Target platform name (claude, gemini, codex, etc.)
        skills_to_build: Optional list of skill dicts to process. If None, processes all skills.
    """
    gemini_model_map = {
        "sonnet": "gemini-ultra",
        "haiku": "gemini-pro"
    }
    codex_model_map = {
        "sonnet": "gpt-4",
        "haiku": "gpt-3.5-turbo"
    }

    # Use dot notation for platform directory
    dist_platform_dir = dist_dir / f'.{target_platform}'
    if dist_platform_dir.exists():
        shutil.rmtree(dist_platform_dir)
    dist_platform_dir.mkdir()

    # Create structure - everything goes into skills/
    (dist_platform_dir / "skills").mkdir(parents=True, exist_ok=True)

    print(f"Created platform-specific distribution directory: {dist_platform_dir}")

    all_skills_data = []
    errors = []

    frontmatter_re = re.compile(r'---\s*\n(.*?)\n---\s*\n', re.DOTALL)
    
    # Determine which skills to process
    if skills_to_build is not None:
        # Use provided list of skills
        skill_dirs = [s['path'] for s in skills_to_build]
        print(f"Processing {len(skill_dirs)} selected skills...")
    else:
        # Find all SKILL.md files in the skills directory
        skill_dirs = [d for d in skills_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]
        print(f"Processing all {len(skill_dirs)} skills...")
    
    gemini_skills_content = []
    if target_platform == "gemini":
        gemini_skills_content.append("# Generated Gemini Skill Definitions\n")
        gemini_skills_content.append("from typing import List, Dict, Any\n\n")

    codex_skills_content = []
    if target_platform == "codex":
        codex_skills_content.append("# Generated Codex Skill Definitions\n")
        codex_skills_content.append("from typing import List, Dict, Any\n\n")

    for skill_dir in skill_dirs:
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            # Skip directories without SKILL.md
            continue
        
        try:
            content = skill_file.read_text(encoding='utf-8')
            match = frontmatter_re.match(content)
            if not match:
                errors.append(f"No frontmatter found in {skill_file}")
                continue
            
            yaml_content = match.group(1)
            frontmatter = yaml.safe_load(yaml_content)
            
            if not isinstance(frontmatter, dict):
                raise ValueError("Frontmatter is not a valid dictionary.")

            # Skills always have type 'skill'
            item_type = 'skill'

            # Required fields for skills
            required_fields = ['name', 'description']
            missing = [f for f in required_fields if f not in frontmatter]
            if missing:
                raise ValueError(f"Missing required fields: {', '.join(missing)}")
            
            # Infer category from skill name
            category = _infer_category_from_skill_name(frontmatter['name'])

            skill_data = {
                'name': frontmatter['name'],
                'category': category,
                'description': frontmatter['description'],
                'type': item_type,
                'model': frontmatter.get('model', 'sonnet'),
                'file_path': str(skill_file.relative_to(skills_dir.parent)),
            }

            all_skills_data.append(skill_data)
            
            # --- Platform-specific artifact generation ---

            # Copy skill to distribution directory
            dest_skill_dir = dist_platform_dir / "skills" / frontmatter['name']
            dest_skill_dir.mkdir(parents=True, exist_ok=True)
            dest = dest_skill_dir / "SKILL.md"
            shutil.copy(skill_file, dest)

            # Copy sibling files if they exist (for multi-file skills)
            for sibling in skill_dir.glob('*'):
                if sibling.name != 'SKILL.md' and sibling.is_file():
                    shutil.copy(sibling, dest_skill_dir / sibling.name)
                elif sibling.is_dir() and sibling.name not in ['.git', '__pycache__', '.venv', 'venv']:
                    # Copy subdirectories recursively
                    dest_subdir = dest_skill_dir / sibling.name
                    if dest_subdir.exists():
                        shutil.rmtree(dest_subdir)
                    shutil.copytree(sibling, dest_subdir)

            if target_platform == "gemini":
                # Generate Python definition
                class_name = f"{frontmatter['name'].replace('-', '_').title()}Skill"

                gemini_skills_content.append(f"class {class_name}:\n")
                gemini_skills_content.append(f"    name: str = \"{frontmatter['name']}\"\n")
                gemini_skills_content.append(f"    description: str = \"{frontmatter['description']}\"\n")
                gemini_skills_content.append(f"    category: str = \"{category}\"\n")
                gemini_skills_content.append(f"    type: str = \"skill\"\n")
                gemini_skills_content.append(f"    model: str = \"{gemini_model_map.get(frontmatter.get('model', 'sonnet'), frontmatter.get('model', 'sonnet'))}\"\n")

                # Extract content after frontmatter for system instructions
                skill_instructions = content[match.end():].strip()
                gemini_skills_content.append(f"    system_instruction: str = \"\"\"\n{skill_instructions}\n\"\"\"\n\n")

            elif target_platform == "codex":
                # Generate Python definition
                class_name = f"{frontmatter['name'].replace('-', '_').title()}Skill"

                codex_skills_content.append(f"class {class_name}:\n")
                codex_skills_content.append(f"    name: str = \"{frontmatter['name']}\"\n")
                codex_skills_content.append(f"    description: str = \"{frontmatter['description']}\"\n")
                codex_skills_content.append(f"    category: str = \"{category}\"\n")
                codex_skills_content.append(f"    type: str = \"skill\"\n")
                codex_skills_content.append(f"    model: str = \"{codex_model_map.get(frontmatter.get('model', 'sonnet'), frontmatter.get('model', 'sonnet'))}\"\n")

                # Extract content after frontmatter for prompt
                skill_prompt = content[match.end():].strip()
                codex_skills_content.append(f"    prompt: str = \"\"\"\n{skill_prompt}\n\"\"\"\n\n")

        except Exception as e:
            errors.append(f"Failed to process {skill_file}: {e}")
    
    if target_platform == "gemini":
        gemini_skills_file_path = dist_platform_dir / "gemini_skills.py"
        with open(gemini_skills_file_path, 'w', encoding='utf-8') as f:
            f.write("".join(gemini_skills_content))
    elif target_platform == "codex":
        codex_skills_file_path = dist_platform_dir / "codex_skills.py"
        with open(codex_skills_file_path, 'w', encoding='utf-8') as f:
            f.write("".join(codex_skills_content))

    return all_skills_data, errors


def _infer_category_from_skill_name(skill_name: str) -> str:
    """Infer category from skill name based on naming patterns."""
    category_patterns = {
        'architecture': ['api', 'database', 'system', 'tech-stack', 'feature-spec'],
        'code-quality': ['code', 'documentation', 'performance', 'refactoring', 'security', 'test'],
        'design': ['brand', 'color', 'design-system', 'icon', 'layout', 'typography', 'ui', 'wireframe'],
        'marketing': ['ad', 'blog', 'copywriter', 'email', 'landing', 'seo', 'social'],
        'product': ['accessibility', 'competitor', 'feature-prioritizer', 'feedback', 'user-story', 'ux'],
        'business': ['business', 'financial', 'market-research', 'pricing', 'privacy', 'terms'],
        'devops': ['backup', 'cost', 'deployment', 'error-investigator', 'monitoring'],
        'data': ['analytics', 'dashboard', 'data-visualizer', 'report', 'sql'],
        'communication': ['api-documenter', 'changelog', 'presentation', 'support', 'team', 'technical-writer'],
        'research': ['best-practice', 'library', 'solution', 'technology', 'trend'],
        'project-management': ['agile', 'project'],
    }
    
    for category, patterns in category_patterns.items():
        for pattern in patterns:
            if skill_name.startswith(pattern) or pattern in skill_name:
                return category
    
    return 'skills'  # default category

if __name__ == "__main__":
    main()
