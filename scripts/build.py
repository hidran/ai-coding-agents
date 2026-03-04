#!/usr/bin/env python3
import json
import yaml
import shutil
import re
import argparse
from pathlib import Path
from collections import defaultdict

def generate_readme(root_dir: Path, all_agents_data: list):
    """Generates the README.md from a template and the agent data."""
    print("Generating README.md...")
    template_path = root_dir /  'README.template.md'
    readme_path = root_dir /  'README.md'
    
    # Filter for agents only for the README
    agents_only = [a for a in all_agents_data if a.get('type', 'agent') == 'agent']

    # Group agents by category
    agents_by_category = defaultdict(list)
    for agent in agents_only:
        agents_by_category[agent['category']].append(agent)
        
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
        "skills": "Repeatable workflows and generators for common tasks"
    }

    md_parts = ["## 🤖 Your AI Dream Team\n\n*Meet your new coding sidekicks - each one a specialist in their field:*"]
    
    for category in category_order:
        if category in agents_by_category:
            agents = sorted(agents_by_category[category], key=lambda x: x['name'])
            md_parts.append(f"\n### 🏗️ {category.capitalize()} ({len(agents)} agents)")
            md_parts.append(f"*{category_descriptions.get(category, '')}*")
            for agent in agents:
                md_parts.append(f"- **{agent['name']}** - A specialist in {agent['name'].replace('-', ' ')}.")
    
    agent_list_md = "\n".join(md_parts)

    # Replace placeholder in template
    template_content = template_path.read_text(encoding='utf-8')
    readme_content = template_content.replace('{{AGENT_LIST}}', agent_list_md)
    
    # Update total agent count
    readme_content = re.sub(r'Meet \d+ specialized AI agents', f'Meet {len(agents_only)} specialized AI agents', readme_content)
    readme_content = re.sub(r'it\'s like having \d+ AI specialists', f'it\'s like having {len(agents_only)} AI specialists', readme_content)


    readme_path.write_text(readme_content, encoding='utf-8')
    print("Successfully generated README.md")

def generate_platform_md(dist_dir: Path, all_agents_data: list, platform: str):
    """Generates PLATFORM.md (e.g. CLAUDE.md) for the given platform."""
    filename = 'CLAUDE.md' if platform == 'claude' else f'{platform.upper()}.md'
    md_path = dist_dir / filename

    content = [f"# {filename}\n"]
    content.append(f"Master configuration for {platform.capitalize()} Code. This file indexes available Skills, Rules, and Subagents.\n")

    content.append("\n# Project Standards\n")
    content.append("<!-- Add project-wide standards here (e.g., framework conventions, code quality, accessibility) -->\n")
    content.append("- Follow the coding style defined in the project.\n")

    content.append("\n# Skills & Subagents\n")

    # Skills
    skills = [a for a in all_agents_data if a.get('type') == 'skill']
    if skills:
        content.append("\n## Available Skills\n")
        for skill in sorted(skills, key=lambda x: x['name']):
            content.append(f"- `/{skill['name']}` - {skill['description']}")

    # Rules
    rules = [a for a in all_agents_data if a.get('type') == 'rule']
    if rules:
        content.append("\n## Project Rules (auto-loaded by path)\n")
        for rule in sorted(rules, key=lambda x: x['name']):
            content.append(f"- `{rule['name']}` - {rule['description']}")

    # Subagents
    subagents = [a for a in all_agents_data if a.get('type') == 'agent']
    if subagents:
        content.append("\n## Subagents\n")
        for agent in sorted(subagents, key=lambda x: x['name']):
            content.append(f"- `{agent['name']}` - {agent['description']}")

    md_path.write_text("\n".join(content), encoding='utf-8')

def parse_arguments():
    parser = argparse.ArgumentParser(description="Build script for AI agents.")
    parser.add_argument(
        "--platform",
        choices=["claude", "gemini", "codex", "junie"],
        default="claude",
        help="Target AI platform for agent generation.",
    )
    return parser.parse_args()


