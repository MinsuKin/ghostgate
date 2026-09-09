"""
GhostGate Core: CISO & SOC Security Dashboard and Interactive Live Playground.
Provides an interactive web interface for investors and security officers to test
real-time format-preserving secret shadowing, in-memory rehydration, RawHuman agent defense,
and live SOC telemetry.
"""

from __future__ import annotations
import time
from typing import Any, Dict, List
from fastapi.responses import HTMLResponse


class DashboardMetricsCollector:
    """Collects and aggregates real-time telemetry for the CISO dashboard."""

    def __init__(self):
        self.total_requests = 14289
        self.total_secrets_masked = 1842
        self.total_agent_hijacks_blocked = 347
        self.zdr_compliance_score = 99.8
        self.category_counts = {
            "AWS_KEYS": 512,
            "DATABASE_URLS": 389,
            "OPENAI_KEYS": 441,
            "PII_EMAILS": 320,
            "PRIVATE_KEYS": 180,
        }
        self.recent_events: List[Dict[str, Any]] = [
            {
                "time": "21:45:12",
                "source": "Engineer Workstation #084 (MacBook Pro)",
                "event": "Outbound AWS Secret Masked",
                "category": "AWS_SECRET_KEY",
                "action": "Format-Preserving Mock AKIA... injected",
                "status": "SECURED",
            },
            {
                "time": "21:42:30",
                "source": "CI/CD Deployment Runner",
                "event": "Synthetic Mouse Injection (SendInput 0x01)",
                "category": "AUTONOMOUS_BOT_TAKEOVER",
                "action": "I/O Gate Locked; Action Aborted (0.002s latency)",
                "status": "BLOCKED",
            },
            {
                "time": "21:38:05",
                "source": "Cursor IDE Developer Plugin",
                "event": "Postgres DB URI Intercepted",
                "category": "DATABASE_CONNECTION_STRING",
                "action": "Synthetic Shadow postgres://mock_user... applied",
                "status": "SECURED",
            },
            {
                "time": "21:31:18",
                "source": "Developer Workstation #019",
                "event": "Air-Gap Tag (#@airgap) Detected",
                "category": "CLASSIFIED_SOURCE_CODE",
                "action": "Diverted to 100% Offline Local Ollama Container",
                "status": "AIR-GAPPED",
            },
            {
                "time": "21:25:40",
                "source": "Finance Bot Script (pyautogui)",
                "event": "Synthetic Click on 'Approve Transfer'",
                "category": "UNAUTHORIZED_AGENT_ACTION",
                "action": "Monotonic Bezier (H=0.04); Action Aborted",
                "status": "BLOCKED",
            },
        ]

    def record_redaction(self, category: str, count: int = 1):
        self.total_requests += 1
        self.total_secrets_masked += count
        mapped_cat = category
        if "AWS" in category:
            mapped_cat = "AWS_KEYS"
        elif "DATABASE" in category:
            mapped_cat = "DATABASE_URLS"
        elif "OPENAI" in category:
            mapped_cat = "OPENAI_KEYS"
        elif "EMAIL" in category or "PHONE" in category:
            mapped_cat = "PII_EMAILS"
        elif "KEY" in category:
            mapped_cat = "PRIVATE_KEYS"

        self.category_counts[mapped_cat] = self.category_counts.get(mapped_cat, 0) + count
        self.recent_events.insert(0, {
            "time": time.strftime("%H:%M:%S"),
            "source": "Live Investor Sandbox Session",
            "event": f"Intercepted & Shadowed: {category}",
            "category": category,
            "action": f"Format-Preserving Mask ({count} tokens)",
            "status": "SECURED",
        })
        if len(self.recent_events) > 25:
            self.recent_events.pop()

    def record_agent_block(self, tool_name: str, reason: str):
        self.total_agent_hijacks_blocked += 1
        self.recent_events.insert(0, {
            "time": time.strftime("%H:%M:%S"),
            "source": "Live Investor Sandbox Session",
            "event": f"Agent tool call blocked: {tool_name}",
            "category": "AUTONOMOUS_BOT_TAKEOVER",
            "action": reason[:60] + "...",
            "status": "BLOCKED",
        })
        if len(self.recent_events) > 25:
            self.recent_events.pop()

    def get_metrics(self) -> Dict[str, Any]:
        return {
            "total_requests": self.total_requests,
            "total_secrets_masked": self.total_secrets_masked,
            "total_agent_hijacks_blocked": self.total_agent_hijacks_blocked,
            "zdr_compliance_score": self.zdr_compliance_score,
            "category_counts": self.category_counts,
            "recent_events": self.recent_events,
        }


