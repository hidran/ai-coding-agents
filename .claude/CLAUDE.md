# CLAUDE.md

Master configuration for Claude Code. This file indexes available Skills, Rules, and Subagents.


# Project Standards

<!-- Add project-wide standards here (e.g., framework conventions, code quality, accessibility) -->

- Follow the coding style defined in the project.


# Skills & Subagents


## Available Skills

### Framework Generators
- `/angular-component` - Generates production-ready Angular standalone components with signals, TypeScript, unit tests (Jasmine/Jest), and Storybook stories.
- `/angular-feature` - Generates a complete Angular feature with standalone components, service, routes, guards, resolver, and tests.
- `/laravel-feature` - Generates a Laravel feature set including Model, Migration, Controller, FormRequest, and Policy.
- `/laravel-action` - Generates a single-action class with __invoke, validation, authorization. Usable as controller action, queued job, or console command.
- `/laravel-api-resource` - Generates API Resource and Collection classes for JSON transformation with conditional attributes, relationships, and pagination meta.
- `/laravel-command` - Generates Artisan console commands with arguments, options, scheduling, progress bars, interactive prompts, and tests.
- `/laravel-event` - Generates an Event with Listener, queued Job, and Notification. Full async event-driven pipeline with tests.
- `/laravel-livewire` - Generates Livewire 3 components with form objects, validation, real-time features, Alpine.js integration, and tests.
- `/laravel-middleware` - Generates HTTP middleware with before/after/terminable patterns, route registration, and tests.
- `/laravel-service` - Generates a Service class with interface, ServiceProvider binding, dependency injection, and unit tests.
- `/laravel-test` - Generates Feature and Unit tests with factories, HTTP testing, database assertions, and mocking. Supports PHPUnit and Pest.
- `/nestjs-resource` - Generates a complete NestJS resource (Module, Controller, Service, DTOs, Entities) following clean architecture principles.
- `/nextjs-page` - Generates a Next.js 14+ App Router page with metadata, loading state, error handling, and server/client component separation.
- `/react-component` - Generates production-ready React components with TypeScript, tests (Vitest/Jest), Storybook stories, and Tailwind CSS.
- `/symfony-bundle` - Generates a Symfony bundle structure or a feature set (Entity, Repository, Controller, Form) within an existing app.

### Architecture & Documentation
- `/adr` - Generates Architecture Decision Records (ADRs) with context, decision, consequences, and maintains an index.
- `/api-spec` - Generates OpenAPI 3.1 specifications from natural language descriptions. Outputs YAML with paths, schemas, authentication, and examples.

### Testing & Quality
- `/test-suite` - Scaffolds test files for existing code. Supports PHPUnit, Pest, Jest, and Vitest with arrange/act/assert pattern.
- `/typescript-best-practices` - TypeScript code review and best practices. Provides dos and don'ts for type design, naming conventions, generics, and patterns.

### DevOps & Infrastructure
- `/docker-compose` - Generates Docker Compose development environments for Laravel (PHP, MySQL, Redis, Nginx) and Node.js (Node, PostgreSQL, Redis) stacks.
- `/env-setup` - Generates environment configuration including .env files, .env.example, Makefile with common commands, and a setup script for developer onboarding.
- `/github-actions` - Generates CI/CD pipelines for GitHub Actions. Supports Laravel, NestJS, Angular, and React with testing, linting, building, and deployment stages.

## Project Rules (auto-loaded by path)

