import { readFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'
import type { LanguageRegistration } from '@shikijs/types'
import { defineConfig } from 'vitepress'
import { withMermaid } from 'vitepress-plugin-mermaid'
import { sidebarMulti } from './sidebar.generated'

const __dirname = dirname(fileURLToPath(import.meta.url))
const mettaGrammar = JSON.parse(
  readFileSync(join(__dirname, '../../metta.tmLanguage.json'), 'utf-8'),
) as LanguageRegistration

export default withMermaid(
  defineConfig({
    base: '/hyperon-experimental/',
    lang: 'zh-CN',
    title: 'OpenCog Hyperon 文档',
    description: 'MeTTa 语言、Rust 引擎、Python API 与系统架构的 Hyperon 说明文档。',
    themeConfig: {
      nav: [
        { text: '快速开始', link: '/' },
        {
          text: 'MeTTa语言',
          link: '/metta-lang/overview',
          activeMatch: '^/metta-lang/',
        },
        {
          text: '架构',
          link: '/architecture/overview',
          activeMatch: '^/architecture/',
        },
        {
          text: 'Rust引擎',
          link: '/rust-engine/lib-entry',
          activeMatch: '^/rust-engine/',
        },
        {
          text: 'Python API',
          link: '/python-source/runner',
          activeMatch: '^/python-source/',
        },
      ],
      sidebar: sidebarMulti,
      search: { provider: 'local' },
      editLink: {
        pattern:
          'https://github.com/trueagi/hyperon-experimental/edit/main/project_docs/output/docs/:path',
        text: '在 GitHub 上编辑此页',
      },
      socialLinks: [
        { icon: 'github', link: 'https://github.com/trueagi/hyperon-experimental' },
      ],
      docFooter: {
        prev: '上一页',
        next: '下一页',
      },
    },
    markdown: {
      lineNumbers: true,
      math: true,
      languages: [mettaGrammar],
    },
    mermaid: {
      theme: 'default',
    },
  }),
)