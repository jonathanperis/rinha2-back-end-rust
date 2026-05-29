import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';
import { satteri } from '@astrojs/markdown-satteri';

const isProd = process.env.NODE_ENV === 'production';

export default defineConfig({
  integrations: [sitemap()],
  markdown: {
    processor: satteri(),
  },
  output: 'static',
  outDir: 'out',
  site: 'https://jonathanperis.github.io',
  base: isProd ? '/rinha2-back-end-rust' : '',
  vite: {
    plugins: [tailwindcss()],
  },
});