- `brand-guidelines` - Applies Anthropic's official brand colors and typography to any sort of artifact that may benefit from having Anthropic's look-and-feel. Use it when brand colors or style guidelines, visual formatting, or company design standards apply.
- `developer-growth-analysis` - Analyzes your recent Claude Code chat history to identify coding patterns, development gaps, and areas for improvement, curates relevant learning resources from HackerNews, and automatically sends a personalized growth report to your Slack DMs.
- `docx` - Comprehensive document creation, editing, and analysis with support for tracked changes, comments, formatting preservation, and text extraction. When Claude needs to work with professional documents (.docx files) for: (1) Creating new documents, (2) Modifying or editing content, (3) Working with tracked changes, (4) Adding comments, or any other document tasks
- `pdf` - Comprehensive PDF manipulation toolkit for extracting text and tables, creating new PDFs, merging/splitting documents, and handling forms. When Claude needs to fill in a PDF form or programmatically process, generate, or analyze PDF documents at scale.
- `pptx` - Presentation creation, editing, and analysis. When Claude needs to work with presentations (.pptx files) for: (1) Creating new presentations, (2) Modifying or editing content, (3) Working with layouts, (4) Adding comments or speaker notes, or any other presentation tasks
- `xlsx` - Comprehensive spreadsheet creation, editing, and analysis with support for formulas, formatting, data analysis, and visualization. When Claude needs to work with spreadsheets (.xlsx, .xlsm, .csv, .tsv, etc) for: (1) Creating new spreadsheets with formulas and formatting, (2) Reading or analyzing data, (3) Modify existing spreadsheets while preserving formulas, (4) Data analysis and visualization in spreadsheets, or (5) Recalculating formulas
- `youtube-downloader` - Download YouTube videos with customizable quality and format options. Use this skill when the user asks to download, save, or grab YouTube videos. Supports various quality settings (best, 1080p, 720p, 480p, 360p), multiple formats (mp4, webm, mkv), and audio-only downloads as MP3.

## Subagents

