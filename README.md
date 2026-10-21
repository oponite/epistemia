# Epistemia

An independent research archive for academic papers, technical reports, and exploratory research notes. Built with [Quarto](https://quarto.org/) and its default Lux theme.

## Repository structure

```text
epistemia/
├── .github/workflows/deploy.yml
├── papers/index.qmd
├── papers/np-complete.md
├── _quarto.yml
├── .gitignore
├── README.md
├── TODO.md
└── index.qmd
```

## Add a research paper

1. Create a `.md` or `.qmd` file in `papers/` with a unique filename, such as `information-models.md`. Subdirectories are supported. Reserve `papers/index.qmd` for the publication listing.
2. Add the following required YAML front matter, then write the paper in Markdown:

   ```yaml
   ---
   title: "Paper Title"
   author: "Author Name"
   date: "2026-10-21"
   description: "Brief abstract or paper description."
   ---
   ```

3. Run `quarto render` to check the result. Papers render directly to HTML and appear automatically in the Papers listing, newest first. No conversion or navigation edits are needed.

Use relative paths for links and assets, and keep paper assets alongside the paper. Quarto resolves links to `.md` and `.qmd` project pages to their HTML output. Tables of contents are enabled for papers.

## Local use

Install [Quarto](https://quarto.org/docs/get-started/), then run these commands from this directory:

```sh
quarto preview
```

Generate the static site in `_site/`:

```sh
quarto render
```

Generated output and Quarto caches are ignored by Git.

## GitHub Pages

The local source is prepared on `main`. Run the following from this directory when ready to publish publicly.

1. Create the GitHub repository and push the committed source:

   ```sh
   gh repo create oponite/epistemia --public --source=. --remote=origin --push
   ```

2. Enable GitHub Pages with GitHub Actions as its build source:

   ```sh
   gh api --method POST repos/oponite/epistemia/pages -f build_type=workflow
   ```

   The equivalent setting is **Repository Settings → Pages → Build and deployment → Source: GitHub Actions**.

3. Start the first deployment after Pages is enabled:

   ```sh
   gh workflow run deploy.yml --repo oponite/epistemia --ref main
   ```

4. Check deployment status:

   ```sh
   gh run list --repo oponite/epistemia --workflow deploy.yml --limit 5
   ```

Later pushes to `main` deploy automatically. An initial run triggered before Pages is enabled may fail; the explicit run in step 3 performs the first configured deployment.

The workflow renders and deploys to <https://oponite.github.io/epistemia/> using the native GitHub Pages artifact deployment. No `gh-pages` branch or committed HTML is needed.

The first article will be available at <https://oponite.github.io/epistemia/papers/np-complete.html>.
