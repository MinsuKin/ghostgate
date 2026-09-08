"""
RawHuman Engine: Interactive CLI Visualizer & Pitch Demonstration.
Simulates and visualizes live detection of Autonomous AI Agents vs Biological Humans.
"""

from __future__ import annotations
import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rawhuman_engine.biomechanics import (
    BiomechanicalAnalyzer,
    generate_human_like_trajectory,
    generate_synthetic_bot_trajectory,
)
from rawhuman_engine.detector import SyntheticEventDetector

console = Console()


def render_banner():
    banner = Text()
    banner.append("   ██████╗  █████╗ ██╗    ██╗██╗  ██╗██╗   ██╗███╗   ███╗ █████╗ ███╗   ██╗\n", style="bold cyan")
    banner.append("   ██╔══██╗██╔══██╗██║    ██║██║  ██║██║   ██║████╗ ████║██╔══██╗████╗  ██║\n", style="bold cyan")
    banner.append("   ██████╔╝███████║██║ █╗ ██║███████║██║   ██║██╔████╔██║███████║██╔██╗ ██║\n", style="bold cyan")
    banner.append("   ██╔══██╗██╔══██║██║███╗██║██╔══██║██║   ██║██║╚██╔╝██║██╔══██║██║╚██╗██║\n", style="bold cyan")
    banner.append("   ██║  ██║██║  ██║╚███╔███╔╝██║  ██║╚██████╔╝██║ ╚═╝ ██║██║  ██║██║ ╚████║\n", style="bold cyan")
    banner.append("   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝\n", style="bold cyan")
    banner.append("       Kernel & I/O-Level Proof-of-Human Defense Against Multimodal AI Agents\n", style="bold white")
    banner.append("       Kinematic Trajectory Dynamics & Synthetic Event Interceptor\n", style="dim green")
    console.print(Panel(banner, border_style="cyan"))


def run_simulation_case(scenario_name: str, is_bot: bool):
    console.print(f"\n[bold yellow]>> Initiating Scenario: {scenario_name}...[/bold yellow]")
    time.sleep(0.6)

    start = (120.0, 350.0)
    end = (980.0, 720.0)

    if is_bot:
        points = generate_synthetic_bot_trajectory(start, end, steps=25)
        simulated_flags = 0x01  # Simulated LLMHF_INJECTED
    else:
        points = generate_human_like_trajectory(start, end, steps=25)
        simulated_flags = 0x00  # Hardware HID origin

    analyzer = BiomechanicalAnalyzer(min_samples=8, confidence_threshold=0.60)
    for p in points:
        analyzer.add_point(p.x, p.y, p.timestamp)

    report = analyzer.analyze()
    detector = SyntheticEventDetector()
    os_result = detector.inspect_event_metadata(event_flags=simulated_flags)

    table = Table(title=f"Telemetry Inspection: {scenario_name}", border_style="blue")
    table.add_column("Security Metric Layer", style="cyan", no_wrap=True)
    table.add_column("Observed Value", style="magenta")
    table.add_column("Threshold / Expected", style="white")
    table.add_column("Verdict", style="bold")

    # OS Synthetic Flag
    flag_verdict = "[bold red]BLOCKED (Synthetic API)[/bold red]" if os_result.is_synthetic else "[bold green]PASS (Physical HID)[/bold green]"
    table.add_row("OS Event Origin Hook", os_result.platform_flag or "Standard", "PHYSICAL_HID_INTERRUPT", flag_verdict)

    # Ballistic Fit
    ballistic_verdict = "[bold green]PASS[/bold green]" if report.fitts_law_fit >= 0.4 else "[bold red]FAIL (Unnatural)[/bold red]"
    table.add_row("Fitts's Law Ballistic Fit", f"{report.fitts_law_fit * 100:.1f}%", ">= 40.0%", ballistic_verdict)

    # Curvature Entropy
    entropy_verdict = "[bold green]PASS[/bold green]" if report.curvature_entropy_score >= 0.2 else "[bold red]FAIL (Zero Curvature Entropy)[/bold red]"
    table.add_row("Kinematic Curvature Entropy", f"{report.curvature_entropy_score * 100:.1f}%", ">= 20.0%", entropy_verdict)

    # Timing Jitter
    jitter_verdict = "[bold green]PASS[/bold green]" if report.timing_jitter_entropy >= 0.25 else "[bold red]FAIL (Flat Clock)[/bold red]"
    table.add_row("Hardware Interrupt Drift", f"{report.timing_jitter_entropy * 100:.1f}%", ">= 25.0%", jitter_verdict)

    console.print(table)

    final_pass = report.is_human and not os_result.is_synthetic
    if final_pass:
        console.print(
            Panel(
                f"[bold green]✔ AUTHENTIC HUMAN VERIFIED[/bold green]\n"
                f"Confidence Score : [bold green]{report.human_confidence * 100:.1f}%[/bold green]\n"
                f"Origin           : Biological Hardware HID\n"
                f"Attestation ID   : rawhuman_attest_9f83a8b29f01c4",
                border_style="green",
            )
        )
    else:
        reasons_list = []
        if os_result.is_synthetic:
            reasons_list.append(f"Synthetic OS Event Injected ({os_result.platform_flag})")
        reasons_list.extend(report.rejection_reasons)
        if not reasons_list and not report.is_human:
            reasons_list.append(f"Composite Confidence Score ({report.human_confidence * 100:.1f}%) below 60% threshold")

        reasons_txt = "\n - ".join(reasons_list)
        console.print(
            Panel(
                f"[bold red]✖ AUTONOMOUS AI AGENT DETECTED & TERMINATED[/bold red]\n"
                f"Confidence Score : [bold red]{report.human_confidence * 100:.1f}%[/bold red]\n"
                f"Threat Details   :\n - {reasons_txt}\n"
                f"Action Taken     : I/O Gate Locked; Endpoint Transaction Aborted (0.002s latency)",
                border_style="red",
            )
        )


def main():
    render_banner()
    console.print("[dim]Simulating real-time inputs against RawHuman Kernel & Biomechanics Sentinel...[/dim]")

    # Case 1: Autonomous Agent (e.g. Claude Computer Use or pyautogui bot)
    run_simulation_case("Autonomous AI Agent (Claude 3.7 Computer Use / SendInput)", is_bot=True)

    console.print("\n" + "=" * 70 + "\n")

    # Case 2: Organic Human Operator
    run_simulation_case("Biological Human Operator (Physical USB Mouse)", is_bot=False)


if __name__ == "__main__":
    main()
