#!/usr/bin/env node

import { Level } from 'level';
import LZString from 'lz-string';
import fs from 'fs';
import path from 'path';

const { decompressFromUTF16, decompressFromBase64 } = LZString;

// -----------------------------
// CLI argument handling
// -----------------------------
const dbDir = process.argv[2];

if (!dbDir) {
  console.error('Usage: node extract_all_json.ts <path-to-leveldb-directory>');
  process.exit(1);
}

if (!fs.existsSync(dbDir) || !fs.statSync(dbDir).isDirectory()) {
  console.error(`Not a directory: ${dbDir}`);
  process.exit(1);
}

// -----------------------------
// Open LevelDB
// -----------------------------
const db = new Level(dbDir, {
  keyEncoding: 'utf8',
  valueEncoding: 'utf8'
});

// -----------------------------
// Helpers
// -----------------------------
function tryDecompress(value: string): string | null {
  return (
    decompressFromUTF16(value) ||
    decompressFromBase64(value) ||
    value // fallback: maybe uncompressed JSON
  );
}

// -----------------------------
// Main extraction
// -----------------------------
async function run() {
  let count = 0;

  for await (const [key, value] of db.iterator()) {
    const decompressed = tryDecompress(value);

    try {
      const doc = JSON.parse(decompressed);
      count++;

      console.log('----------------------------------------');
      console.log(`Key: ${key}`);
      console.log(JSON.stringify(doc, null, 2));
      console.log('');
    } catch {
      // Not JSON, ignore
    }
  }

  console.log(`\nExtracted ${count} JSON documents.`);
}

run()
  .catch(err => {
    console.error('Fatal error:', err);
    process.exit(1);
  })
  .finally(async () => {
    await db.close();
  });