- `accessibility-checker` - Use this agent when you need to audit accessibility compliance, ensure WCAG standards, or make interfaces inclusive for users with disabilities. Call this agent when reviewing interfaces, before major releases, or when addressing accessibility requirements.
- `ad-copy-creator` - Use this agent when you need to create paid advertising copy for Google Ads, Facebook Ads, LinkedIn Ads, or other platforms. Call this agent when launching ad campaigns, optimizing ad performance, or creating promotional content for paid channels.
- `agile-coach` - Use this agent when you need help with Agile methodologies, Sprint planning, Retrospectives, or improving team processes. Call this agent to resolve team friction, optimize workflows, or facilitate ceremonies.
- `analytics-setup` - Use this agent when you need to implement analytics tracking, set up measurement systems, or create data collection strategies. Call this agent when setting up product analytics, tracking user behavior, or implementing data-driven decision systems.
- `api-designer` - Use this agent when you need to design REST APIs, GraphQL schemas, or other API interfaces. Call this agent when planning API architecture, defining endpoints, or creating API documentation and specifications.
- `api-documenter` - Use this agent when you need to create API documentation, developer references, or integration guides. Call this agent when documenting REST APIs, GraphQL schemas, or any developer-facing API interfaces.
- `backup-planner` - Use this agent when you need to design backup strategies, plan disaster recovery, or implement data protection systems. Call this agent when setting up data protection, planning for disasters, or ensuring business continuity.
- `best-practice-finder` - Use this agent when you need to research industry best practices, development standards, or proven methodologies. Call this agent when implementing new processes, improving existing systems, or ensuring adherence to industry standards.
- `blog-writer` - Use this agent when you need to create technical blog posts, tutorials, or content marketing articles. Call this agent when building thought leadership, explaining technical concepts, or creating educational content that drives traffic and engagement.
- `brand-designer` - Use this agent when you need to create brand identity elements, design logos, or establish visual brand guidelines. Call this agent when starting new projects, rebranding, or creating consistent brand experiences across your application.
- `business-model-analyzer` - Use this agent when you need to analyze business models, evaluate monetization strategies, or optimize business operations. Call this agent when planning business strategy, evaluating pivots, or optimizing existing business models.
- `changelog-writer` - Use this agent when you need to create release notes, changelogs, or product update communications. Call this agent when releasing new features, fixing bugs, or communicating product changes to users.
- `code-reviewer` - Use this agent when you need expert code review and quality analysis. Call this agent after writing new code, before committing changes, or when you want to improve code quality and catch potential issues.
- `color-specialist` - Use this agent when you need to choose color schemes, create color palettes, or ensure color accessibility. Call this agent when designing interfaces, establishing brand colors, or optimizing color contrast and accessibility.
- `competitor-researcher` - Use this agent when you need to analyze competitors, research market positioning, or understand competitive landscape. Call this agent when planning product strategy, evaluating market opportunities, or responding to competitive threats.
- `copywriter` - Use this agent when you need compelling marketing copy, product descriptions, headlines, or persuasive content. Call this agent when creating landing pages, writing product copy, crafting email campaigns, or developing marketing materials.
- `cost-optimizer` - Use this agent when you need to analyze and reduce cloud infrastructure costs, optimize resource usage, or plan cost-effective scaling strategies. Call this agent when cloud bills are high, when optimizing for efficiency, or when planning budget-conscious growth.
- `dashboard-planner` - Use this agent when you need to design operational dashboards, plan business intelligence interfaces, or create data monitoring systems. Call this agent when building executive dashboards, real-time monitoring interfaces, or comprehensive data visualization systems.
- `data-visualizer` - Use this agent when you need to create charts, graphs, or visual representations of data. Call this agent when presenting data insights, creating reports, or building data visualization dashboards.
- `database-planner` - Use this agent when you need to design database schemas, plan data models, optimize queries, or solve database-related architectural challenges. Call this agent when setting up new databases, migrating data structures, or optimizing database performance.
- `deployment-troubleshooter` - Use this agent when you need to fix deployment issues, resolve CI/CD problems, or troubleshoot infrastructure deployments. Call this agent when deployments fail, when experiencing environment issues, or when setting up deployment pipelines.
- `design-system-builder` - Use this agent to create and manage comprehensive design systems. Call this agent when you need to establish consistent design patterns, create reusable component libraries, or define the visual language (colors, typography, icons, layout) for a project.
- `documentation-writer` - Use this agent when you need to create or improve code documentation, API docs, README files, or technical documentation. Call this agent when code lacks proper documentation, when onboarding new team members, or when preparing for code handoffs.
- `email-writer` - Use this agent when you need to create email campaigns, newsletters, or automated email sequences. Call this agent when setting up email marketing, creating welcome sequences, or developing email communication strategies.
- `error-investigator` - Use this agent when you need to debug production issues, analyze error logs, or troubleshoot system problems. Call this agent when experiencing outages, investigating bugs, or analyzing system failures.
- `feature-prioritizer` - Use this agent when you need to prioritize feature requests, evaluate competing development options, or make strategic product decisions. Call this agent when managing product backlogs, responding to user feedback, or planning development roadmaps.
- `feature-spec-writer` - Use this agent when you need to write detailed technical specifications for new features or system components. Call this agent when planning feature development, documenting requirements, or creating technical design documents.
- `feedback-analyzer` - Use this agent when you need to analyze user feedback, customer reviews, or support tickets to extract actionable insights. Call this agent when processing user feedback, analyzing satisfaction surveys, or identifying product improvement opportunities.
- `financial-planner` - Use this agent when you need to create financial projections, analyze business finances, or plan funding strategies. Call this agent when preparing for investment, analyzing financial performance, or planning business growth.
- `icon-designer` - Use this agent when you need to design custom icons, create iconography systems, or plan visual symbols for your application. Call this agent when building icon libraries, creating custom graphics, or establishing consistent visual language.
- `landing-page-writer` - Use this agent when you need to create high-converting landing page copy, optimize conversion rates, or write persuasive sales pages. Call this agent when launching new products, creating marketing campaigns, or improving existing landing page performance.
- `layout-designer` - Use this agent when you need to create page layouts, design responsive grid systems, or plan content organization. Call this agent when building new pages, optimizing mobile experiences, or creating consistent layout patterns.
- `library-evaluator` - Use this agent when you need to evaluate libraries, frameworks, or development tools for specific projects. Call this agent when choosing between technical options, evaluating third-party solutions, or making technology stack decisions.
- `market-researcher` - Use this agent when you need to research target markets, analyze customer segments, or understand market opportunities. Call this agent when validating product ideas, planning go-to-market strategies, or analyzing market trends.
- `monitoring-setup` - Use this agent when you need to set up monitoring, alerting, or observability systems. Call this agent when implementing monitoring solutions, creating dashboards, or setting up incident response systems.
- `performance-optimizer` - Use this agent when you need to analyze and optimize code performance, identify bottlenecks, or improve application speed and efficiency. Call this agent when experiencing performance issues, before production deployment, or when optimizing critical code paths.
- `presentation-builder` - Use this agent when you need to create presentations, pitch decks, or structured presentation content. Call this agent when building investor pitches, technical presentations, or stakeholder communications.
- `pricing-strategist` - Use this agent when you need to develop pricing models, analyze pricing strategies, or optimize revenue structures. Call this agent when launching products, evaluating pricing changes, or responding to competitive pressure.
- `privacy-policy-writer` - Use this agent when you need to create or update privacy policies, ensure GDPR compliance, or handle data protection requirements. Call this agent when launching products, updating data practices, or addressing privacy compliance needs.
- `project-planner` - Use this agent when you need to break down large initiatives into tasks, create roadmaps, or manage project timelines. Call this agent when starting a new epic, estimating effort, or organizing a backlog.
- `refactoring-expert` - Use this agent when you need to refactor existing code, improve code structure, or modernize legacy code. Call this agent when code has become difficult to maintain, when adding new features is challenging, or when you want to improve code organization.
- `report-generator` - Use this agent when you need to create automated reports, generate business intelligence summaries, or build recurring data reports. Call this agent when creating executive reports, automated analytics summaries, or data-driven presentations.
- `security-auditor` - Use this agent when you need to audit code for security vulnerabilities, implement security best practices, or review security-sensitive features. Call this agent when handling user data, authentication, payments, or any security-critical functionality.
- `seo-optimizer` - Use this agent when you need to optimize content for search engines, improve SEO rankings, or research keywords. Call this agent when creating content, optimizing existing pages, or developing SEO strategies.
- `social-media-creator` - Use this agent when you need to create social media content, plan posting strategies, or engage with online communities. Call this agent when building social presence, creating content calendars, or developing platform-specific content.
- `solution-architect` - Use this agent when you need to research and design comprehensive solutions for complex technical challenges. Call this agent when facing architecture problems, integration challenges, or when you need end-to-end solution design.
- `sql-expert` - Use this agent when you need to write complex SQL queries, optimize database performance, or solve data analysis problems. Call this agent when working with databases, creating reports, or troubleshooting query performance issues.
- `support-responder` - Use this agent when you need to create customer support responses, help desk communications, or customer service templates. Call this agent when responding to customer issues, creating support documentation, or building customer service workflows.
- `system-designer` - Use this agent when you need to design system architecture, plan technical infrastructure, or create end-to-end solutions for complex challenges. Call this agent when starting new projects, scaling existing systems, or facing complex architectural and integration problems.
- `team-communicator` - Use this agent when you need to create internal team communications, status updates, or organizational announcements. Call this agent when writing team updates, project communications, or internal company messaging.
- `tech-stack-advisor` - Use this agent when you need to choose technologies, evaluate frameworks, or make architectural technology decisions. Call this agent when starting new projects, considering technology migrations, or evaluating technical options.
- `technical-writer` - Use this agent when you need to create any form of technical documentation, including user guides, API references, README files, or architectural documents. Call this agent when documenting systems, creating user manuals, writing technical tutorials, or generating API documentation.
- `technology-researcher` - Use this agent when you need to research new technologies, evaluate emerging tools, or analyze technology trends. Call this agent when exploring new tech stacks, researching solutions, or staying current with technology developments.
- `terms-writer` - Use this agent when you need to create terms of service, user agreements, or legal documents for your application. Call this agent when launching products, updating user terms, or addressing legal compliance requirements.
- `test-strategist` - Use this agent when you need to plan testing strategies, write test cases, or improve test coverage. Call this agent when implementing new features, refactoring code, or when you want to ensure comprehensive testing coverage.
- `trend-analyzer` - Use this agent when you need to analyze industry trends, predict technology directions, or understand market evolution patterns. Call this agent when planning long-term strategy, analyzing market shifts, or understanding industry developments.
- `typography-expert` - Use this agent when you need to choose fonts, create typography systems, or optimize text readability and hierarchy. Call this agent when establishing typographic scales, improving content readability, or creating consistent text styling.
- `ui-designer` - Use this agent when you need to design user interfaces, create UI components, or improve visual design. Call this agent when building new features, redesigning existing interfaces, or creating design systems and component libraries.
- `user-story-writer` - Use this agent when you need to write user stories, acceptance criteria, or translate business requirements into development tasks. Call this agent when planning features, breaking down epics, or creating backlog items for development teams.
- `ux-reviewer` - Use this agent when you need to review user experience designs, analyze user interfaces, or improve usability. Call this agent when evaluating mockups, analyzing user flows, or identifying UX issues in existing interfaces.
- `wireframe-creator` - Use this agent when you need to create wireframes, plan user flows, or design low-fidelity prototypes. Call this agent when planning new features, mapping user journeys, or organizing content structure before visual design.