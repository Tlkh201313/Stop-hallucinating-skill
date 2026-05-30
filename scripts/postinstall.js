#!/usr/bin/env node

/**
 * Postinstall script - shows quick guide after npm install
 */

const colors = {
  reset: '\x1b[0m',
  cyan: '\x1b[36m',
  green: '\x1b[32m',
  bold: '\x1b[1m',
  dim: '\x1b[2m',
};

console.log(`
${colors.bold}${colors.cyan}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${colors.reset}
${colors.bold}${colors.cyan}  🛡️  Anti-Hallucination Skill Installed!${colors.reset}
${colors.bold}${colors.cyan}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${colors.reset}

${colors.bold}Quick Start:${colors.reset}

  ${colors.green}npx anti-hallucination-skill install${colors.reset}
    Install the skill to OpenCode

  ${colors.green}npx anti-hallucination-skill validate --text "Your text"${colors.reset}
    Check text for hallucination signals

  ${colors.green}npx anti-hallucination-skill guide${colors.reset}
    Show the quick reference guide

  ${colors.green}npx anti-hallucination-skill prompt structured${colors.reset}
    Show the structured output template

${colors.dim}Full docs: https://github.com/Tlkh201313/Stop-hallucinating-skill${colors.reset}
`);