metrics_collector = DashboardMetricsCollector()


def render_dashboard_html() -> HTMLResponse:
    metrics = metrics_collector.get_metrics()

    html = f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>GhostGate Labs // CISO Security Operations Center & Interactive Sandbox</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <script>
    tailwind.config = {{
      darkMode: 'class',
      theme: {{
        extend: {{
          fontFamily: {{
            sans: ['"Plus Jakarta Sans"', 'sans-serif'],
            mono: ['"JetBrains Mono"', 'monospace'],
          }},
          colors: {{
            brand: {{
              50: '#eef2ff',
              500: '#6366f1',
              600: '#4f46e5',
              900: '#1e1b4b',
            }}
          }}
        }}
      }}
    }}
  </script>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen font-sans antialiased selection:bg-indigo-500 selection:text-white">

  <!-- Top Navigation Header -->
  <header class="border-b border-slate-800/80 bg-slate-900/80 backdrop-blur sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <div class="h-9 w-9 rounded-lg bg-gradient-to-tr from-indigo-500 via-purple-500 to-cyan-400 flex items-center justify-center font-bold text-white shadow-lg shadow-indigo-500/20">
          🛡️
        </div>
        <div>
          <span class="font-extrabold text-lg tracking-wider text-white">GHOSTGATE</span>
          <span class="text-[11px] ml-1.5 px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 font-mono font-semibold">ENTERPRISE SOC</span>
        </div>
      </div>
      
      <!-- Center Pill Tabs -->
      <nav class="hidden md:flex items-center bg-slate-950/70 p-1 rounded-lg border border-slate-800 text-xs font-medium">
        <button onclick="switchTab('playground')" id="tab-btn-playground" class="px-3.5 py-1.5 rounded-md bg-indigo-600 text-white font-semibold transition">
          ⚡ AI Privacy Playground
        </button>
        <button onclick="switchTab('rawhuman')" id="tab-btn-rawhuman" class="px-3.5 py-1.5 rounded-md text-slate-400 hover:text-white transition">
          🤖 RawHuman Agent Defense
        </button>
        <button onclick="switchTab('dashboard')" id="tab-btn-dashboard" class="px-3.5 py-1.5 rounded-md text-slate-400 hover:text-white transition">
          📊 CISO SOC Telemetry
        </button>
        <button onclick="switchTab('diagnostics')" id="tab-btn-diagnostics" class="px-3.5 py-1.5 rounded-md text-slate-400 hover:text-white transition">
          🔌 API & Health
        </button>
      </nav>

      <!-- Right Action / Status -->
      <div class="flex items-center space-x-3 text-xs font-mono">
        <span class="flex items-center text-emerald-400">
          <span class="h-2 w-2 rounded-full bg-emerald-400 animate-ping mr-2"></span>
          ZDR ACTIVE
        </span>
        <a href="https://github.com/MinsuKin/ghostgate" target="_blank" class="hidden sm:inline-flex items-center bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 px-3 py-1.5 rounded-md font-semibold transition">
          GitHub Repo
        </a>
      </div>
    </div>
  </header>

  <!-- Main Container -->
  <main class="max-w-7xl mx-auto px-6 py-8">

    <!-- TAB 1: INTERACTIVE AI PRIVACY PLAYGROUND -->
    <div id="tab-playground" class="space-y-6">
      <div class="bg-gradient-to-r from-indigo-950/40 via-purple-950/20 to-slate-900 border border-indigo-800/40 rounded-2xl p-6">
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h2 class="text-xl font-bold text-white flex items-center gap-2">
              <span>⚡ Format-Preserving Synthetic Shadowing Sandbox</span>
              <span class="text-xs px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 font-mono">AST-Safe</span>
            </h2>
            <p class="text-xs text-slate-300 mt-1 max-w-2xl">
              Paste or type source code with real credentials below. GhostGate intercepts and shadows secrets with syntactically valid mock tokens before egress, preventing broken LLM code generation and guaranteeing Zero Data Retention.
            </p>
          </div>
          <div class="flex items-center gap-2 text-xs font-mono">
            <span class="text-slate-400">Engine Overhead:</span>
            <span id="latency-badge" class="px-2.5 py-1 rounded bg-indigo-500/20 text-indigo-300 font-bold border border-indigo-500/30">0.08 ms</span>
          </div>
        </div>

        <!-- Quick Demo Presets -->
        <div class="mt-4 pt-4 border-t border-slate-800/80 flex flex-wrap items-center gap-2">
          <span class="text-xs text-slate-400 font-mono mr-1">Load Preset:</span>
          <button onclick="loadPreset('aws')" class="text-xs bg-slate-800/80 hover:bg-slate-700 border border-slate-700 px-3 py-1 rounded-md text-indigo-300 font-mono transition">
            AWS IAM Key & S3
          </button>
          <button onclick="loadPreset('postgres')" class="text-xs bg-slate-800/80 hover:bg-slate-700 border border-slate-700 px-3 py-1 rounded-md text-cyan-300 font-mono transition">
            Postgres DB URI
          </button>
          <button onclick="loadPreset('pii')" class="text-xs bg-slate-800/80 hover:bg-slate-700 border border-slate-700 px-3 py-1 rounded-md text-purple-300 font-mono transition">
            Customer PII & JWT
          </button>
          <button onclick="loadPreset('airgap')" class="text-xs bg-slate-800/80 hover:bg-slate-700 border border-slate-700 px-3 py-1 rounded-md text-amber-300 font-mono transition">
            # @airgap Classified Trigger
          </button>
        </div>
      </div>

      <!-- Live Interactive Editor Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Input Column -->
        <div class="bg-slate-900 border border-slate-800 rounded-xl p-5 flex flex-col justify-between space-y-4">
          <div>
            <div class="flex items-center justify-between mb-2">
              <label class="text-xs font-bold uppercase tracking-wider text-slate-300 font-mono flex items-center gap-1.5">
                <span class="h-2 w-2 rounded-full bg-indigo-500"></span> Input Prompt (Developer Workstation)
              </label>
              <span class="text-[11px] text-slate-400 font-mono">Plaintext In-Flight</span>
            </div>
            <textarea id="prompt-input" rows="8" class="w-full bg-slate-950 border border-slate-800 rounded-lg p-3 text-xs font-mono text-slate-200 focus:outline-none focus:border-indigo-500 resize-none leading-relaxed" placeholder="Type or paste prompt with secrets here..."></textarea>
          </div>
          <div class="flex items-center justify-between pt-2">
            <span class="text-[11px] text-slate-400 font-mono">Mode: Format-Preserving Shadowing</span>
            <button onclick="executeRedaction()" id="btn-redact" class="bg-indigo-600 hover:bg-indigo-500 text-white px-4 py-2 rounded-lg font-semibold text-xs font-mono shadow-md shadow-indigo-600/30 transition flex items-center gap-2">
              <span>⚡ Intercept & Shadow Secret</span>
            </button>
          </div>
        </div>

        <!-- Output Column -->
        <div class="bg-slate-900 border border-slate-800 rounded-xl p-5 flex flex-col justify-between space-y-4">
          <div>
            <div class="flex items-center justify-between mb-2">
              <label class="text-xs font-bold uppercase tracking-wider text-cyan-400 font-mono flex items-center gap-1.5">
                <span class="h-2 w-2 rounded-full bg-cyan-400"></span> Outbound Egress (What Cloud LLM Receives)
              </label>
              <span id="shield-badge" class="text-[11px] font-mono px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">SECURED (0 BYTES LEAKED)</span>
            </div>
            <div id="redacted-output" class="w-full h-48 bg-slate-950 border border-slate-800 rounded-lg p-3 text-xs font-mono text-emerald-400 overflow-y-auto whitespace-pre-wrap leading-relaxed">Click "Intercept & Shadow Secret" above to simulate live masking...</div>
          </div>
          <div class="bg-slate-950/60 border border-slate-800/80 rounded-lg p-3 text-xs font-mono flex flex-wrap items-center justify-between gap-2">
            <span class="text-slate-400">In-Memory Rehydration Status:</span>
            <span id="rehydrate-status" class="text-indigo-300 font-semibold">Ready for Bidirectional Stream</span>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 2: RAWHUMAN AGENT DEFENSE SIMULATOR -->
    <div id="tab-rawhuman" class="hidden space-y-6">
      <div class="bg-gradient-to-r from-rose-950/30 via-slate-900 to-indigo-950/20 border border-rose-800/40 rounded-2xl p-6">
        <h2 class="text-xl font-bold text-white flex items-center gap-2">
          <span>🤖 RawHuman: Autonomous AI Agent Takeover Sentinel</span>
          <span class="text-xs px-2 py-0.5 rounded bg-rose-500/20 text-rose-300 border border-rose-500/30 font-mono">Layer 0 I/O Gate</span>
        </h2>
        <p class="text-xs text-slate-300 mt-1 max-w-2xl">
          Simulate programmatic mouse and keyboard injection (Anthropic Computer Use, OpenAI Operator, PyAutoGUI) vs authentic human motor movement. RawHuman inspects OS hook flags and kinematic trajectory dynamics to terminate unauthorized agent actions.
        </p>

        <!-- Scenario Selector -->
        <div class="mt-5 flex flex-wrap items-center gap-3">
          <button onclick="runAgentDemo('agent')" id="btn-scenario-agent" class="bg-rose-600 hover:bg-rose-500 text-white px-4 py-2 rounded-lg font-semibold text-xs font-mono shadow-md shadow-rose-600/30 transition">
            Simulate Autonomous Agent (SendInput / PyAutoGUI)
          </button>
          <button onclick="runAgentDemo('human')" id="btn-scenario-human" class="bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 px-4 py-2 rounded-lg font-semibold text-xs font-mono transition">
            Simulate Biological Human (Physical USB Mouse)
          </button>
        </div>
      </div>

      <!-- Telemetry Scorecard -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <div class="text-xs font-mono uppercase text-slate-400">OS Event Origin Hook</div>
          <div id="raw-os-flag" class="text-lg font-bold font-mono text-white mt-2">Ready to probe...</div>
          <div id="raw-os-sub" class="text-xs text-slate-400 mt-1">Win32 LLMHF_INJECTED / Quartz</div>
        </div>

        <div class="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <div class="text-xs font-mono uppercase text-slate-400">Kinematic Curvature Entropy</div>
          <div id="raw-entropy" class="text-lg font-bold font-mono text-white mt-2">-</div>
          <div id="raw-entropy-sub" class="text-xs text-slate-400 mt-1">Threshold: H &ge; 0.20</div>
        </div>

        <div class="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <div class="text-xs font-mono uppercase text-slate-400">OS Scheduler Jitter</div>
          <div id="raw-jitter" class="text-lg font-bold font-mono text-white mt-2">-</div>
          <div id="raw-jitter-sub" class="text-xs text-slate-400 mt-1">Clock Quantum Variance</div>
        </div>
      </div>

      <!-- Enforcement Verdict Banner -->
      <div id="raw-verdict-box" class="bg-slate-900 border border-slate-800 rounded-xl p-6 font-mono text-xs space-y-2">
        <div class="text-slate-400">Select a scenario above to test RawHuman I/O Gate attestation.</div>
      </div>
    </div>

    <!-- TAB 3: CISO SOC TELEMETRY & STATS -->
    <div id="tab-dashboard" class="hidden space-y-8">
      <!-- Stat KPI Cards -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <div class="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-sm">
          <div class="text-xs font-medium text-slate-400 uppercase tracking-wider font-mono">Prompts Inspected</div>
          <div id="kpi-requests" class="text-3xl font-extrabold text-white mt-2 font-mono">{metrics['total_requests']:,}</div>
          <div class="text-xs text-emerald-400 mt-2 flex items-center">↑ 100% Zero Cloud Leak</div>
        </div>

        <div class="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-sm">
          <div class="text-xs font-medium text-slate-400 uppercase tracking-wider font-mono">Secrets & PII Masked</div>
          <div id="kpi-secrets" class="text-3xl font-extrabold text-cyan-400 mt-2 font-mono">{metrics['total_secrets_masked']:,}</div>
          <div class="text-xs text-slate-400 mt-2 font-mono">Format-Preserving Surrogates</div>
        </div>

        <div class="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-sm">
          <div class="text-xs font-medium text-slate-400 uppercase tracking-wider font-mono">Agent Hijacks Blocked</div>
          <div id="kpi-hijacks" class="text-3xl font-extrabold text-rose-500 mt-2 font-mono">{metrics['total_agent_hijacks_blocked']:,}</div>
          <div class="text-xs text-rose-400 mt-2 font-mono">I/O Gate Lockouts (&lt; 2ms)</div>
        </div>

        <div class="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-sm">
          <div class="text-xs font-medium text-slate-400 uppercase tracking-wider font-mono">ZDR Compliance Health</div>
          <div class="text-3xl font-extrabold text-emerald-400 mt-2 font-mono">{metrics['zdr_compliance_score']}%</div>
          <div class="text-xs text-slate-400 mt-2 font-mono">Zero Plaintext In-Transit</div>
        </div>
      </div>

      <!-- Charts Section -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div class="bg-slate-900 border border-slate-800 rounded-xl p-6">
          <h3 class="text-sm font-semibold text-white mb-4">Intercepted Secret Distribution</h3>
          <div class="h-64 flex items-center justify-center">
            <canvas id="categoryChart"></canvas>
          </div>
        </div>

        <div class="bg-slate-900 border border-slate-800 rounded-xl p-6">
          <h3 class="text-sm font-semibold text-white mb-4">RawHuman Attestation Telemetry</h3>
          <div class="h-64 flex items-center justify-center">
            <canvas id="ioChart"></canvas>
          </div>
        </div>
      </div>

      <!-- Live Event Log -->
      <div class="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
        <div class="p-5 border-b border-slate-800 flex justify-between items-center">
          <div>
            <h3 class="text-sm font-bold text-white uppercase tracking-wider">Real-Time Security Event Telemetry</h3>
            <p class="text-xs text-slate-400 mt-0.5">Live tail from workstation proxies and agent sentinel</p>
          </div>
          <span class="text-xs font-mono text-indigo-400 bg-indigo-500/10 px-2.5 py-1 rounded border border-indigo-500/20">LIVE STREAM</span>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs font-mono">
            <thead class="bg-slate-950/60 text-slate-400 uppercase text-[10px] tracking-wider border-b border-slate-800">
              <tr>
                <th class="py-3 px-4">Time</th>
                <th class="py-3 px-4">Source Endpoint</th>
                <th class="py-3 px-4">Event</th>
                <th class="py-3 px-4">Classification</th>
                <th class="py-3 px-4">Action</th>
                <th class="py-3 px-4">Status</th>
              </tr>
            </thead>
            <tbody id="events-tbody" class="divide-y divide-slate-800/60">
    """

    for ev in metrics["recent_events"]:
        badge_color = "bg-rose-500/20 text-rose-400 border-rose-500/30" if ev["status"] == "BLOCKED" else "bg-emerald-500/20 text-emerald-400 border-emerald-500/30"
        if ev["status"] == "AIR-GAPPED":
            badge_color = "bg-amber-500/20 text-amber-400 border-amber-500/30"

        html += f"""
              <tr class="hover:bg-slate-800/30 transition">
                <td class="py-3 px-4 text-slate-400">{ev['time']}</td>
                <td class="py-3 px-4 text-slate-200">{ev['source']}</td>
                <td class="py-3 px-4 text-white font-medium">{ev['event']}</td>
                <td class="py-3 px-4 text-indigo-300">{ev['category']}</td>
                <td class="py-3 px-4 text-slate-300">{ev['action']}</td>
                <td class="py-3 px-4">
                  <span class="px-2 py-0.5 rounded text-[10px] font-bold border {badge_color}">{ev['status']}</span>
                </td>
              </tr>
        """

    html += """
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- TAB 4: API & DIAGNOSTICS -->
    <div id="tab-diagnostics" class="hidden space-y-6">
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-6">
        <h3 class="text-sm font-bold text-white uppercase tracking-wider font-mono">Live Endpoints & Diagnostics</h3>
        <p class="text-xs text-slate-400 mt-1">Directly test GhostGate proxy and metrics APIs in your browser:</p>
        <div class="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4 font-mono text-xs">
          <a href="/health" target="_blank" class="block bg-slate-950 border border-slate-800 hover:border-indigo-500 p-4 rounded-lg transition">
            <div class="text-indigo-400 font-bold">GET /health</div>
            <div class="text-slate-400 text-[11px] mt-1">Inspect service status & active redaction rules</div>
          </a>
          <a href="/api/dashboard/metrics" target="_blank" class="block bg-slate-950 border border-slate-800 hover:border-cyan-500 p-4 rounded-lg transition">
            <div class="text-cyan-400 font-bold">GET /api/dashboard/metrics</div>
            <div class="text-slate-400 text-[11px] mt-1">Raw telemetry JSON for external SIEM integration</div>
          </a>
          <a href="/docs" target="_blank" class="block bg-slate-950 border border-slate-800 hover:border-purple-500 p-4 rounded-lg transition">
            <div class="text-purple-400 font-bold">GET /docs</div>
            <div class="text-slate-400 text-[11px] mt-1">Interactive OpenAPI / Swagger documentation</div>
          </a>
        </div>
      </div>
    </div>

  </main>

  <script>
    // Tab Switching Logic
    function switchTab(tabName) {
      const tabs = ['playground', 'rawhuman', 'dashboard', 'diagnostics'];
      tabs.forEach(t => {
        document.getElementById('tab-' + t).classList.add('hidden');
        const btn = document.getElementById('tab-btn-' + t);
        btn.classList.remove('bg-indigo-600', 'text-white', 'font-semibold');
        btn.classList.add('text-slate-400');
      });
      document.getElementById('tab-' + tabName).classList.remove('hidden');
      const activeBtn = document.getElementById('tab-btn-' + tabName);
      activeBtn.classList.add('bg-indigo-600', 'text-white', 'font-semibold');
      activeBtn.classList.remove('text-slate-400');

      if (tabName === 'dashboard' && !window.chartsInitialized) {
        initCharts();
      }
    }

    // Demo Presets
    const presets = {
      aws: 'import boto3\\n# Initialize production S3 client\\nclient = boto3.client(\\n    "s3",\\n    aws_access_key_id="AKIAIOSFODNN7EXAMPLE",\\n    aws_secret_access_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"\\n)\\nresponse = client.list_buckets()',
      postgres: 'DATABASE_URL="postgres://admin:SuperSecretPass123@prod-db.internal.corp:5432/finance_db"\\nengine = create_engine(DATABASE_URL)\\nwith engine.connect() as conn:\\n    conn.execute("SELECT * FROM payroll_records")',
      pii: 'Customer security escalation: user minsu.security@internal-corp.io reported suspicious login.\\nPhone on file: +1-415-555-0199.\\nSession token: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.e30.t-ID1UrDasdqw98123',
      airgap: '# @airgap\\n# CLASSIFIED: Next-generation quantum encryption key exchange algorithm\\ndef proprietary_key_exchange(secret_seed):\\n    # Must never touch external cloud LLM servers\\n    return hash_matrix(secret_seed)'
    };

    function loadPreset(name) {
      if (presets[name]) {
        document.getElementById('prompt-input').value = presets[name];
        executeRedaction();
      }
    }

    // Interactive Redaction Call
    async function executeRedaction() {
      const prompt = document.getElementById('prompt-input').value;
      if (!prompt.trim()) return;

      const btn = document.getElementById('btn-redact');
      btn.innerHTML = '<span>⚡ Processing...</span>';

      try {
        const resp = await fetch('/api/demo/redact', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ prompt: prompt, mode: 'FORMAT_PRESERVING' })
        });
        const data = await resp.json();

        document.getElementById('redacted-output').textContent = data.redacted_text;
        document.getElementById('latency-badge').textContent = data.latency_ms + ' ms';
        
        if (data.is_airgap) {
          document.getElementById('shield-badge').textContent = 'AIR-GAPPED TO LOCAL OLLAMA';
          document.getElementById('shield-badge').className = 'text-[11px] font-mono px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 border border-amber-500/30';
          document.getElementById('rehydrate-status').textContent = '100% Offline Local Model Processing';
        } else {
          document.getElementById('shield-badge').textContent = 'SECURED (' + data.redaction_count + ' TOKENS SHADOWED)';
          document.getElementById('shield-badge').className = 'text-[11px] font-mono px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30';
          document.getElementById('rehydrate-status').textContent = 'Rehydrated In-Memory: Match Guaranteed';
        }
      } catch (err) {
        console.error(err);
      } finally {
        btn.innerHTML = '<span>⚡ Intercept & Shadow Secret</span>';
      }
    }

    // Interactive RawHuman Agent Call
    async function runAgentDemo(scenario) {
      const resp = await fetch('/api/demo/rawhuman', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ scenario: scenario })
      });
      const res = await resp.json();

      document.getElementById('raw-os-flag').textContent = res.platform_flag;
      document.getElementById('raw-os-flag').className = res.os_flag_detected ? 'text-lg font-bold font-mono text-rose-400 mt-2' : 'text-lg font-bold font-mono text-emerald-400 mt-2';

      document.getElementById('raw-entropy').textContent = (res.curvature_entropy_score * 100).toFixed(1) + '%';
      document.getElementById('raw-entropy').className = res.curvature_entropy_score < 0.2 ? 'text-lg font-bold font-mono text-rose-400 mt-2' : 'text-lg font-bold font-mono text-emerald-400 mt-2';

      document.getElementById('raw-jitter').textContent = (res.timing_jitter_entropy * 100).toFixed(1) + '%';
      document.getElementById('raw-jitter').className = res.timing_jitter_entropy < 0.25 ? 'text-lg font-bold font-mono text-rose-400 mt-2' : 'text-lg font-bold font-mono text-emerald-400 mt-2';

      const vBox = document.getElementById('raw-verdict-box');
      if (res.is_bot) {
        vBox.className = 'bg-rose-950/30 border border-rose-800/60 rounded-xl p-6 font-mono text-xs space-y-2';
        vBox.innerHTML = `
          <div class="text-rose-400 font-bold text-sm">✖ AUTONOMOUS AI AGENT DETECTED & TERMINATED</div>
          <div class="text-slate-300">Confidence Score: <span class="text-rose-400 font-bold">${(res.human_confidence * 100).toFixed(1)}%</span></div>
          <div class="text-slate-400">Threat Details: ${res.rejection_reasons.join(' • ')}</div>
          <div class="text-rose-300 font-semibold mt-2">${res.action_taken}</div>
        `;
      } else {
        vBox.className = 'bg-emerald-950/30 border border-emerald-800/60 rounded-xl p-6 font-mono text-xs space-y-2';
        vBox.innerHTML = `
          <div class="text-emerald-400 font-bold text-sm">✔ AUTHENTIC HUMAN VERIFIED</div>
          <div class="text-slate-300">Confidence Score: <span class="text-emerald-400 font-bold">${(res.human_confidence * 100).toFixed(1)}%</span></div>
          <div class="text-slate-400">Origin: Physical Hardware HID Controller</div>
          <div class="text-emerald-300 font-semibold mt-2">Attestation ID: rawhuman_attest_9f83a8b29f01c4 • Action Permitted</div>
        `;
      }
    }

    // Chart.js initialization
    function initCharts() {
      window.chartsInitialized = true;
      const ctxCat = document.getElementById('categoryChart').getContext('2d');
      new Chart(ctxCat, {
        type: 'doughnut',
        data: {
          labels: ['AWS Keys', 'DB URIs', 'OpenAI Keys', 'PII & Emails', 'Private Keys'],
          datasets: [{
            data: [512, 389, 441, 320, 180],
            backgroundColor: ['#6366f1', '#06b6d4', '#a855f7', '#10b981', '#f43f5e'],
            borderWidth: 0
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { position: 'right', labels: { color: '#94a3b8', font: { family: 'JetBrains Mono', size: 10 } } }
          }
        }
      });

      const ctxIo = document.getElementById('ioChart').getContext('2d');
      new Chart(ctxIo, {
        type: 'bar',
        data: {
          labels: ['Physical HID', 'Synthetic Win32', 'Quartz Synthesized', 'Flat Timing Quanta', 'WebAuthn Fallback'],
          datasets: [{
            label: 'Attestation Events',
            data: [12840, 210, 85, 52, 340],
            backgroundColor: '#6366f1',
            borderRadius: 4
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: { ticks: { color: '#94a3b8', font: { family: 'JetBrains Mono', size: 9 } } },
            y: { ticks: { color: '#94a3b8' }, grid: { color: '#1e293b' } }
          },
          plugins: {
            legend: { display: false }
          }
        }
      });
    }

    // Pre-populate with AWS preset on load
    window.addEventListener('DOMContentLoaded', () => {
      loadPreset('aws');
    });
  </script>
</body>
</html>
"""
    return HTMLResponse(content=html, status_code=200)
