#!/usr/bin/env node

/**
 * anti-hallucination-skill CLI
 * 
 * Usage:
 *   npx anti-hallucination-skill install   - Install skill to OpenCode
 *   npx anti-hallucination-skill validate  - Validate text for hallucinations
 *   npx anti-hallucination-skill prompt    - Show prompt templates
 *   npx anti-hallucination-skill guide     - Open the full guide
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// ANSI colors
const colors = {
  reset: '\x1b[0m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m',
  bold: '\x1b[1m',
  dim: '\x1b[2m',
};

function log(msg) { console.log(msg); }
function success(msg) { console.log(`${colors.green}✅ ${msg}${colors.reset}`); }
function warn(msg) { console.log(`${colors.yellow}⚠️  ${msg}${colors.reset}`); }
function error(msg) { console.log(`${colors.red}❌ ${msg}${colors.reset}`); }
function info(msg) { console.log(`${colors.cyan}ℹ️  ${msg}${colors.reset}`); }
function header(msg) {
  console.log(`\n${colors.bold}${colors.cyan}${'='.repeat(60)}${colors.reset}`);
  console.log(`${colors.bold}${colors.cyan}  ${msg}${colors.reset}`);
  console.log(`${colors.bold}${colors.cyan}${'='.repeat(60)}${colors.reset}\n`);
}

// Get the skill directory (where the package is installed)
function getSkillDir() {
  return path.join(__dirname, '..', 'skill');
}

// Get OpenCode skills directory
function getOpenCodeSkillsDir() {
  const homeDir = require('os').homedir();
  
  // Check common locations
  const candidates = [
    path.join(homeDir, '.config', 'opencode', 'skills'),
    path.join(homeDir, '.opencode', 'skills'),
    path.join(homeDir, '.claude', 'skills'),
  ];
  
  for (const candidate of candidates) {
    if (fs.existsSync(path.dirname(candidate))) {
      return candidate;
    }
  }
  
  // Default to .config/opencode/skills
  return path.join(homeDir, '.config', 'opencode', 'skills');
}

// Install skill to OpenCode
function installSkill() {
  header('Installing Anti-Hallucination Skill');
  
  const skillDir = getSkillDir();
  const targetDir = path.join(getOpenCodeSkillsDir(), 'anti-hallucination');
  
  log(`Source: ${skillDir}`);
  log(`Target: ${targetDir}\n`);
  
  // Check if skill dir exists
  if (!fs.existsSync(skillDir)) {
    error('Skill directory not found. Package may be corrupted.');
    process.exit(1);
  }
  
  // Create target directory
  fs.mkdirSync(targetDir, { recursive: true });
  
  // Copy files
  const files = fs.readdirSync(skillDir);
  let copied = 0;
  
  for (const file of files) {
    const srcPath = path.join(skillDir, file);
    const destPath = path.join(targetDir, file);
    
    if (fs.statSync(srcPath).isDirectory()) {
      fs.mkdirSync(destPath, { recursive: true });
      const subFiles = fs.readdirSync(srcPath);
      for (const subFile of subFiles) {
        fs.copyFileSync(path.join(srcPath, subFile), path.join(destPath, subFile));
        copied++;
      }
    } else {
      fs.copyFileSync(srcPath, destPath);
      copied++;
    }
  }
  
  success(`Installed ${copied} files to ${targetDir}`);
  info('The skill is now available in OpenCode.');
  log('\nUsage:');
  log('  - The skill will auto-trigger when you ask about hallucinations');
  log('  - Or manually: "Use the anti-hallucination skill"');
  log(`\nFiles location: ${targetDir}`);
}

// Validate text for hallucinations
function validateText(text, options = {}) {
  header('Hallucination Risk Assessment');
  
  // Red flag patterns
  const patterns = {
    fabricated_statistic: {
      regex: /\b\d{2,3}%\b/g,
      severity: 'HIGH',
      desc: 'Precise percentage without source',
    },
    unsourced_studies: {
      regex: /(?:studies|research|evidence)\s+(?:show|suggest|indicate|demonstrate)/gi,
      severity: 'HIGH',
      desc: '"Studies show" without citation',
    },
    vague_authority: {
      regex: /(?:experts|scientists|researchers|doctors)\s+(?:say|believe|agree|recommend)/gi,
      severity: 'MEDIUM',
      desc: 'Vague appeal to authority',
    },
    invented_quote: {
      regex: /(?:as\s+\w+\s+(?:once\s+)?said|according\s+to\s+\w+)/gi,
      severity: 'MEDIUM',
      desc: 'Attribution (may be misattributed)',
    },
  };
  
  // Good patterns
  const goodPatterns = {
    hedging: /(?:i(?:'m|\s+am)\s+not\s+(?:sure|certain)|i\s+don(?:'t|\s+not)\s+know|please\s+verify|check\s+(?:the|your))/gi,
    grounding: /\[Source:\s*[^\]]+\]|\[Doc:\s*[^\]]+\]|according\s+to\s+the\s+(?:provided|source)/gi,
  };
  
  const flags = [];
  const good = [];
  
  // Check red flags
  for (const [name, pattern] of Object.entries(patterns)) {
    const matches = text.match(pattern.regex);
    if (matches) {
      for (const match of matches) {
        flags.push({ type: name, severity: pattern.severity, desc: pattern.desc, match });
      }
    }
  }
  
  // Check good patterns
  for (const [name, pattern] of Object.entries(goodPatterns)) {
    const matches = text.match(pattern);
    if (matches) {
      good.push({ type: name, count: matches.length });
    }
  }
  
  // Calculate risk
  let riskScore = 50;
  for (const flag of flags) {
    riskScore += flag.severity === 'HIGH' ? 15 : flag.severity === 'MEDIUM' ? 8 : 3;
  }
  for (const g of good) {
    riskScore -= g.count * 5;
  }
  riskScore = Math.max(0, Math.min(100, riskScore));
  
  const riskLevel = riskScore >= 75 ? 'HIGH' : riskScore >= 50 ? 'MEDIUM' : riskScore >= 25 ? 'LOW' : 'MINIMAL';
  const riskEmoji = { HIGH: '🔴', MEDIUM: '🟡', LOW: '🟢', MINIMAL: '✅' }[riskLevel];
  
  // Display results
  log(`${riskEmoji} Risk Level: ${riskLevel} (Score: ${riskScore}/100)\n`);
  
  if (flags.length > 0) {
    log(`${colors.red}Red Flags Found: ${flags.length}${colors.reset}`);
    for (const flag of flags.slice(0, 10)) {
      const sevColor = flag.severity === 'HIGH' ? colors.red : colors.yellow;
      log(`  ${sevColor}[${flag.severity}]${colors.reset} ${flag.desc}: "${flag.match}"`);
    }
    if (flags.length > 10) log(`  ... and ${flags.length - 10} more`);
    log('');
  }
  
  if (good.length > 0) {
    log(`${colors.green}Good Signs:${colors.reset}`);
    for (const g of good) {
      log(`  ✅ ${g.type}: ${g.count} found`);
    }
    log('');
  }
  
  if (riskLevel === 'HIGH') {
    error('VALIDATION FAILED — High hallucination risk');
    if (!options.json) process.exit(1);
  } else {
    success('VALIDATION PASSED');
  }
  
  if (options.json) {
    console.log(JSON.stringify({ riskLevel, riskScore, flags, good }, null, 2));
  }
}

// Show prompt templates
function showPrompts(template) {
  header('Anti-Hallucination Prompt Templates');
  
  const templates = {
    minimal: `You are a factual assistant. Follow these rules strictly:
- If you are uncertain about any claim, say "I'm not confident about this" before stating it.
- If you do not know the answer, say "I don't know" rather than guessing.
- Do not fabricate citations, statistics, names, or examples.
- Distinguish clearly between facts you are certain of and inferences you are making.`,

    research: `You are operating in RESEARCH MODE. Apply the following guardrails:

FACTUAL ACCURACY:
- Only assert facts you can support with evidence from the provided materials.
- For every claim, identify whether it is: (a) directly stated, (b) inferred, or (c) speculative.

UNCERTAINTY HANDLING:
- Use "I don't know" freely when you lack information.
- Never use hedged language to sneak in a guess.

CITATIONS:
- Every non-trivial factual claim must cite a source. Format: [Source: ...]
- If you can't cite it, don't state it as fact.

FORBIDDEN:
- No invented statistics, citations, or paper references
- No speculative cause-and-effect presented as established fact`,

    structured: `Respond in this exact JSON format:
{
  "answer": "Your answer here",
  "claims": [
    {
      "statement": "The factual claim",
      "confidence": "HIGH|MEDIUM|LOW",
      "source": "Exact quote from source document, or null",
      "verified": true|false
    }
  ],
  "unanswered": ["Questions you could not answer"],
  "caveats": ["Important limitations"]
}

RULES:
- Every claim MUST have a "source" field
- If no source exists, "verified" MUST be false
- Claims with "verified": false will be removed before delivery
- NEVER set "verified": true without an exact source quote`,
  };
  
  if (template && templates[template]) {
    log(`${colors.bold}Template: ${template}${colors.reset}\n`);
    log(templates[template]);
  } else {
    log(`${colors.bold}Available templates:${colors.reset}\n`);
    for (const [name, content] of Object.entries(templates)) {
      log(`${colors.cyan}--- ${name} ---${colors.reset}`);
      log(content);
      log('');
    }
    log(`Usage: npx anti-hallucination-skill prompt <template>`);
    log(`Example: npx anti-hallucination-skill prompt minimal`);
  }
}

// Show guide
function showGuide() {
  header('Anti-Hallucination Quick Guide');
  
  log(`${colors.bold}1. Immediate Fix (No Code Changes)${colors.reset}`);
  log(`   Add to your system prompt: "If uncertain, say 'I don't know'. Never fabricate."\n`);
  
  log(`${colors.bold}2. Strongest Enforcement${colors.reset}`);
  log(`   Use structured JSON output with required "source" and "verified" fields.\n`);
  
  log(`${colors.bold}3. Domain-Specific Rules${colors.reset}`);
  log(`   Legal: NEVER cite cases without verification`);
  log(`   Medical: ALWAYS include disclaimer + source for dosages`);
  log(`   Code: VERIFY package names against PyPI/npm`);
  log(`   Financial: ALWAYS include date for figures\n`);
  
  log(`${colors.bold}4. Validation${colors.reset}`);
  log(`   Run: npx anti-hallucination-skill validate --text "Your text"\n`);
  
  log(`${colors.bold}5. Full Documentation${colors.reset}`);
  log(`   Read: SKILL.md, prompt-templates.md, domain-specific.md`);
  log(`   Examples: references/examples.md`);
  log(`   Measurement: references/measurement.md\n`);
  
  log(`${colors.bold}Key Principle:${colors.reset}`);
  log(`   ${colors.cyan}Prefer refusal over hallucination. "I don't know" is always${colors.reset}`);
  log(`   ${colors.cyan}better than a confident but wrong answer.${colors.reset}`);
}

// Main CLI
function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  
  // Show help if no command
  if (!command || command === '--help' || command === '-h') {
    header('Anti-Hallucination Skill CLI');
    log(`${colors.bold}Usage:${colors.reset}`);
    log(`  npx anti-hallucination-skill install           Install skill to OpenCode`);
    log(`  npx anti-hallucination-skill validate --text "..." Validate text`);
    log(`  npx anti-hallucination-skill validate --file f.txt Validate file`);
    log(`  npx anti-hallucination-skill prompt [template]  Show prompt templates`);
    log(`  npx anti-hallucination-skill guide              Show quick guide`);
    log(`  npx anti-hallucination-skill readme             Show README`);
    log('');
    log(`${colors.bold}Shortcuts:${colors.reset}`);
    log(`  npx anti-hall install`);
    log(`  npx anti-hall validate --text "..."`);
    log('');
    log(`${colors.bold}Examples:${colors.reset}`);
    log(`  npx anti-hallucination-skill install`);
    log(`  npx anti-hallucination-skill validate --text "Studies show 73% of users..."`);
    log(`  npx anti-hallucination-skill prompt structured`);
    log('');
    return;
  }
  
  // Parse command
  switch (command.toLowerCase()) {
    case 'install':
    case 'setup':
      installSkill();
      break;
      
    case 'validate':
    case 'check':
    case 'audit':
      const textIdx = args.indexOf('--text');
      const fileIdx = args.indexOf('--file');
      const jsonFlag = args.includes('--json');
      
      let text = '';
      if (textIdx !== -1 && args[textIdx + 1]) {
        text = args[textIdx + 1];
      } else if (fileIdx !== -1 && args[fileIdx + 1]) {
        const filePath = args[fileIdx + 1];
        if (!fs.existsSync(filePath)) {
          error(`File not found: ${filePath}`);
          process.exit(1);
        }
        text = fs.readFileSync(filePath, 'utf-8');
      } else {
        error('Please provide --text "..." or --file path');
        log('Usage: npx anti-hallucination-skill validate --text "Your text here"');
        process.exit(1);
      }
      
      validateText(text, { json: jsonFlag });
      break;
      
    case 'prompt':
    case 'prompts':
    case 'template':
    case 'templates':
      showPrompts(args[1]);
      break;
      
    case 'guide':
    case 'help':
    case 'quickstart':
      showGuide();
      break;
      
    case 'readme':
    case 'docs':
      const readmePath = path.join(__dirname, '..', 'README.md');
      if (fs.existsSync(readmePath)) {
        log(fs.readFileSync(readmePath, 'utf-8'));
      } else {
        error('README.md not found');
      }
      break;
      
    case 'version':
    case '--version':
    case '-v':
      const pkg = require('../package.json');
      log(`anti-hallucination-skill v${pkg.version}`);
      break;
      
    default:
      error(`Unknown command: ${command}`);
      log('Run "npx anti-hallucination-skill --help" for usage');
      process.exit(1);
  }
}

main();
