import { defineConfig } from 'vite';
import { resolve } from 'path';
import fs from 'fs';
import { createHtmlPlugin } from 'vite-plugin-html';

// Get all HTML files in the current directory
const htmlFiles = fs.readdirSync(__dirname).filter(file => file.endsWith('.html'));

const input = {};
htmlFiles.forEach(file => {
    const name = file.replace('.html', '');
    input[name] = resolve(__dirname, file);
});

export default defineConfig({
    plugins: [
        createHtmlPlugin({
            minify: true,
        }),
    ],
    build: {
        rollupOptions: {
            input: input,
        },
        outDir: 'dist',
    },
    base: './', // Use relative paths for assets
});
