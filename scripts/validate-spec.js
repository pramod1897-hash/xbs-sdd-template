#!/usr/bin/env node
/**
 * validate-spec.js — SDD Spec Structure Validator
 *
 * Validates that a SPEC.md contains all required SDD sections.
 *
 * Usage: node scripts/validate-spec.js <path/to/SPEC.md>
 * Example: node scripts/validate-spec.js docs/features/create-account/SPEC.md
 */

const fs = require('fs');
const path = require('path');

const REQUIRED_SECTIONS = [
    { heading: '## Purpose', description: 'One-sentence description of what this does' },
    { heading: '## Inputs', description: 'All input parameters with types' },
    { heading: '## Outputs', description: 'Success and failure return values' },
    { heading: '## Business Rules', description: 'Business logic rules' },
    { heading: '## Edge Cases', description: 'Known edge cases and expected behaviour' },
    { heading: '## Acceptance Criteria', description: 'Testable acceptance criteria' },
];

const RECOMMENDED_SECTIONS = [
    { heading: '## Dependencies', description: 'External dependencies' },
];

function validateSpec(filePath) {
    const absolutePath = path.resolve(process.cwd(), filePath);
    if (!fs.existsSync(absolutePath)) {
        console.error(`\n❌ File not found: ${absolutePath}\n`);
        process.exit(1);
    }

    const content = fs.readFileSync(absolutePath, 'utf-8');
    const lines = content.split('\n');

    console.log(`\n🔍 Validating: ${filePath}`);
    console.log('─'.repeat(60));

    let errors = 0;
    let warnings = 0;

    console.log('\n📋 Required Sections:');
    for (const section of REQUIRED_SECTIONS) {
        const found = lines.some(line => line.trim().startsWith(section.heading));
        if (found) {
            console.log(`  ✅ ${section.heading}`);
        } else {
            console.log(`  ❌ MISSING: ${section.heading} — ${section.description}`);
            errors++;
        }
    }

    console.log('\n💡 Recommended Sections:');
    for (const section of RECOMMENDED_SECTIONS) {
        const found = lines.some(line => line.trim().startsWith(section.heading));
        if (found) {
            console.log(`  ✅ ${section.heading}`);
        } else {
            console.log(`  ⚠️  MISSING (recommended): ${section.heading} — ${section.description}`);
            warnings++;
        }
    }

    const acSectionIndex = lines.findIndex(l => l.trim().startsWith('## Acceptance Criteria'));
    if (acSectionIndex !== -1) {
        const acContent = lines.slice(acSectionIndex).join('\n');
        const hasGWT = acContent.includes('Given') && acContent.includes('When') && acContent.includes('Then');
        console.log('\n🧪 AC Quality:');
        if (hasGWT) {
            console.log('  ✅ Given/When/Then format detected');
        } else {
            console.log('  ⚠️  No Given/When/Then format — consider using it');
            warnings++;
        }

        const acMatches = acContent.match(/\*\*AC-\d+/g) || [];
        if (acMatches.length >= 3) {
            console.log(`  ✅ ${acMatches.length} acceptance criteria found`);
        } else {
            console.log(`  ⚠️  Only ${acMatches.length} AC found — consider adding more coverage`);
            warnings++;
        }
    }

    const hasTitle = lines.some(line => line.startsWith('# '));
    console.log('\n📄 Structure:');
    console.log(hasTitle ? '  ✅ Has H1 title' : '  ⚠️  No H1 title found');
    if (!hasTitle) warnings++;

    if (content.includes('[ASSUMPTION:') || content.includes('[NEEDS CLARIFICATION:')) {
        console.log('  ℹ️  Contains [ASSUMPTION] or [NEEDS CLARIFICATION] markers — resolve before implementation');
    }

    console.log('\n' + '─'.repeat(60));
    if (errors === 0 && warnings === 0) {
        console.log(`✅ SPEC VALID — ${filePath} is a complete SDD specification\n`);
        process.exit(0);
    } else if (errors === 0) {
        console.log(`⚠️  SPEC COMPLETE WITH WARNINGS — ${errors} errors, ${warnings} warnings\n`);
        process.exit(0);
    } else {
        console.log(`❌ SPEC INVALID — ${errors} errors, ${warnings} warnings\n`);
        process.exit(1);
    }
}

const args = process.argv.slice(2);
if (args.length === 0) {
    console.log('\nUsage: node scripts/validate-spec.js <path/to/SPEC.md>');
    console.log('Example: node scripts/validate-spec.js docs/features/create-account/SPEC.md\n');
    process.exit(1);
}

validateSpec(args[0]);
