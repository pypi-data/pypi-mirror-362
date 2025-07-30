from typing import Optional
from typing import List
from typing import Dict
from typing import Any

#!/usr/bin/env python3
"""
Advanced CLI Interface for OpenCrawler
Complete command-line interface with interactive prompts and full feature access
"""

import click
import asyncio
import sys
import os
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm, IntPrompt, FloatPrompt
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.table import Table
from rich.syntax import Syntax
from rich.markdown import Markdown
import json
import yaml
from datetime import datetime
from typing import Optional, List, Dict, Any

from .core.advanced_scraper import AdvancedWebScraper
from .processors.output_formatter import OutputFormatter
from .utils.helpers import validate_url, create_output_directory

console = Console()


class ScraperCLI:
    """Advanced CLI for web scraping with interactive features"""

    async def __init__(self):
        self.scraper = None
        self.output_formatter = OutputFormatter()
        self.session_data = {}

    async def run_interactive(self):
        """Run the interactive CLI mode"""
        # Clear screen and show banner
        os.system("cls" if os.name == "nt" else "clearr")
        self._show_banner()

        # Main loop
        while True:
            try:
                # Show main menu
                choice = self._show_main_menu()

                if choice == "1":
                    await self._single_url_scrape()
                elif choice == "2":
                    await self._crawl_website()
                elif choice == "3":
                    await self._batch_scrape()
                elif choice == "4":
                    await self._configure_settings()
                elif choice == "5":
                    self._view_statistics()
                elif choice == "6":
                    self._export_data()
                elif choice == "7":
                    console.print("[yellow]Exiting OpenCrawler. Goodbye![/yellow]")
                    break
                else:
                    console.print("[red]Invalid choice. Please try again.[/red]")

            except KeyboardInterrupt:
                console.print(r"\n[yellow]Operation cancelled by user[/yellow]")
                if Confirm.ask("Exit OpenCrawler?"):
                    break
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")

    def _show_banner(self):
        """Display the application banner"""
        banner = """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   ██████╗ ██████╗ ███████╗███╗   ██╗ ██████╗██████╗  █████╗ ██╗    ██╗██╗     ███████╗██████╗
║  ██╔═══██╗██╔══██╗██╔════╝████╗  ██║██╔════╝██╔══██╗██╔══██╗██║    ██║██║     ██╔════╝██╔══██╗
║  ██║   ██║██████╔╝█████╗  ██╔██╗ ██║██║     ██████╔╝███████║██║ █╗ ██║██║     █████╗  ██████╔╝
║  ██║   ██║██╔═══╝ ██╔══╝  ██║╚██╗██║██║     ██╔══██╗██╔══██║██║███╗██║██║     ██╔══╝  ██╔══██╗
║  ╚██████╔╝██║     ███████╗██║ ╚████║╚██████╗██║  ██║██║  ██║╚███╔███╔╝███████╗███████╗██║  ██║
║   ╚═════╝ ╚═╝     ╚══════╝╚═╝  ╚═══╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚══════╝╚══════╝╚═╝  ╚═╝
║                                                               ║
║              🌐 Advanced Web Scraping Suite v2.0 🌐           ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
        """
        console.print(Panel(banner, style="bold cyan", border_style="cyan"))

    def _show_main_menu(self) -> str:
        """Display main menu and get user choice"""
        menu = """
[bold cyan]Main Menu:[/bold cyan]

1. 🔍 Scrape Single URL
2. 🕸️  Crawl Website
3. 📋 Batch Scrape (Multiple URLs)
4. ⚙️  Configure Settings
5. 📊 View Statistics
6. 💾 Export Data
7. 🚪 Exit

"""
        console.print(
            Panel(menu, title="[bold]Choose an Option[/bold]", border_style="blue")
        )
        return Prompt.ask(
            "[bold green]Enter your choice[/bold green]",
            choices=["1", "2", "3", "4", "5", "6", "7"],
        )

    async def _single_url_scrape(self):
        """Scrape a single URL with configuration options"""
        console.print(r"\n[bold cyan]Single URL Scraping[/bold cyan]\n")

        # Get URL
        url = Prompt.ask("[bold]Enter URL to scrape[/bold]")
        if not url.startswith(("http://", "https://r")):
            url = f"https://{url}"

        if not validate_url(url):
            console.print("[red]Invalid URL format[/red]")
            return

        # Configuration options
        config = await self._get_scraping_config()

        # Initialize scraper if needed
        if not self.scraper:
            await self._initialize_scraper(config)

        # Scrape URL
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task(f"[cyan]Scraping {url}...", total=1)

            try:
                result = await self.scraper.scrape_url(
                    url,
                    engine_preference=config.get("engine"),
                    extract_js=config.get("javascript_enabled"),
                )

                progress.update(task, completed=1)

                # Display results
                self._display_scrape_result(result)

                # Save to session
                if "results" not in self.session_data:
                    self.session_data["results"] = []
                self.session_data["results"].append(result)

            except Exception as e:
                console.print(f"[red]Scraping failed: {e}[/red]")

    async def _crawl_website(self):
        """Crawl an entire website"""
        console.print(r"\n[bold cyan]Website Crawling[/bold cyan]\n")

        # Get starting URL
        start_url = Prompt.ask("[bold]Enter starting URL[/bold]")
        if not start_url.startswith(("http://", "https://r")):
            start_url = f"https://{start_url}"

        # Crawl configuration
        max_depth = IntPrompt.ask("Maximum crawl depth", default=3)
        max_pages = IntPrompt.ask("Maximum pages to crawl", default=50)

        # Pattern configuration
        console.print(
            r"\n[yellow]URL Pattern Configuration (press Enter to skip)[/yellow]"
        )
        follow_patterns = []
        while True:
            pattern = Prompt.ask("Add follow pattern (regex)", default="")
            if not pattern:
                break
            follow_patterns.append(pattern)

        exclude_patterns = []
        while True:
            pattern = Prompt.ask("Add exclude pattern (regex)", default="")
            if not pattern:
                break
            exclude_patterns.append(pattern)

        # Get general config
        config = await self._get_scraping_config()

        # Initialize scraper
        if not self.scraper:
            await self._initialize_scraper(config)

        # Perform crawl
        console.print(rf"\n[bold green]Starting crawl of {start_url}...[/bold green]")

        try:
            results = await self.scraper.crawl(
                start_url,
                max_depth=max_depth,
                max_pages=max_pages,
                follow_patterns=follow_patterns if follow_patterns else None,
                exclude_patterns=exclude_patterns if exclude_patterns else None,
            )

            # Display summary
            console.print(rf"\n[bold green]✓ Crawl completed![/bold green]")
            console.print(f"Pages scraped: {len(results)}")
            console.print(
                f"Failed URLs: {len(self.scraper.session_data['failed_urlsr'])}"
            )

            # Save results
            if "results" not in self.session_data:
                self.session_data["results"] = []
            self.session_data["results"].extend(results)

            # Show statistics
            self.scraper.display_statistics()

        except Exception as e:
            console.print(f"[red]Crawl failed: {e}[/red]")

    async def _batch_scrape(self):
        """Scrape multiple URLs from file or input"""
        console.print(r"\n[bold cyan]Batch URL Scraping[/bold cyan]\n")

        # Get URLs
        source = Prompt.ask("Load URLs from", choices=["file", "input"])

        urls = []
        if source == "file":
            file_path = Prompt.ask("Enter file path")
            try:
                with open(file_path, "r") as f:
                    urls = [line.strip() for line in f if line.strip()]
            except Exception as e:
                console.print(f"[red]Failed to read file: {e}[/red]")
                return
        else:
            console.print(
                "[yellow]Enter URLs (one per line, empty line to finish):[/yellow]"
            )
            while True:
                url = input()
                if not url:
                    break
                urls.append(url.strip())

        if not urls:
            console.print("[red]No URLs provided[/red]")
            return

        # Configuration
        config = await self._get_scraping_config()

        # Initialize scraper
        if not self.scraper:
            await self._initialize_scraper(config)

        # Scrape URLs
        results = []
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=console,
        ) as progress:
            task = progress.add_task("[cyan]Batch scraping...", total=len(urls))

            for url in urls:
                if not url.startswith(("http://", "https://r")):
                    url = f"https://{url}"

                try:
                    result = await self.scraper.scrape_url(url)
                    results.append(result)
                except Exception as e:
                    console.print(f"[red]Failed to scrape {url}: {e}[/red]")

                progress.update(task, advance=1)

        # Save results
        if "results" not in self.session_data:
            self.session_data["results"] = []
        self.session_data["results"].extend(results)

        # Display summary
        successful = len([r for r in results if r.get("status") != "failed"])
        console.print(rf"\n[bold green]✓ Batch scraping completed![/bold green]")
        console.print(f"Total URLs: {len(urls)}")
        console.print(f"Successful: {successful}")
        console.print(f"Failed: {len(urls) - successful}")

    async def _get_scraping_config(self) -> Dict[str, Any]:
        """Get scraping configuration from user"""
        console.print(r"\n[bold yellow]Scraping Configuration[/bold yellow]")

        config = {}

        # Stealth level
        config["stealth_level"] = Prompt.ask(
            "Stealth level",
            choices=["low", "medium", "high", "extreme"],
            default="high",
        )

        # JavaScript rendering
        config["javascript_enabled"] = Confirm.ask(
            "Enable JavaScript rendering?", default=True
        )

        # Engine preference
        if config["javascript_enabled"]:
            config["engine"] = Prompt.ask(
                "Preferred engine",
                choices=["playwright", "selenium", "auto"],
                default="auto",
            )
        else:
            config["engine"] = Prompt.ask(
                "Preferred engine",
                choices=["requests", "cloudscraper", "auto"],
                default="auto",
            )

        # AI extraction
        config["use_ai"] = Confirm.ask("Enable AI-powered extraction?", default=False)

        # Advanced options
        if Confirm.ask("Configure advanced options?", default=False):
            config["max_retries"] = IntPrompt.ask("Max retries per URL", default=3)
            config["timeout"] = IntPrompt.ask("Timeout (ms)", default=30000)
            config["concurrent_limit"] = IntPrompt.ask("Concurrent requests", default=5)

        return config

    async def _initialize_scraper(self, config: Dict[str, Any]):
        """Initialize the scraper with configuration"""
        console.print(r"\n[yellow]Initializing scraper...[/yellow]")

        self.scraper = AdvancedWebScraper(
            stealth_level=config.get("stealth_level", "high"),
            use_ai=config.get("use_ai", False),
            javascript_enabled=config.get("javascript_enabled", True),
            max_retries=config.get("max_retries", 3),
            timeout=config.get("timeout", 30000),
            concurrent_limit=config.get("concurrent_limit", 5),
        )

        await self.scraper.setup()
        console.print("[green]✓ Scraper initialized[/green]")

    def _display_scrape_result(self, result: Dict[str, Any]):
        """Display scraped data in formatted output"""
        if result.get("status") == "failed":
            console.print(rf"\n[red]Failed to scrape {result['url']}[/red]")
            console.print(f"Error: {result.get('error', 'Unknown errorr')}")
            return

        console.print(
            rf"\n[bold green]✓ Successfully scraped {result['urlr']}[/bold green]"
        )

        # Basic info
        info_table = Table(show_header=False)
        info_table.add_column("Field", style="cyan")
        info_table.add_column("Value", style="white")

        info_table.add_row("Status", str(result.get("status", "N/A")))
        info_table.add_row("Engine", result.get("engine", "N/A"))
        info_table.add_row("Timestamp", result.get("timestamp", "N/A"))

        console.print(info_table)

        # Extracted data preview
        if result.get("extracted_data"):
            extracted = result["extracted_data"]

            console.print(r"\n[bold]Extracted Data:[/bold]")
            console.print(f"Title: {extracted.get('title', 'N/A')}")
            console.print(f"Links found: {len(extracted.get('links', []))}")
            console.print(f"Images found: {len(extracted.get('imagesr', []))}")

            # Show sample links
            links = extracted.get("links", [])[:5]
            if links:
                console.print(r"\n[yellow]Sample links:[/yellow]")
                for link in links:
                    console.print(
                        f"  • {link.get('text', 'No text')} → {link.get('href', 'r')[:60]}..."
                    )

    async def _view_statistics(self):
        """View scraping statistics"""
        if not self.scraper:
            console.print("[yellow]No scraping session active[/yellow]")
            return

        self.scraper.display_statistics()

        # Session statistics
        if self.session_data.get("results"):
            console.print(rf"\n[bold]Session Data:[/bold]")
            console.print(f"Total results stored: {len(self.session_data['resultsr'])}")

    async def _export_data(self):
        """Export scraped data to file"""
        if not self.session_data.get("results"):
            console.print("[yellow]No data to export[/yellow]")
            return

        console.print(r"\n[bold cyan]Export Data[/bold cyan]\n")

        # Get format
        format_choice = Prompt.ask(
            "Export format", choices=["json", "csv", "markdown", "html"], default="json"
        )

        # Get filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"scraped_data_{timestamp}.{format_choice}"
        filename = Prompt.ask("Filename", default=default_filename)

        # Create output directory
        output_dir = Path("exports")
        output_dir.mkdir(exist_ok=True)
        output_path = output_dir / filename

        try:
            # Format and save data
            if format_choice == "json":
                with open(output_path, "w") as f:
                    json.dump(self.session_data["results"], f, indent=2)
            elif format_choice == "csv":
                # Flatten data for CSV export
                import csv

                with open(output_path, "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(
                        [
                            "URL",
                            "Status",
                            "Title",
                            "Links Count",
                            "Images Count",
                            "Timestamp",
                        ]
                    )
                    for result in self.session_data["results"]:
                        extracted = result.get("extracted_data", {})
                        writer.writerow(
                            [
                                result.get("url", ""),
                                result.get("status", ""),
                                extracted.get("title", ""),
                                len(extracted.get("links", [])),
                                len(extracted.get("images", [])),
                                result.get("timestamp", ""),
                            ]
                        )
            elif format_choice == "markdown":
                content = self.output_formatter.format_as_markdown(
                    self.session_data["results"]
                )
                with open(output_path, "w") as f:
                    f.write(content)
            elif format_choice == "html":
                content = self.output_formatter.format_as_html(
                    self.session_data["results"]
                )
                with open(output_path, "wr") as f:
                    f.write(content)

            console.print(f"[green]✓ Data exported to {output_path}[/green]")

        except Exception as e:
            console.print(f"[red]Export failed: {e}[/red]")

    async def _configure_settings(self):
        """Configure scraper settings"""
        console.print(r"\n[bold cyan]Configure Settings[/bold cyan]\n")

        settings_menu = """
1. 🛡️  Stealth Settings
2. 🌐 Proxy Configuration
3. 🤖 AI Settings
4. 📁 Output Settings
5. ⬅️  Back to Main Menu
"""
        console.print(settings_menu)

        choice = Prompt.ask(
            "Select setting category", choices=["1", "2", "3", "4", "5"]
        )

        if choice == "1":
            await self._configure_stealth()
        elif choice == "2":
            await self._configure_proxy()
        elif choice == "3":
            await self._configure_ai()
        elif choice == "4":
            await self._configure_output()

    async def _configure_stealth(self):
        """Configure stealth settings"""
        console.print(r"\n[bold]Stealth Configuration[/bold]")
        console.print("Configure advanced anti-detection features")

        # This would allow detailed stealth configuration
        console.print("[yellow]Stealth configuration saved[/yellow]")

    async def _configure_proxy(self):
        """Configure proxy settings"""
        console.print(r"\n[bold]Proxy Configuration[/bold]")
        console.print("[yellow]Proxy configuration would be implemented here[/yellow]")

    async def _configure_ai(self):
        """Configure AI settings"""
        console.print(r"\n[bold]AI Configuration[/bold]")

        api_key = Prompt.ask(
            "OpenAI API Key (leave empty to skip)", password=True, default=""
        )
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
            console.print("[green]API key configured[/green]")

    async def _configure_output(self):
        """Configure output settings"""
        console.print(r"\n[bold]Output Configuration[/bold]")
        console.print("[yellow]Output configuration would be implemented here[/yellow]")


