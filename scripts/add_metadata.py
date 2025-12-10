#!/usr/bin/env python3
import re
from pathlib import Path
import yaml

def add_metadata_to_file(agent_file: Path):
    """
    Adds the 'category' field to the YAML frontmatter of an agent file
    based on its parent directory.
    """
    try:
        category = agent_file.parent.name
        content = agent_file.read_text(encoding='utf-8')

        # Regex to find YAML frontmatter
        frontmatter_re = re.compile(r'---\s*\n(.*?)\n---', re.DOTALL)
        match = frontmatter_re.match(content)

        if not match:
            print(f"SKIPPING: No frontmatter found in {agent_file}")
            return False

        yaml_content_str = match.group(1)
        frontmatter = yaml.safe_load(yaml_content_str)

        if 'category' in frontmatter and frontmatter['category'] == category:
            # print(f"SKIPPING: Category already exists and is correct in {agent_file}")
            return False

        # Add the category field
        frontmatter['category'] = category
        
        # Re-dump the YAML to string
        # Use a custom dumper to ensure consistent formatting if needed
        new_yaml_content_str = yaml.dump(frontmatter, default_flow_style=False, sort_keys=False, indent=2)

        # Replace the old frontmatter with the new one
        new_file_content = content.replace(yaml_content_str, new_yaml_content_str, 1)

        agent_file.write_text(new_file_content, encoding='utf-8')
        print(f"UPDATED: Added category '{category}' to {agent_file}")
        return True

    except Exception as e:
        print(f"ERROR processing {agent_file}: {e}")
        return False

def main():
    root_dir = Path(__file__).parent.parent
    source_dir = root_dir / 'docs'
    
    print("Starting to add 'category' metadata to agent files...")
    
    updated_count = 0
    for md_file in source_dir.glob('**/*.md'):
        if md_file.name in ['README.md', 'CONTRIBUTING.md', 'EXAMPLES.md', 'LICENSE']:
            continue
        if add_metadata_to_file(md_file):
            updated_count += 1
            
    print(f"\nMetadata process finished. {updated_count} files updated.")

if __name__ == "__main__":
    main()
