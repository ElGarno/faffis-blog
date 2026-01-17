# Faffis Blog

A personal tech blog built with [Hugo](https://gohugo.io/) and the [PaperMod](https://github.com/adityatelange/hugo-PaperMod) theme.

**Live site:** [https://faffi.cloud/](https://faffi.cloud/)

## About

This blog covers technical topics including:

- AI/ML projects and tutorials
- Cloud deployment and DevOps
- Docker and containerization
- Home automation
- Data science workflows

## Tech Stack

- **Framework:** Hugo (static site generator)
- **Theme:** PaperMod
- **Content:** Markdown
- **Configuration:** TOML

## Getting Started

### Prerequisites

- [Hugo](https://gohugo.io/installation/) v0.146.0+ (extended version recommended)

### Development

Run the local development server:

```bash
hugo server
```

The site will be available at `http://localhost:1313/`.

### Build

Generate the static site:

```bash
hugo
```

For production with minification:

```bash
hugo --minify
```

Output is generated in the `public/` directory.

## Deployment (Cloudflare Pages)

Set the following environment variable in your Cloudflare Pages project:

| Variable | Value |
|----------|-------|
| `HUGO_VERSION` | `0.146.0` |

## Project Structure

```
.
├── archetypes/       # Content templates
├── assets/css/       # Custom CSS styles
├── content/          # Blog posts and pages (Markdown)
├── static/images/    # Static assets and images
├── themes/           # Hugo themes (PaperMod)
└── hugo.toml         # Site configuration
```

## License

All rights reserved. Content and code in this repository are the property of the author.

## Author

**Fabian Wörenkämper**
Data Scientist
