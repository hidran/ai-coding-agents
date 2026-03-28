#!/usr/bin/env node

/**
 * AI Coding Agents Build Script (Node.js version)
 * 
 * Usage:
 *   node scripts/build.js --all
 *   node scripts/build.js --skills=api-designer,code-reviewer
 *   node scripts/build.js --list
 *   node scripts/build.js --platform=gemini
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Try to import optional dependencies
let chalk, inquirer, yaml;
let HAS_CHALK = false;
let HAS_INQUIRER = false;

try {
  chalk = require('chalk');
  HAS_CHALK = true;
} catch (e) {
  // chalk not installed
}

try {
  inquirer = require('inquirer');
  HAS_INQUIRER = true;
} catch (e) {
  // inquirer not installed
}

try {
  yaml = require('yaml');
} catch (e) {
  console.error('❌ Error: yaml package is required. Install with: npm install yaml');
  process.exit(1);
}

// Utility functions for colored output
const c = {
  success: (text) => HAS_CHALK ? chalk.green(text) : text,
  error: (text) => HAS_CHALK ? chalk.red(text) : text,
  warning: (text) => HAS_CHALK ? chalk.yellow(text) : text,
  info: (text) => HAS_CHALK ? chalk.blue(text) : text,
  bold: (text) => HAS_CHALK ? chalk.bold(text) : text,
  dim: (text) => HAS_CHALK ? chalk.dim(text) : text,
};

// Parse command line arguments
function parseArguments() {
  const args = process.argv.slice(2);
  const options = {
    platform: 'claude',
    all: false,
    skills: null,
    list: false,
    help: false
  };

  for (const arg of args) {
    if (arg === '--help' || arg === '-h') {
      options.help = true;
    } else if (arg === '--all') {
      options.all = true;
    } else if (arg === '--list') {
      options.list = true;
    } else if (arg.startsWith('--platform=')) {
      options.platform = arg.split('=')[1];
    } else if (arg.startsWith('--skills=')) {
      options.skills = arg.split('=')[1];
    }
  }

  return options;
}

function showHelp() {
  console.log(`
${c.bold('AI Coding Agents Build Script (Node.js)')}

${c.bold('Usage:')} node scripts/build.js [options]

${c.bold('Options:')}
  --all                   Build all skills
  --skills=list           Comma-separated list of specific skills
  --list                  List all available skills
  --platform=<name>       Target platform (claude|gemini|codex) [default: claude]
  --help, -h              Show this help message

${c.bold('Examples:')}
  node scripts/build.js --all
  node scripts/build.js --skills=api-designer,code-reviewer
  node scripts/build.js --list
  node scripts/build.js --platform=gemini --all
`);
}

// Category mapping based on skill names
const categoryPatterns = {
  'architecture': ['api', 'database', 'system', 'tech-stack', 'feature-spec', 'supabase-architect'],
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
  'workflow': ['brainstorming', 'writing-plans', 'subagent-driven-development', 'executing-plans', 
               'test-driven-development', 'systematic-debugging', 'using-git-worktrees', 
               'requesting-code-review', 'receiving-code-review'],
};

function inferCategory(skillName) {
  for (const [category, patterns] of Object.entries(categoryPatterns)) {
    for (const pattern of patterns) {
      if (skillName.startsWith(pattern) || skillName.includes(pattern)) {
        return category;
      }
    }
  }
  return 'skills';
}

function getAllSkills(skillsDir, rootDir) {
  const skills = [];
  
  // Source directories to scan for skills
  const sourceDirs = [
    { dir: skillsDir, type: 'skill' },
    { dir: path.join(rootDir, 'workflow'), type: 'workflow' },
    { dir: path.join(rootDir, 'architecture'), type: 'agent' },
    { dir: path.join(rootDir, 'code-quality'), type: 'agent' },
    { dir: path.join(rootDir, 'design'), type: 'agent' },
    { dir: path.join(rootDir, 'marketing'), type: 'agent' },
    { dir: path.join(rootDir, 'product'), type: 'agent' },
    { dir: path.join(rootDir, 'business'), type: 'agent' },
    { dir: path.join(rootDir, 'devops'), type: 'agent' },
    { dir: path.join(rootDir, 'data'), type: 'agent' },
    { dir: path.join(rootDir, 'communication'), type: 'agent' },
    { dir: path.join(rootDir, 'research'), type: 'agent' },
    { dir: path.join(rootDir, 'project-management'), type: 'agent' },
  ];
  
  for (const { dir, type } of sourceDirs) {
    if (!fs.existsSync(dir)) {
      continue;
    }

    const entries = fs.readdirSync(dir, { withFileTypes: true });
    
    for (const entry of entries) {
      if (entry.isDirectory() && !entry.name.startsWith('.')) {
        const skillFile = path.join(dir, entry.name, 'SKILL.md');
        const mdFile = path.join(dir, entry.name + '.md');
        
        // Check for SKILL.md inside directory (for skills/)
        if (fs.existsSync(skillFile)) {
          const category = type === 'skill' ? inferCategory(entry.name) : type;
          skills.push({
            name: entry.name,
            category,
            path: path.join(dir, entry.name),
            type,
            sourceFile: skillFile
          });
        }
      } else if (entry.isFile() && entry.name.endsWith('.md') && !entry.name.startsWith('.')) {
        // Check for .md files directly in directory (for agents like architecture/, workflow/)
        const baseName = entry.name.replace('.md', '');
        // For agent and workflow types, use directory name as category; otherwise infer from name
        const category = (type === 'agent' || type === 'workflow') ? path.basename(dir) : inferCategory(baseName);
        skills.push({
          name: baseName,
          category,
          path: dir,
          type,
          sourceFile: path.join(dir, entry.name)
        });
      }
    }
  }

  return skills.sort((a, b) => {
    if (a.category !== b.category) {
      return a.category.localeCompare(b.category);
    }
    return a.name.localeCompare(b.name);
  });
}

function listAllSkills(skills) {
  console.log('\n' + '='.repeat(60));
  console.log('📋 AVAILABLE SKILLS');
  console.log('='.repeat(60));

  // Group by category
  const byCategory = {};
  for (const skill of skills) {
    if (!byCategory[skill.category]) {
      byCategory[skill.category] = [];
    }
    byCategory[skill.category].push(skill);
  }

  const categoryOrder = [
    'workflow', 'architecture', 'code-quality', 'design', 'marketing', 'product',
    'business', 'devops', 'data', 'communication', 'research', 'project-management', 'skills'
  ];

  for (const category of categoryOrder) {
    if (byCategory[category]) {
      console.log(`\n📁 ${category.toUpperCase().replace(/-/g, ' ')}`);
      console.log('-'.repeat(40));
      for (const skill of byCategory[category]) {
        console.log(`   • ${skill.name}`);
      }
    }
  }

  console.log('\n' + '='.repeat(60));
  console.log(`Total: ${skills.length} skills available`);
  console.log('='.repeat(60) + '\n');
}

async function interactiveSkillSelector(skills) {
  if (!HAS_INQUIRER) {
    console.log('\n⚠️  Interactive selection requires inquirer package.');
    console.log('   Install it with: npm install inquirer');
    console.log('\n   Falling back to text-based selection...\n');
    return simpleSkillSelector(skills);
  }

  // Group skills by category
  const byCategory = {};
  for (const skill of skills) {
    if (!byCategory[skill.category]) {
      byCategory[skill.category] = [];
    }
    byCategory[skill.category].push(skill);
  }

  const categoryOrder = [
    'workflow', 'architecture', 'code-quality', 'design', 'marketing', 'product',
    'business', 'devops', 'data', 'communication', 'research', 'project-management', 'skills'
  ];

  // Build choices with separators
  const choices = [];
  for (const category of categoryOrder) {
    if (byCategory[category]) {
      choices.push(new inquirer.Separator(`\n📁 ${category.toUpperCase().replace(/-/g, ' ')}`));
      for (const skill of byCategory[category].sort((a, b) => a.name.localeCompare(b.name))) {
        choices.push({
          name: `  ${skill.name}`,
          value: skill.name,
          checked: false
        });
      }
    }
  }

  console.log('\n' + '='.repeat(60));
  console.log('🎯 SKILL SELECTOR');
  console.log('='.repeat(60));
  console.log('\nUse ↑/↓ to navigate, SPACE to select/deselect, ENTER to confirm.\n');

  try {
    const answers = await inquirer.prompt([{
      type: 'checkbox',
      name: 'selected',
      message: 'Select skills to build:',
      choices: choices,
      pageSize: 20
    }]);

    if (!answers.selected || answers.selected.length === 0) {
      console.log('\n⚠️  No skills selected. Exiting.');
      return [];
    }

    const selectedNames = new Set(answers.selected);
    return skills.filter(s => selectedNames.has(s.name));
  } catch (error) {
    console.log('\n❌ Selection cancelled.');
    return [];
  }
}

async function simpleSkillSelector(skills) {
  console.log('\n' + '='.repeat(60));
  console.log('🎯 SKILL SELECTOR (Text Mode)');
  console.log('='.repeat(60));
  console.log('\nAvailable skills by category:\n');

  // Group by category
  const byCategory = {};
  for (const skill of skills) {
    if (!byCategory[skill.category]) {
      byCategory[skill.category] = [];
    }
    byCategory[skill.category].push(skill);
  }

  const categoryOrder = [
    'workflow', 'architecture', 'code-quality', 'design', 'marketing', 'product',
    'business', 'devops', 'data', 'communication', 'research', 'project-management', 'skills'
  ];

  const skillList = [];
  let idx = 1;
  
  for (const category of categoryOrder) {
    if (byCategory[category]) {
      console.log(`\n📁 ${category.toUpperCase().replace(/-/g, ' ')}`);
      for (const skill of byCategory[category].sort((a, b) => a.name.localeCompare(b.name))) {
        console.log(`   [${idx.toString().padStart(2)}] ${skill.name}`);
        skillList.push(skill);
        idx++;
      }
    }
  }

  console.log('\n' + '='.repeat(60));
  console.log('Enter skill numbers to select (comma-separated, e.g., "1,3,5-7")');
  console.log('Or type "all" to select all skills.');
  console.log('='.repeat(60));

  // Read user input
  const readline = require('readline');
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  return new Promise((resolve) => {
    rl.question('\nYour selection: ', (input) => {
      rl.close();
      input = input.trim();

      if (input.toLowerCase() === 'all') {
        resolve(skills);
        return;
      }

      const selectedIndices = [];
      const parts = input.split(',');
      
      for (const part of parts) {
        const trimmed = part.trim();
        if (trimmed.includes('-')) {
          // Range selection
          const [start, end] = trimmed.split('-').map(n => parseInt(n.trim()));
          if (!isNaN(start) && !isNaN(end)) {
            for (let i = start; i <= end; i++) {
              selectedIndices.push(i);
            }
          }
        } else {
          const num = parseInt(trimmed);
          if (!isNaN(num)) {
            selectedIndices.push(num);
          }
        }
      }

      const selectedSkills = [];
      for (const idx of selectedIndices) {
        if (idx >= 1 && idx <= skillList.length) {
          selectedSkills.push(skillList[idx - 1]);
        } else {
          console.log(`⚠️  Index ${idx} out of range, skipping.`);
        }
      }

      resolve(selectedSkills);
    });
  });
}

function parseFrontmatter(content) {
  const match = content.match(/^---\s*\n([\s\S]*?)\n---\s*\n/);
  if (!match) {
    return null;
  }
  
  try {
    return yaml.parse(match[1]);
  } catch (e) {
    console.error('Failed to parse YAML frontmatter:', e.message);
    return null;
  }
}

async function processSkills(rootDir, distDir, platform, skillsToBuild) {
  const distPlatformDir = path.join(distDir, `.${platform}`);
  
  // Clean and create distribution directory
  if (fs.existsSync(distPlatformDir)) {
    fs.rmSync(distPlatformDir, { recursive: true });
  }
  fs.mkdirSync(distPlatformDir, { recursive: true });
  fs.mkdirSync(path.join(distPlatformDir, 'skills'), { recursive: true });

  console.log(`Created platform-specific distribution directory: ${distPlatformDir}`);

  const allSkillsData = [];
  const errors = [];

  const modelMaps = {
    gemini: { sonnet: 'gemini-ultra', haiku: 'gemini-pro' },
    codex: { sonnet: 'gpt-4', haiku: 'gpt-3.5-turbo' }
  };

  let platformContent = [];
  if (platform === 'gemini' || platform === 'codex') {
    platformContent.push(`# Generated ${platform.charAt(0).toUpperCase() + platform.slice(1)} Skill Definitions\n`);
    platformContent.push('from typing import List, Dict, Any\n\n');
  }

  for (const skill of skillsToBuild) {
    // Use the sourceFile property if available, otherwise construct path
    const skillFile = skill.sourceFile || path.join(skill.path, 'SKILL.md');
    
    try {
      const content = fs.readFileSync(skillFile, 'utf-8');
      const frontmatter = parseFrontmatter(content);
      
      // For agent files (.md files without SKILL.md), extract info differently
      let skillName = skill.name;
      let skillDescription = '';
      let skillModel = 'sonnet';
      let skillCategory = skill.category;
      
      if (frontmatter) {
        skillName = frontmatter.name || skill.name;
        skillDescription = frontmatter.description || '';
        skillModel = frontmatter.model || 'sonnet';
        skillCategory = frontmatter.category || skill.category;
      } else {
        // Extract description from first paragraph
        const paragraphs = content.split('\n\n').filter(p => p.trim());
        if (paragraphs.length > 0) {
          const firstPara = paragraphs[0].replace(/^#+\s*/, '').trim();
          skillDescription = firstPara.substring(0, 200);
        }
      }

      if (!skillName) {
        errors.push(`Missing name in ${skillFile}`);
        continue;
      }

      allSkillsData.push({
        name: skillName,
        category: skillCategory,
        description: skillDescription,
        type: skill.type || 'skill',
        model: skillModel,
        file_path: path.relative(rootDir, skillFile)
      });

      // Copy skill to distribution
      const destSkillDir = path.join(distPlatformDir, 'skills', skillName);
      fs.mkdirSync(destSkillDir, { recursive: true });
      fs.copyFileSync(skillFile, path.join(destSkillDir, 'SKILL.md'));

      // Copy sibling files if skill is a directory-based skill
      if (skill.sourceFile && skill.sourceFile.endsWith('SKILL.md') && skill.path !== skill.sourceFile) {
        const entries = fs.readdirSync(skill.path, { withFileTypes: true });
        for (const entry of entries) {
          if (entry.name === 'SKILL.md') continue;
          
          const src = path.join(skill.path, entry.name);
          const dest = path.join(destSkillDir, entry.name);
          
          if (entry.isDirectory() && !entry.name.startsWith('.') && 
              !['node_modules', '__pycache__', '.git', '.venv', 'venv'].includes(entry.name)) {
            fs.cpSync(src, dest, { recursive: true });
          } else if (entry.isFile()) {
            fs.copyFileSync(src, dest);
          }
        }
      }

      // Generate platform-specific code
      if (platform === 'gemini' || platform === 'codex') {
        const mappedModel = modelMaps[platform][skillModel] || skillModel;
        const className = skillName.replace(/-/g, '_').replace(/(^|_)([a-z])/g, (m, p1, p2) => (p1 ? '_' : '') + p2.toUpperCase()) + 'Skill';
        
        platformContent.push(`class ${className}:\n`);
        platformContent.push(`    name: str = "${skillName}"\n`);
        platformContent.push(`    description: str = "${skillDescription.replace(/"/g, '\\"')}"\n`);
        platformContent.push(`    category: str = "${skillCategory}"\n`);
        platformContent.push(`    type: str = "${skill.type || 'skill'}"\n`);
        platformContent.push(`    model: str = "${mappedModel}"\n`);
        
        const instructions = content.replace(/^---\s*\n[\s\S]*?\n---\s*\n/, '').trim();
        platformContent.push(`    ${platform === 'gemini' ? 'system_instruction' : 'prompt'}: str = """\n${instructions}\n"""\n\n`);
      }

    } catch (error) {
      errors.push(`Failed to process ${skillFile}: ${error.message}`);
    }
  }

  // Write platform-specific file
  if (platform === 'gemini' || platform === 'codex') {
    const platformFile = path.join(distPlatformDir, `${platform}_skills.py`);
    fs.writeFileSync(platformFile, platformContent.join(''), 'utf-8');
  }

  return { allSkillsData, errors };
}