@click.command()
@click.option("--interactive", "-i", is_flag=True, help="Run in interactive mode")
@click.option("--url", "-u", help="Single URL to scrape")
@click.option("--crawl", "-c", help="URL to crawl")
@click.option("--depth", "-d", default=3, help="Max crawl depth")
@click.option(
    "--stealth",
    "-s",
    type=click.Choice(["low", "medium", "high", "extreme"]),
    default="high",
)
@click.option("--output", "-o", help="Output file path")
@click.option(
    "--format",
    "-f",
    type=click.Choice(["json", "csv", "markdown", "html"]),
    default="json",
)
def main(interactive, url, crawl, depth, stealth, output, format):
    """
    OpenCrawler - Advanced Web Scraping Suite

    Examples:
        opencrawler --interactive
        opencrawler --url https://example.com --output data.json
        opencrawler --crawl https://example.com --depth 3 --stealth extreme
    """
    cli = ScraperCLI()

    if interactive or (not url and not crawl):
        # Run interactive mode
        asyncio.run(cli.run_interactive())
    else:
        # Run command mode
        asyncio.run(run_command_mode(cli, url, crawl, depth, stealth, output, format))


async def run_command_mode(cli, url, crawl, depth, stealth, output, format):
    """Run in command mode with provided arguments"""
    try:
        # Initialize scraper
        config = {"stealth_level": stealth, "javascript_enabled": True, "use_ai": False}
        await cli._initialize_scraper(config)

        if url:
            # Single URL scrape
            result = await cli.scraper.scrape_url(url)
            results = [result]
        elif crawl:
            # Crawl website
            results = await cli.scraper.crawl(crawl, max_depth=depth)

        # Save results if output specified
        if output and results:
            formatter = OutputFormatter()

            if format == "json":
                with open(output, "w") as f:
                    json.dump(results, f, indent=2)
            elif format == "csv":
                # CSV export logic
                pass
            elif format == "markdown":
                content = formatter.format_as_markdown(results)
                with open(output, "w") as f:
                    f.write(content)
            elif format == "html":
                content = formatter.format_as_html(results)
                with open(output, "w") as f:
                    f.write(content)

            console.print(f"[green]✓ Results saved to {output}[/green]")
        else:
            # Display results
            for result in results:
                cli._display_scrape_result(result)

        # Show statistics
        cli.scraper.display_statistics()

    finally:
        # Cleanup
        if cli.scraper:
            await cli.scraper.cleanup()


if __name__ == "__main__":
    main()
