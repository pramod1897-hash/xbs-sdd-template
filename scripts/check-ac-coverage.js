#!/usr/bin/env node
/**
 * check-ac-coverage.js
 *
 * Counts Acceptance Criterion labels in spec.md and compares against
 * test files to report AC coverage. Works with any test file that uses
 * AC-N labelling (JUnit @DisplayName, Jest describe/test, pytest names, etc.)
 *
 * Usage:
 *   node scripts/check-ac-coverage.js <spec-file> [test-file-or-dir...]
 *
 * Examples:
 *   node scripts/check-ac-coverage.js docs/features/PRJ-101-story/spec.md src/test/
 *   node scripts/check-ac-coverage.js docs/features/PRJ-101-story/spec.md src/test/java src/test/resources
 */

const fs = require('fs');
const path = require('path');

// ── Config ───────────────────────────────────────────────────────────────────

const AC_IN_SPEC_PATTERN = /(?:^###\s+AC-(\d+)|\*\*AC-(\d+)(?::|\.|\s))/gm;  // ### AC-N heading OR **AC-N:** bold
const AC_IN_TEST_PATTERN = /AC-(\d+)/g;               // AC-N anywhere in test files

const TEST_FILE_EXTENSIONS = ['.java', '.js', '.ts', '.py', '.go', '.kt', '.cs'];

// ── Helpers ──────────────────────────────────────────────────────────────────

function collectFiles(dirOrFile, results = []) {
    if (!fs.existsSync(dirOrFile)) return results;
    const stat = fs.statSync(dirOrFile);
    if (stat.isFile()) {
        if (TEST_FILE_EXTENSIONS.some(ext => dirOrFile.endsWith(ext))) {
            results.push(dirOrFile);
        }
    } else if (stat.isDirectory()) {
        for (const child of fs.readdirSync(dirOrFile)) {
            collectFiles(path.join(dirOrFile, child), results);
        }
    }
    return results;
}

function extractACsFromSpec(specPath) {
    const content = fs.readFileSync(specPath, 'utf8');
    const acs = new Set();
    let match;
    // Matches: ### AC-N (heading) OR **AC-N:** bold — captures group 1 or 2
    const re = /(?:^###\s+AC-(\d+)|\*\*AC-(\d+)(?::|\.|\s))/gm;
    while ((match = re.exec(content)) !== null) {
        const num = match[1] || match[2];
        acs.add(parseInt(num, 10));
    }
    return acs;
}

function extractACsFromTestFiles(testPaths) {
    const coverage = {};  // acNumber → [files]
    for (const filePath of testPaths) {
        const content = fs.readFileSync(filePath, 'utf8');
        const re = /AC-(\d+)/g;
        let match;
        while ((match = re.exec(content)) !== null) {
            const ac = parseInt(match[1], 10);
            if (!coverage[ac]) coverage[ac] = [];
            const rel = path.relative(process.cwd(), filePath);
            if (!coverage[ac].includes(rel)) coverage[ac].push(rel);
        }
    }
    return coverage;
}

// ── Main ─────────────────────────────────────────────────────────────────────

const args = process.argv.slice(2);
if (args.length < 1) {
    console.error('Usage: node scripts/check-ac-coverage.js <spec-file> [test-file-or-dir...]');
    process.exit(1);
}

const specFile = args[0];
const testPaths = args.slice(1);

if (!fs.existsSync(specFile)) {
    console.error(`❌ Spec file not found: ${specFile}`);
    process.exit(1);
}

// Collect test files
const testFiles = [];
if (testPaths.length === 0) {
    // Default: search common test dirs
    for (const dir of ['src/test', 'test', '__tests__', 'tests']) {
        collectFiles(dir, testFiles);
    }
} else {
    for (const p of testPaths) collectFiles(p, testFiles);
}

// Extract ACs
const specACs = extractACsFromSpec(specFile);
const testCoverage = extractACsFromTestFiles(testFiles);

// ── Report ───────────────────────────────────────────────────────────────────

const maxAC = Math.max(...specACs, ...Object.keys(testCoverage).map(Number), 0);

console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.log('  AC Coverage Report');
console.log(`  Spec:  ${path.relative(process.cwd(), specFile)}`);
console.log(`  Tests: ${testFiles.length} file(s) scanned`);
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

let covered = 0;
let missing = 0;
const ghostACs = [];

for (let i = 1; i <= maxAC; i++) {
    if (specACs.has(i)) {
        const files = testCoverage[i];
        if (files && files.length > 0) {
            console.log(`  ✅ AC-${i}  → ${files.join(', ')}`);
            covered++;
        } else {
            console.log(`  ❌ AC-${i}  → NOT COVERED`);
            missing++;
        }
    } else if (testCoverage[i]) {
        // AC in tests but not in spec
        ghostACs.push(i);
    }
}

if (ghostACs.length > 0) {
    console.log(`\n  ⚠️  Ghost ACs (in tests but not in spec): AC-${ghostACs.join(', AC-')}`);
    console.log('     → Check if spec.md is up to date');
}

const total = specACs.size;
const pct = total === 0 ? 0 : Math.round((covered / total) * 100);

console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.log(`  Coverage: ${covered}/${total} ACs (${pct}%)`);
if (missing > 0) {
    console.log(`  ❌ ${missing} AC(s) missing test coverage`);
} else {
    console.log('  ✅ All ACs covered');
}
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

process.exit(missing > 0 ? 1 : 0);