def main():
    """
    Build script for the Ai Coding Agents project.
    """
    args = parse_arguments()
    target_platform = args.platform

    print(f"Starting agent build process for platform: {target_platform}...")

    # Setup paths
    root_dir = Path(__file__).parent.parent
    source_dir = root_dir
    dist_dir = root_dir / 'dist'

    if not dist_dir.exists():
        dist_dir.mkdir()
    
    all_agents_data, errors = _process_agents_for_platform(root_dir, dist_dir, target_platform)

    if not errors:
        manifest_path = dist_dir / 'agents.json'
        all_agents_data.sort(key=lambda x: x['name'])
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(all_agents_data, f, indent=2)
        print(f"\nSuccessfully generated manifest at {manifest_path}")
        
        if target_platform == "claude":
            generate_readme(root_dir, all_agents_data)

        dist_agents_dir = dist_dir / f'.{target_platform}'
        generate_platform_md(dist_agents_dir, all_agents_data, target_platform)

    if errors:
        print("\nBuild process completed with errors:")
        for error in errors:
            print(f"- {error}")
        exit(1)
    else:
        print(f"\nBuild process completed successfully! {len(all_agents_data)} items processed.")

def _process_agents_for_platform(source_dir: Path, dist_dir: Path, target_platform: str):
    gemini_model_map = {
        "sonnet": "gemini-ultra",
        "haiku": "gemini-pro"
    }
    codex_model_map = {
        "sonnet": "gpt-4",
        "haiku": "gpt-3.5-turbo"
    }

    # Use dot notation for platform directory
    dist_agents_dir = dist_dir / f'.{target_platform}'
    if dist_agents_dir.exists():
        shutil.rmtree(dist_agents_dir)
    dist_agents_dir.mkdir()

    # Create structure for all platforms
    (dist_agents_dir / "agents").mkdir(parents=True, exist_ok=True)
    (dist_agents_dir / "rules").mkdir(parents=True, exist_ok=True)
    (dist_agents_dir / "skills").mkdir(parents=True, exist_ok=True)

    print(f"Created platform-specific distribution directory: {dist_agents_dir}")

    all_agents_data = []
    errors = []

    frontmatter_re = re.compile(r'---\s*\n(.*?)\n---\s*\n', re.DOTALL)
    categories = [d.name for d in source_dir.iterdir() if d.is_dir() and not d.name.startswith('.') and d.name not in ['dist', 'scripts', 'venv', '__pycache__', '.git', '.idea']]

    gemini_agents_content = []
    if target_platform == "gemini":
        gemini_agents_content.append("# Generated Gemini Agent Definitions\n")
        gemini_agents_content.append("from typing import List, Dict, Any\n\n")

    codex_agents_content = []
    if target_platform == "codex":
        codex_agents_content.append("# Generated Codex Agent Definitions\n")
        codex_agents_content.append("from typing import List, Dict, Any\n\n")

    for category in categories:
        category_path = source_dir / category
        if not category_path.is_dir():
            continue

        # Use glob to find all .md files recursively in the category directory
        for agent_file in category_path.glob('**/*.md'):
            if agent_file.name in ['README.md', 'README.template.md', 'CONTRIBUTING.md', 'EXAMPLES.md', 'LICENSE']:
                continue
            
            try:
                content = agent_file.read_text(encoding='utf-8')
                match = frontmatter_re.match(content)
                if not match:
                    # Skip files without frontmatter
                    continue
                
                yaml_content = match.group(1)
                frontmatter = yaml.safe_load(yaml_content)
                
                if not isinstance(frontmatter, dict):
                    raise ValueError("Frontmatter is not a valid dictionary.")

                # Determine type
                item_type = frontmatter.get('type')
                if not item_type:
                    if 'model' in frontmatter:
                        item_type = 'agent'
                    elif 'paths' in frontmatter:
                        item_type = 'rule'
                    elif 'allowed-tools' in frontmatter:
                        item_type = 'skill'
                    else:
                        # Default to rule if ambiguous but has name/desc
                        item_type = 'rule'

                required_fields = ['name', 'description', 'category']
                if item_type == 'agent':
                    required_fields.append('model')

                missing = [f for f in required_fields if f not in frontmatter]
                if missing:
                    # If category is missing but we are in a known structure, infer it
                    if 'category' in missing:
                        # If we are in skills/typescript/SKILL.md, category is skills
                        # If we are in architecture/api-designer.md, category is architecture
                        # The 'category' variable in this loop is the top-level folder name
                        frontmatter['category'] = category
                        missing.remove('category')

                    if missing:
                        raise ValueError(f"Missing required fields: {', '.join(missing)}")
                
                # Check category match, but allow subdirectories in skills
                if frontmatter['category'] != category:
                     # Allow skills to be in 'skills' folder or their own category
                     if category == 'skills' and frontmatter['category'] == 'skills':
                         pass
                     elif frontmatter['category'] != category:
                         raise ValueError(f"Category in frontmatter ('{frontmatter['category']}') does not match directory ('{category}').")

                agent_data = {
                    'name': frontmatter['name'],
                    'category': frontmatter['category'],
                    'description': frontmatter['description'],
                    'type': item_type,
                    'tags': frontmatter.get('tags', []),
                    'workflow': frontmatter.get('workflow', []),
                    'file_path': str(agent_file.relative_to(source_dir)),
                    'agents_md': frontmatter.get('agents_md', {})
                }
                if item_type == 'agent':
                    agent_data['model'] = frontmatter['model']

                all_agents_data.append(agent_data)
                
                # --- Platform-specific artifact generation ---

                # Copy to appropriate folder in structure
                if item_type == 'agent':
                    dest = dist_agents_dir / "agents" / agent_file.name
                    shutil.copy(agent_file, dest)
                elif item_type == 'rule':
                    dest = dist_agents_dir / "rules" / agent_file.name
                    shutil.copy(agent_file, dest)
                elif item_type == 'skill':
                    # Skills are directories
                    skill_dir = dist_agents_dir / "skills" / frontmatter['name']
                    skill_dir.mkdir(parents=True, exist_ok=True)
                    dest = skill_dir / "SKILL.md"
                    shutil.copy(agent_file, dest)

                    # Copy sibling files if they exist (for multi-file skills)
                    # This assumes the skill is in a subdirectory like skills/typescript/SKILL.md
                    # We want to copy setup.md, code-style.md etc. to the same destination folder
                    if agent_file.parent != category_path:
                        for sibling in agent_file.parent.glob('*'):
                            if sibling.name != 'SKILL.md' and sibling.name != agent_file.name:
                                shutil.copy(sibling, skill_dir / sibling.name)

                else:
                    dest = dist_agents_dir / "agents" / agent_file.name # Default
                    shutil.copy(agent_file, dest)
                    

                if target_platform == "gemini":
                    # Generate Python definition
                    class_suffix = item_type.title()
                    class_name = f"{frontmatter['name'].replace('-', '_').title()}{class_suffix}"

                    gemini_agents_content.append(f"class {class_name}:\n")
                    gemini_agents_content.append(f"    name: str = \"{frontmatter['name']}\"\n")
                    gemini_agents_content.append(f"    description: str = \"{frontmatter['description']}\"\n")
                    gemini_agents_content.append(f"    category: str = \"{frontmatter['category']}\"\n")
                    gemini_agents_content.append(f"    type: str = \"{item_type}\"\n")

                    if item_type == 'agent':
                        gemini_agents_content.append(f"    model: str = \"{gemini_model_map.get(frontmatter['model'], frontmatter['model'])}\"\n")

                    if 'paths' in frontmatter:
                        gemini_agents_content.append(f"    paths: List[str] = {json.dumps(frontmatter['paths'])}\n")

                    # Add AGENTS.md specific fields
                    agents_md_config = agent_data.get('agents_md', {})
                    if agents_md_config:
                        for key, value in agents_md_config.items():
                            if isinstance(value, dict):
                                gemini_agents_content.append(f"    {key}: Dict[str, Any] = {json.dumps(value)}\n")
                            elif isinstance(value, list):
                                gemini_agents_content.append(f"    {key}: List[Any] = {json.dumps(value)}\n")
                            else:
                                gemini_agents_content.append(f"    {key}: Any = {json.dumps(value)}\n")

                    # Extract content after frontmatter for system instructions
                    agent_instructions = content[match.end():].strip()

                    tools_available_match = re.search(r'## Tools Available:\n(.*?)(?=\n##|$)', agent_instructions, re.DOTALL)
                    tools_available_content = tools_available_match.group(1).strip() if tools_available_match else "No specific tools listed."

                    gemini_agents_content.append(f"    system_instruction: str = \"\"\"\n{agent_instructions}\n\"\"\"\n")
                    gemini_agents_content.append(f"    tools_available: str = \"\"\"\n{tools_available_content}\n\"\"\"\n\n")

                elif target_platform == "codex":
                    # Generate Python definition
                    class_suffix = item_type.title()
                    class_name = f"{frontmatter['name'].replace('-', '_').title()}{class_suffix}"

                    codex_agents_content.append(f"class {class_name}:\n")
                    codex_agents_content.append(f"    name: str = \"{frontmatter['name']}\"\n")
                    codex_agents_content.append(f"    description: str = \"{frontmatter['description']}\"\n")
                    codex_agents_content.append(f"    category: str = \"{frontmatter['category']}\"\n")
                    codex_agents_content.append(f"    type: str = \"{item_type}\"\n")

                    if item_type == 'agent':
                        codex_agents_content.append(f"    model: str = \"{codex_model_map.get(frontmatter['model'], frontmatter['model'])}\"\n")

                    if 'paths' in frontmatter:
                        codex_agents_content.append(f"    paths: List[str] = {json.dumps(frontmatter['paths'])}\n")

                    # Add AGENTS.md specific fields
                    agents_md_config = agent_data.get('agents_md', {})
                    if agents_md_config:
                        for key, value in agents_md_config.items():
                            if isinstance(value, dict):
                                codex_agents_content.append(f"    {key}: Dict[str, Any] = {json.dumps(value)}\n")
                            elif isinstance(value, list):
                                codex_agents_content.append(f"    {key}: List[Any] = {json.dumps(value)}\n")
                            else:
                                codex_agents_content.append(f"    {key}: Any = {json.dumps(value)}\n")

                    # Extract content after frontmatter for prompt
                    agent_prompt = content[match.end():].strip()

                    tools_available_match = re.search(r'## Tools Available:\n(.*?)(?=\n##|$)', agent_prompt, re.DOTALL)
                    tools_available_content = tools_available_match.group(1).strip() if tools_available_match else "No specific tools listed."

                    codex_agents_content.append(f"    prompt: str = \"\"\"\n{agent_prompt}\n\"\"\"\n")
                    codex_agents_content.append(f"    tools_available: str = \"\"\"\n{tools_available_content}\n\"\"\"\n\n")


            except Exception as e:
                errors.append(f"Failed to process {agent_file}: {e}")
    
    if target_platform == "gemini":
        gemini_agents_file_path = dist_agents_dir / "gemini_agents.py"
        with open(gemini_agents_file_path, 'w', encoding='utf-8') as f:
            f.write("".join(gemini_agents_content))
    elif target_platform == "codex":
        codex_agents_file_path = dist_agents_dir / "codex_agents.py"
        with open(codex_agents_file_path, 'w', encoding='utf-8') as f:
            f.write("".join(codex_agents_content))

    return all_agents_data, errors

if __name__ == "__main__":
    main()
