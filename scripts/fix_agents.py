#!/usr/bin/env python3
import re
from pathlib import Path

def fix_agent_file(file_path: Path):
    """
    Corrects the YAML frontmatter of a given agent file.

    It finds 'Examples:' blocks and 'model:' lines inside the YAML
    frontmatter and moves them to the correct locations.
    """
    try:
        content = file_path.read_text(encoding='utf-8')

        # Pattern to find the model line and the examples block if they are inside the frontmatter
        pattern = re.compile(
            r'(---\n'                  # Start of frontmatter
            r'.*?'                     # Non-greedy content
            r')(Examples:\s*\n'          # Capture group for Examples block
            r'.*?'                     # The content of the examples
            r')(\nmodel:\s*(?:sonnet|haiku)\s*\n)' # Capture group for the model line
            r'(---\n.*)',              # Rest of the file
            re.DOTALL
        )

        match = pattern.search(content)

        # A simpler pattern if the first one fails
        if not match:
             pattern = re.compile(
                r'(---\n'
                r'[\s\S]*?)' # The frontmatter content before Examples
                r'(Examples:\s*\n'
                r'[\s\S]*?' # The examples block
                r')(\nmodel:\s*(?:sonnet|haiku)\s*\n)'
                r'(---\n'
                r'[\s\S]*)',
                re.DOTALL
            )
             match = pattern.search(content)


        if match:
            frontmatter_before = match.group(1).strip()
            examples_block = match.group(2).strip()
            model_line = match.group(3).strip()
            rest_of_file = match.group(4).strip()

            # Reconstruct the file with corrected structure
            new_content = (
                f"---\n"
                f"{frontmatter_before}\n"
                f"{model_line}\n"
                f"---\n\n"
                f"{examples_block}\n\n"
                f"{rest_of_file.replace('---', '', 1).strip()}\n"
            )
            
            # A slightly different pattern for reconstruction if needed
            if 'description:' not in frontmatter_before:
                 new_content = (
                    f"---\n"
                    f"{frontmatter_before}\n"
                    f"{model_line}\n"
                    f"---\n\n"
                    f"{examples_block}\n"
                    f"{rest_of_file.replace('---', '').strip()}"
                )


            file_path.write_text(new_content, encoding='utf-8')
            print(f"FIXED: {file_path}")
            return True

    except Exception as e:
        print(f"ERROR processing {file_path}: {e}")
    
    return False

def main():
    root_dir = Path(__file__).parent.parent
    source_dir = root_dir
    
    print("Starting agent file correction process...")
    
    fixed_count = 0
    for md_file in source_dir.glob('**/*.md'):
        if md_file.name == 'README.md' or md_file.name == 'CONTRIBUTING.md' or md_file.name == 'EXAMPLES.md' or md_file.name == 'LICENSE':
            continue
        if fix_agent_file(md_file):
            fixed_count += 1
            
    print(f"\nCorrection process finished. {fixed_count} files fixed.")

if __name__ == "__main__":
    main()