function generateReadme(rootDir, skillsData) {
  console.log('Generating README.md...');
  
  const templatePath = path.join(rootDir, 'README.template.md');
  const readmePath = path.join(rootDir, 'README.md');
  
  if (!fs.existsSync(templatePath)) {
    console.log(c.warning('README.template.md not found, skipping README generation'));
    return;
  }

  // Group skills by category
  const byCategory = {};
  for (const skill of skillsData) {
    if (!byCategory[skill.category]) {
      byCategory[skill.category] = [];
    }
    byCategory[skill.category].push(skill);
  }

  const categoryOrder = [
    'workflow', 'architecture', 'code-quality', 'design', 'marketing', 'product',
    'business', 'devops', 'data', 'communication', 'research', 'project-management', 'skills'
  ];

  const categoryDescriptions = {
    workflow: 'Development process automation and methodology enforcement',
    architecture: 'The masterminds who design your digital empire',
    'code-quality': 'The guardians of clean, secure, and blazing-fast code',
    design: 'The creative geniuses who make everything beautiful',
    marketing: 'The word wizards who turn features into must-haves',
    product: 'The user champions who build products people actually want',
    business: 'The suit-wearing strategists who keep the lights on',
    devops: 'The infrastructure heroes who keep your app running while you sleep',
    data: 'The number crunchers who turn chaos into insights',
    communication: 'The translators who make tech speak human',
    research: 'The curious minds who keep you ahead of the curve',
    'project-management': 'The organizers who ensure on-time and on-budget delivery',
    skills: 'Specialized AI skills for common development tasks'
  };

  const mdParts = ['## 🤖 Your AI Dream Team\n\n*Meet your new coding sidekicks - each one a specialist in their field:*'];
  
  for (const category of categoryOrder) {
    if (byCategory[category]) {
      const skills = byCategory[category].sort((a, b) => a.name.localeCompare(b.name));
      mdParts.push(`\n### 🏗️ ${category.charAt(0).toUpperCase() + category.slice(1).replace(/-/g, ' ')} (${skills.length} skills)`);
      mdParts.push(`*${categoryDescriptions[category] || ''}*`);
      for (const skill of skills) {
        const desc = skill.description.split('.')[0];
        mdParts.push(`- **${skill.name}** - ${desc}.`);
      }
    }
  }

  const agentListMd = mdParts.join('\n');

  let templateContent = fs.readFileSync(templatePath, 'utf-8');
  let readmeContent = templateContent.replace('{{AGENT_LIST}}', agentListMd);
  
  readmeContent = readmeContent.replace(/Meet \d+ specialized AI agents/g, `Meet ${skillsData.length} specialized AI skills`);
  readmeContent = readmeContent.replace(/it's like having \d+ AI specialists/g, `it's like having ${skillsData.length} AI specialists`);

  fs.writeFileSync(readmePath, readmeContent, 'utf-8');
  console.log(c.success('Successfully generated README.md'));
}

function generatePlatformMd(distDir, skillsData, platform) {
  const filename = platform === 'claude' ? 'CLAUDE.md' : `${platform.toUpperCase()}.md`;
  const mdPath = path.join(distDir, filename);

  const content = [];
  content.push(`# ${filename}\n`);
  content.push(`Master configuration for ${platform.charAt(0).toUpperCase() + platform.slice(1)} Code. This file indexes available Skills.\n`);
  content.push('\n# Project Standards\n');
  content.push('<!-- Add project-wide standards here -->\n');
  content.push('- Follow the coding style defined in the project.\n');
  content.push('\n# Available Skills\n');
  content.push(`*${skillsData.length} skills ready to use*\n`);

  // Group by category
  const byCategory = {};
  for (const skill of skillsData) {
    if (!byCategory[skill.category]) {
      byCategory[skill.category] = [];
    }
    byCategory[skill.category].push(skill);
  }

  const categoryOrder = [
    'workflow', 'architecture', 'code-quality', 'design', 'marketing', 'product',
    'business', 'devops', 'data', 'communication', 'research', 'project-management', 'skills'
  ];

  for (const category of categoryOrder) {
    if (byCategory[category]) {
      const skills = byCategory[category].sort((a, b) => a.name.localeCompare(b.name));
      content.push(`\n## ${category.charAt(0).toUpperCase() + category.slice(1).replace(/-/g, ' ')}\n`);
      for (const skill of skills) {
        content.push(`- \`/${skill.name}\` - ${skill.description}`);
      }
    }
  }

  fs.writeFileSync(mdPath, content.join('\n'), 'utf-8');
}

async function main() {
  const args = parseArguments();

  if (args.help) {
    showHelp();
    process.exit(0);
  }

  const platform = args.platform;
  
  // Setup paths
  const rootDir = path.dirname(path.dirname(__filename));
  const skillsDir = path.join(rootDir, 'skills');
  const distDir = path.join(rootDir, 'dist');

  if (!fs.existsSync(skillsDir)) {
    console.error(c.error(`Error: Skills directory not found at ${skillsDir}`));
    process.exit(1);
  }

  // Get all available skills from multiple source directories
  const allAvailableSkills = getAllSkills(skillsDir, rootDir);

  if (allAvailableSkills.length === 0) {
    console.error(c.error('Error: No skills found in the skills directory.'));
    process.exit(1);
  }

  // Handle --list
  if (args.list) {
    listAllSkills(allAvailableSkills);
    process.exit(0);
  }

  // Determine which skills to build
  let skillsToBuild = [];

  if (args.all) {
    skillsToBuild = allAvailableSkills;
    console.log(`Building ALL ${skillsToBuild.length} skills for platform: ${platform}...`);
  } else if (args.skills) {
    const requestedSkills = args.skills.split(',').map(s => s.trim());
    const availableNames = new Set(allAvailableSkills.map(s => s.name));
    
    const invalidSkills = requestedSkills.filter(s => !availableNames.has(s));
    if (invalidSkills.length > 0) {
      console.log(c.warning(`\n⚠️  Warning: The following skills were not found: ${invalidSkills.join(', ')}`));
      console.log('   Run with --list to see available skills.\n');
    }

    skillsToBuild = allAvailableSkills.filter(s => requestedSkills.includes(s.name));
    
    if (skillsToBuild.length === 0) {
      console.error(c.error('❌ No valid skills selected. Exiting.'));
      process.exit(1);
    }

    console.log(`Building ${skillsToBuild.length} selected skills for platform: ${platform}...`);
  } else {
    // Interactive selection
    console.log(`No skills specified. Starting interactive selection for platform: ${platform}...`);
    skillsToBuild = await interactiveSkillSelector(allAvailableSkills);
    
    if (skillsToBuild.length === 0) {
      console.log(c.error('❌ No skills selected. Exiting.'));
      process.exit(0);
    }

    console.log(c.success(`\n✅ Selected ${skillsToBuild.length} skills to build.`));
  }

  // Confirm before building (unless --all or --skills was used)
  if (!args.all && !args.skills) {
    console.log('\nSelected skills:');
    for (const skill of skillsToBuild.sort((a, b) => a.name.localeCompare(b.name))) {
      console.log(`  • ${skill.name}`);
    }

    const readline = require('readline');
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    });

    const confirm = await new Promise((resolve) => {
      rl.question('\nProceed with build? [Y/n]: ', (answer) => {
        rl.close();
        resolve(answer.trim().toLowerCase());
      });
    });

    if (confirm && confirm !== 'y' && confirm !== 'yes') {
      console.log(c.error('❌ Build cancelled.'));
      process.exit(0);
    }
  }

  // Create distribution directory
  if (!fs.existsSync(distDir)) {
    fs.mkdirSync(distDir, { recursive: true });
  }

  // Process skills
  const { allSkillsData, errors } = await processSkills(rootDir, distDir, platform, skillsToBuild);

  if (errors.length === 0) {
    // Write manifest
    const manifestPath = path.join(distDir, 'skills.json');
    allSkillsData.sort((a, b) => a.name.localeCompare(b.name));
    fs.writeFileSync(manifestPath, JSON.stringify(allSkillsData, null, 2), 'utf-8');
    console.log(c.success(`\n✅ Successfully generated manifest at ${manifestPath}`));

    // Generate README
    if (platform === 'claude') {
      generateReadme(rootDir, allSkillsData);
    }

    // Generate platform config
    const distPlatformDir = path.join(distDir, `.${platform}`);
    generatePlatformMd(distPlatformDir, allSkillsData, platform);

    console.log(c.success(`\n🎉 Build process completed successfully! ${allSkillsData.length} skills processed.`));
  } else {
    console.log(c.warning('\n⚠️  Build process completed with errors:'));
    for (const error of errors) {
      console.log(`   - ${error}`);
    }
    process.exit(1);
  }
}

main().catch(error => {
  console.error(c.error(`❌ Unexpected error: ${error.message}`));
  process.exit(1);
});
