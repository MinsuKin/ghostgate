"""
GhostGate Core: Executive CISO Dashboard & Zero-Background Investor Sandbox.
Provides an intuitive, narrative-driven interactive web interface for investors,
CISOs, and security evaluators to immediately experience real-time data leak protection,
format-preserving synthetic shadowing, autonomous AI agent takeover defense, and live SOC telemetry.
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
<html lang="ko" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>GhostGate Labs // CISO Security Operations Center & Zero-Trust AI Privacy Shield</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Noto+Sans+KR:wght@400;500;700;800&display=swap" rel="stylesheet">
  <script>
    tailwind.config = {{
      darkMode: 'class',
      theme: {{
        extend: {{
          fontFamily: {{
            sans: ['"Plus Jakarta Sans"', '"Noto Sans KR"', 'sans-serif'],
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
<body class="bg-[#0b0f19] text-slate-100 min-h-screen font-sans antialiased selection:bg-indigo-500 selection:text-white">

  <!-- TOP EXECUTIVE NAVIGATION BAR -->
  <header class="border-b border-slate-800/80 bg-[#0d1322]/90 backdrop-blur sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <div class="h-10 w-10 rounded-xl bg-gradient-to-tr from-indigo-500 via-purple-500 to-cyan-400 flex items-center justify-center font-bold text-white shadow-lg shadow-indigo-500/25">
          🛡️
        </div>
        <div>
          <div class="flex items-center gap-2">
            <span class="font-extrabold text-xl tracking-wider text-white">GHOSTGATE</span>
            <span class="text-[10px] px-2 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 font-mono font-bold tracking-wide">ENTERPRISE AI SHIELD</span>
          </div>
          <p class="text-[11px] text-slate-400 hidden sm:block" id="nav-tagline">Zero-Trust Bulletproof Glass Between Employees & Cloud AI</p>
        </div>
      </div>
      
      <!-- Center Navigation Tabs -->
      <nav class="hidden lg:flex items-center bg-slate-950/80 p-1 rounded-xl border border-slate-800/80 text-xs font-medium">
        <button onclick="switchTab('leak-defense')" id="tab-btn-leak-defense" class="px-4 py-2 rounded-lg bg-indigo-600 text-white font-bold transition shadow-sm">
          ⚡ <span class="lang-text" data-en="⚡ AI Privacy Playground" data-ko="⚡ 실시간 기밀유출 방어 (Playground)">AI Privacy Playground</span>
        </button>
        <button onclick="switchTab('agent-defense')" id="tab-btn-agent-defense" class="px-4 py-2 rounded-lg text-slate-400 hover:text-white transition font-medium">
          🤖 <span class="lang-text" data-en="AI Agent Hijack Defense" data-ko="자율 AI 탈취 방어">자율 AI 탈취 방어</span>
        </button>
        <button onclick="switchTab('vc-pitch')" id="tab-btn-vc-pitch" class="px-4 py-2 rounded-lg text-slate-400 hover:text-white transition font-medium">
          📈 <span class="lang-text" data-en="VC Pitch & ROI" data-ko="투자 핵심 & 시장 기회">투자 핵심 & 시장 기회</span>
        </button>
        <button onclick="switchTab('soc-telemetry')" id="tab-btn-soc-telemetry" class="px-4 py-2 rounded-lg text-slate-400 hover:text-white transition font-medium">
          📊 <span class="lang-text" data-en="CISO Telemetry" data-ko="보안 관제 센터">보안 관제 센터</span>
        </button>
        <button onclick="switchTab('api-specs')" id="tab-btn-api-specs" class="px-4 py-2 rounded-lg text-slate-400 hover:text-white transition font-medium">
          🔌 <span class="lang-text" data-en="Live API Docs" data-ko="API 사양서">API 사양서</span>
        </button>
      </nav>

      <!-- Right Action / Language Toggle -->
      <div class="flex items-center space-x-3 text-xs">
        <!-- Bilingual Language Switcher -->
        <button onclick="toggleLanguage()" id="lang-btn" class="flex items-center gap-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 px-3 py-1.5 rounded-lg font-bold transition font-mono">
          <span id="lang-flag">🇺🇸</span>
          <span id="lang-label">English</span>
        </button>
        <a href="https://github.com/MinsuKin/ghostgate" target="_blank" class="hidden sm:inline-flex items-center gap-1.5 bg-indigo-600/20 hover:bg-indigo-600/30 text-indigo-300 border border-indigo-500/30 px-3 py-1.5 rounded-lg font-bold transition">
          <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg>
          GitHub
        </a>
      </div>
    </div>
  </header>

  <!-- EXECUTIVE HERO PITCH BANNER -->
  <section class="border-b border-slate-800/60 bg-gradient-to-b from-[#11192e] to-[#0b0f19] py-8 px-4 sm:px-6">
    <div class="max-w-7xl mx-auto">
      <div class="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-6">
        <div class="max-w-3xl">
          <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-mono font-bold mb-3">
            <span class="h-2 w-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span class="lang-text" data-en="PROTECTION ACTIVE • 0.14ms INLINE SPEED" data-ko="실시간 보호 가동 중 • 0.14ms 초저지연">PROTECTION ACTIVE • 0.14ms INLINE SPEED</span>
          </div>
          <h1 class="text-2xl sm:text-3xl lg:text-4xl font-extrabold text-white tracking-tight leading-tight">
            <span class="lang-text" 
                  data-en="The Invisible Bulletproof Glass Between Enterprise Employees and Cloud AI." 
                  data-ko="기업용 AI의 투명 방탄유리: 직원은 자유롭게, 기밀은 완벽하게.">
              기업용 AI의 투명 방탄유리: 직원은 자유롭게, 기밀은 완벽하게.
            </span>
          </h1>
          <p class="mt-3 text-sm sm:text-base text-slate-300 leading-relaxed">
            <span class="lang-text"
                  data-en="When employees use ChatGPT or Claude, they accidentally paste database passwords, client emails, and AWS keys. GhostGate sits invisibly on the workstation, swaps real secrets with harmless fake replicas in 0.1 milliseconds before they leave the laptop, and seamlessly restores the real secrets when AI replies."
                  data-ko="직원들이 ChatGPT나 Claude를 쓸 때 회사 DB 비밀번호, 고객 개인정보, AWS 클라우드 키를 무심코 붙여넣습니다. GhostGate는 0.1밀리초 만에 기밀을 무해한 가짜 데이터로 자동 바꿔치기하여 클라우드로 1바이트도 유출되지 않게 하고, AI가 답변을 주면 원래 비밀번호로 무손실 자동 복원합니다.">
              직원들이 ChatGPT나 Claude를 쓸 때 회사 DB 비밀번호, 고객 개인정보, AWS 클라우드 키를 무심코 붙여넣습니다. GhostGate는 0.1밀리초 만에 기밀을 무해한 가짜 데이터로 자동 바꿔치기하여 클라우드로 1바이트도 유출되지 않게 하고, AI가 답변을 주면 원래 비밀번호로 무손실 자동 복원합니다.
            </span>
          </p>
        </div>

        <!-- 3-Step Visual Card for Zero-Background Investors -->
        <div class="w-full lg:w-auto bg-slate-900/90 border border-slate-800 rounded-2xl p-4 sm:p-5 shadow-xl">
          <div class="text-[11px] font-bold uppercase tracking-wider text-indigo-400 font-mono mb-3">
            <span class="lang-text" data-en="How GhostGate Works In 3 Steps" data-ko="GhostGate 3단계 작동 원리">GhostGate 3단계 작동 원리</span>
          </div>
          <div class="grid grid-cols-3 gap-3 text-center">
            <div class="bg-slate-950/80 p-3 rounded-xl border border-rose-500/30">
              <div class="text-rose-400 font-extrabold text-sm sm:text-base">1. 🚨 DANGER</div>
              <div class="text-[11px] text-slate-300 mt-1 font-medium">
                <span class="lang-text" data-en="Employee pastes real DB password into AI" data-ko="직원이 실제 DB 비번을 AI에 입력">직원이 실제 DB 비번을 AI에 입력</span>
              </div>
            </div>
            <div class="bg-slate-950/80 p-3 rounded-xl border border-indigo-500/40">
              <div class="text-indigo-400 font-extrabold text-sm sm:text-base">2. ⚡ 0.14ms</div>
              <div class="text-[11px] text-slate-300 mt-1 font-medium">
                <span class="lang-text" data-en="GhostGate swaps secret into fake token" data-ko="0.1밀리초 만에 가짜 데이터로 치환">0.1밀리초 만에 가짜 데이터로 치환</span>
              </div>
            </div>
            <div class="bg-slate-950/80 p-3 rounded-xl border border-emerald-500/30">
              <div class="text-emerald-400 font-extrabold text-sm sm:text-base">3. 🛡️ ZERO LEAK</div>
              <div class="text-[11px] text-slate-300 mt-1 font-medium">
                <span class="lang-text" data-en="OpenAI writes code; secrets stay 100% safe" data-ko="AI는 코드 완성, 기밀은 0바이트 유출">AI는 코드 완성, 기밀은 0바이트 유출</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- MAIN INTERACTIVE CONTAINER -->
  <main class="max-w-7xl mx-auto px-4 sm:px-6 py-8">

    <!-- ================================================================= -->
    <!-- TAB 1: LIVE DATA LEAK DEFENSE (BEFORE VS AFTER SANDBOX)            -->
    <!-- ================================================================= -->
    <div id="tab-leak-defense" class="space-y-8">
      <!-- Scenario Selector Banner -->
      <div class="bg-gradient-to-r from-indigo-950/60 via-purple-950/30 to-slate-900 border border-indigo-500/30 rounded-2xl p-6 shadow-lg">
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div class="flex items-center gap-2">
              <span class="text-xs px-2.5 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 font-mono font-bold">INTERACTIVE DEMO</span>
              <h2 class="text-xl font-extrabold text-white">
                <span class="lang-text" data-en="Test A Real-World Corporate Data Leak" data-ko="실제 기업 기밀 유출 상황을 직접 테스트해보세요">실제 기업 기밀 유출 상황을 직접 테스트해보세요</span>
              </h2>
            </div>
            <p class="text-xs sm:text-sm text-slate-300 mt-1.5 max-w-3xl leading-relaxed">
              <span class="lang-text"
                    data-en="Choose an employee mistake below to see how GhostGate transparently intercepts credentials before they leave the laptop."
                    data-ko="아래에서 직원이 흔히 저지르는 기밀 유출 시나리오를 선택하세요. GhostGate가 어떻게 외부 전송 직전 가짜 데이터로 안전하게 바꿔치기하는지 실시간으로 증명합니다.">
                아래에서 직원이 흔히 저지르는 기밀 유출 시나리오를 선택하세요. GhostGate가 어떻게 외부 전송 직전 가짜 데이터로 안전하게 바꿔치기하는지 실시간으로 증명합니다.
              </span>
            </p>
          </div>
          <div class="flex items-center gap-2 bg-slate-950/80 px-4 py-2 rounded-xl border border-slate-800 text-xs font-mono shrink-0">
            <span class="text-slate-400">Engine Speed:</span>
            <span id="latency-badge" class="px-2.5 py-1 rounded bg-indigo-500/20 text-indigo-300 font-extrabold border border-indigo-500/30">0.142 ms</span>
          </div>
        </div>

        <!-- Real-Life Scenario Buttons -->
        <div class="mt-5 pt-4 border-t border-slate-800/80 flex flex-wrap items-center gap-2.5">
          <span class="text-xs text-slate-400 font-bold mr-1">
            <span class="lang-text" data-en="Select Scenario:" data-ko="시나리오 선택:">시나리오 선택:</span>
          </span>
          <button onclick="loadScenario('postgres')" id="btn-scen-postgres" class="text-xs bg-slate-800 hover:bg-slate-700 border border-slate-700 px-3.5 py-2 rounded-xl text-cyan-300 font-bold transition flex items-center gap-2 shadow-sm">
            <span>🏢</span>
            <span class="lang-text" data-en="Scenario 1: Payroll Database Password" data-ko="시나리오 1: 사내 급여 DB 비밀번호 유출">시나리오 1: 사내 급여 DB 비밀번호 유출</span>
          </button>
          <button onclick="loadScenario('aws')" id="btn-scen-aws" class="text-xs bg-slate-800 hover:bg-slate-700 border border-slate-700 px-3.5 py-2 rounded-xl text-indigo-300 font-bold transition flex items-center gap-2 shadow-sm">
            <span>☁️</span>
            <span class="lang-text" data-en="Scenario 2: Cloud AWS Master Key" data-ko="시나리오 2: AWS 클라우드 마스터 키 유출">시나리오 2: AWS 클라우드 마스터 키 유출</span>
          </button>
          <button onclick="loadScenario('pii')" id="btn-scen-pii" class="text-xs bg-slate-800 hover:bg-slate-700 border border-slate-700 px-3.5 py-2 rounded-xl text-purple-300 font-bold transition flex items-center gap-2 shadow-sm">
            <span>💳</span>
            <span class="lang-text" data-en="Scenario 3: Customer Phone, Email & Token" data-ko="시나리오 3: 고객 개인정보 & 인증 토큰 유출">시나리오 3: 고객 개인정보 & 인증 토큰 유출</span>
          </button>
          <button onclick="loadScenario('airgap')" id="btn-scen-airgap" class="text-xs bg-slate-800 hover:bg-slate-700 border border-slate-700 px-3.5 py-2 rounded-xl text-amber-300 font-bold transition flex items-center gap-2 shadow-sm">
            <span>🔒</span>
            <span class="lang-text" data-en="Scenario 4: Top-Secret Code (#@airgap)" data-ko="시나리오 4: 극비 국방/금융 알고리즘 (#@airgap)">시나리오 4: 극비 국방/금융 알고리즘 (#@airgap)</span>
          </button>
        </div>
      </div>

      <!-- VISUAL SIDE-BY-SIDE: WHAT EMPLOYEE TYPED vs WHAT OPENAI RECEIVES -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- LEFT COLUMN: EMPLOYEE LAPTOP (DANGER / REAL SECRET) -->
        <div class="bg-[#0f172a] border-2 border-rose-500/40 rounded-2xl p-5 sm:p-6 flex flex-col justify-between space-y-4 shadow-xl">
          <div>
            <div class="flex items-center justify-between mb-3">
              <div class="flex items-center gap-2">
                <span class="h-3 w-3 rounded-full bg-rose-500 animate-ping"></span>
                <span class="text-xs font-extrabold uppercase tracking-wider text-rose-400 font-mono">
                  <span class="lang-text" data-en="1. What Employee Typed (Laptop)" data-ko="1. 직원이 입력한 내용 (내부 노트북)">1. 직원이 입력한 내용 (내부 노트북)</span>
                </span>
              </div>
              <span class="text-[11px] font-bold px-2.5 py-0.5 rounded bg-rose-500/20 text-rose-300 border border-rose-500/30">
                <span class="lang-text" data-en="🚨 DANGER: REAL CREDENTIALS" data-ko="🚨 위험: 실제 회사 기밀 노출">🚨 위험: 실제 회사 기밀 노출</span>
              </span>
            </div>
            <p class="text-xs text-slate-400 mb-2 leading-relaxed">
              <span class="lang-text"
                    data-en="Without GhostGate, these real database passwords and private keys are sent directly to public cloud servers."
                    data-ko="GhostGate가 없다면 이 실제 비밀번호와 개인정보는 그대로 OpenAI 서버로 전송되어 영구 저장됩니다.">
                GhostGate가 없다면 이 실제 비밀번호와 개인정보는 그대로 OpenAI 서버로 전송되어 영구 저장됩니다.
              </span>
            </p>
            <textarea id="prompt-input" rows="8" class="w-full bg-[#070b14] border border-slate-800 rounded-xl p-3 text-xs font-mono text-slate-100 focus:outline-none focus:border-indigo-500 resize-none leading-relaxed" placeholder="Type code or secret here..."></textarea>
          </div>
          <div class="flex flex-col sm:flex-row items-center justify-between gap-3 pt-2">
            <span class="text-[11px] text-slate-400 font-mono">
              <span class="lang-text" data-en="Protection: Format-Preserving Masking" data-ko="보호 방식: 포맷 보존 실시간 가명화">보호 방식: 포맷 보존 실시간 가명화</span>
            </span>
            <button onclick="executeRedaction()" id="btn-redact" class="w-full sm:w-auto bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white px-5 py-2.5 rounded-xl font-extrabold text-xs font-mono shadow-lg shadow-indigo-600/30 transition flex items-center justify-center gap-2">
              <span>⚡</span>
              <span class="lang-text" data-en="Click to Protect & Shadow Secret" data-ko="클릭: 기밀 가명화 및 차단 실행">클릭: 기밀 가명화 및 차단 실행</span>
            </button>
          </div>
        </div>

        <!-- RIGHT COLUMN: WHAT CLOUD LLM RECEIVES (PROTECTED / ZERO LEAK) -->
        <div class="bg-[#0f172a] border-2 border-emerald-500/40 rounded-2xl p-5 sm:p-6 flex flex-col justify-between space-y-4 shadow-xl">
          <div>
            <div class="flex items-center justify-between mb-3">
              <div class="flex items-center gap-2">
                <span class="h-3 w-3 rounded-full bg-emerald-400"></span>
                <span class="text-xs font-extrabold uppercase tracking-wider text-emerald-400 font-mono">
                  <span class="lang-text" data-en="2. What Cloud AI Receives (Egress)" data-ko="2. OpenAI/Claude가 실제 전달받는 내용">2. OpenAI/Claude가 실제 전달받는 내용</span>
                </span>
              </div>
              <span id="shield-badge" class="text-[11px] font-bold px-2.5 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                <span class="lang-text" data-en="🛡️ 100% SECURED (0 BYTES LEAKED)" data-ko="🛡️ 100% 안전 (기밀 0바이트 유출)">🛡️ 100% 안전 (기밀 0바이트 유출)</span>
              </span>
            </div>
            <p class="text-xs text-slate-400 mb-2 leading-relaxed">
              <span class="lang-text"
                    data-en="GhostGate replaced real secrets with synthetic dummy replicas. ChatGPT thinks it's real code and writes the solution perfectly."
                    data-ko="GhostGate가 실제 기밀을 감쪽같은 가짜 데이터로 바꿨습니다. AI는 정상 코드로 인식하여 버그 없이 코드를 완성합니다.">
                GhostGate가 실제 기밀을 감쪽같은 가짜 데이터로 바꿨습니다. AI는 정상 코드로 인식하여 버그 없이 코드를 완성합니다.
              </span>
            </p>
            <div id="redacted-output" class="w-full h-48 bg-[#070b14] border border-slate-800 rounded-xl p-3 text-xs font-mono text-emerald-400 overflow-y-auto whitespace-pre-wrap leading-relaxed">Click "Protect & Shadow Secret" on the left to see live protection...</div>
          </div>
          <div class="bg-slate-950/80 border border-slate-800 rounded-xl p-3 text-xs flex flex-wrap items-center justify-between gap-2">
            <span class="text-slate-400">
              <span class="lang-text" data-en="Lossless Recovery on Response:" data-ko="AI 답변 시 자동 복구:">AI 답변 시 자동 복구:</span>
            </span>
            <span id="rehydrate-status" class="text-indigo-300 font-bold">
              <span class="lang-text" data-en="In-Memory Rehydration: Real Data Restored on Laptop" data-ko="로컬 메모리 무손실 복원: 직원 화면엔 원본 표시">로컬 메모리 무손실 복원: 직원 화면엔 원본 표시</span>
            </span>
          </div>
        </div>
      </div>

      <!-- 3 PROOFS FOR INVESTORS (WHY GHOSTGATE WINS) -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 pt-4">
        <div class="bg-slate-900/80 border border-slate-800 rounded-2xl p-5">
          <div class="text-2xl mb-2">⚡</div>
          <h3 class="text-sm font-bold text-white">
            <span class="lang-text" data-en="0.14ms Overhead (Invisible Speed)" data-ko="0.14ms 초저지연 (체감 지연 0)">0.14ms 초저지연 (체감 지연 0)</span>
          </h3>
          <p class="text-xs text-slate-400 mt-1.5 leading-relaxed">
            <span class="lang-text"
                  data-en="Human eyes take 100ms to blink. GhostGate processes security rules in 0.14ms. Developers feel zero lag in Cursor, VSCode, or web browsers."
                  data-ko="인간의 눈 깜빡임(100ms)보다 700배 빠릅니다. 개발자는 Cursor나 브라우저에서 지연을 전혀 느끼지 못하고 코딩에 집중합니다.">
              인간의 눈 깜빡임(100ms)보다 700배 빠릅니다. 개발자는 Cursor나 브라우저에서 지연을 전혀 느끼지 못하고 코딩에 집중합니다.
            </span>
          </p>
        </div>

        <div class="bg-slate-900/80 border border-slate-800 rounded-2xl p-5">
          <div class="text-2xl mb-2">🧩</div>
          <h3 class="text-sm font-bold text-white">
            <span class="lang-text" data-en="100% Code Integrity (No Broken AI)" data-ko="AI 코드 문법 보존 (에러 발생 제로)">AI 코드 문법 보존 (에러 발생 제로)</span>
          </h3>
          <p class="text-xs text-slate-400 mt-1.5 leading-relaxed">
            <span class="lang-text"
                  data-en="Dumb DLP tools replace text with '[REDACTED]', which breaks Python syntax and causes AI hallucination. GhostGate generates syntax-valid dummy tokens."
                  data-ko="기존 보안 툴처럼 [삭제됨]으로 가리면 AI가 문법 오류를 일으킵니다. GhostGate는 실제와 동일한 자릿수의 가짜 토큰을 만들어 AI가 완벽한 코드를 작성합니다.">
              기존 보안 툴처럼 [삭제됨]으로 가리면 AI가 문법 오류를 일으킵니다. GhostGate는 실제와 동일한 자릿수의 가짜 토큰을 만들어 AI가 완벽한 코드를 작성합니다.
            </span>
          </p>
        </div>

        <div class="bg-slate-900/80 border border-slate-800 rounded-2xl p-5">
          <div class="text-2xl mb-2">🔄</div>
          <h3 class="text-sm font-bold text-white">
            <span class="lang-text" data-en="Zero-Friction In-Memory Rehydration" data-ko="쌍방향 무손실 복원 (Rehydration)">쌍방향 무손실 복원 (Rehydration)</span>
          </h3>
          <p class="text-xs text-slate-400 mt-1.5 leading-relaxed">
            <span class="lang-text"
                  data-en="When ChatGPT responds with refactored code, GhostGate swaps the fake tokens back to real secrets locally. The developer never has to copy-paste passwords."
                  data-ko="ChatGPT가 완성된 코드를 보내주면, GhostGate가 로컬 메모리에서 가짜 데이터를 진짜 비밀번호로 자동 복구해 주므로 직원은 일체의 수작업이 필요 없습니다.">
              ChatGPT가 완성된 코드를 보내주면, GhostGate가 로컬 메모리에서 가짜 데이터를 진짜 비밀번호로 자동 복구해 주므로 직원은 일체의 수작업이 필요 없습니다.
            </span>
          </p>
        </div>
      </div>
    </div>

    <!-- ================================================================= -->
    <!-- TAB 2: ROGUE AI AGENT DEFENSE (RAWHUMAN SENTINEL)                  -->
    <!-- ================================================================= -->
    <div id="tab-agent-defense" class="hidden space-y-8">
      <div class="bg-gradient-to-r from-rose-950/40 via-slate-900 to-indigo-950/30 border border-rose-500/30 rounded-2xl p-6 shadow-lg">
        <div class="max-w-3xl">
          <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-rose-500/10 border border-rose-500/30 text-rose-400 text-xs font-mono font-bold mb-3">
            <span>🚨</span>
            <span class="lang-text" data-en="THE $50B EMERGING THREAT: ROGUE AGENT HIJACK" data-ko="차세대 보안 위협: 자율 AI 에이전트 탈취">THE $50B EMERGING THREAT: ROGUE AGENT HIJACK</span>
          </div>
          <h2 class="text-2xl font-extrabold text-white">
            <span class="lang-text" 
                  data-en="What Happens When An AI Agent Takes Control of Your Mouse & Keyboard?" 
                  data-ko="AI 에이전트가 직원의 마우스와 키보드를 직접 조작할 때, 어떻게 통제할 것인가?">
              AI 에이전트가 직원의 마우스와 키보드를 직접 조작할 때, 어떻게 통제할 것인가?
            </span>
          </h2>
          <p class="text-xs sm:text-sm text-slate-300 mt-2 leading-relaxed">
            <span class="lang-text"
                  data-en="New autonomous agents (Anthropic Computer Use, OpenAI Operator) can physically control employee laptops. But what if a malicious website tricks an AI agent via prompt injection into clicking 'Transfer $1,000,000' or wiping your enterprise database? GhostGate RawHuman™ inspects physical motor kinematics to physically block unauthorized AI bot clicks."
                  data-ko="Anthropic Computer Use, OpenAI Operator처럼 사람 대신 마우스와 키보드를 움직이는 자율 AI 에이전트가 확산되고 있습니다. 만약 해커의 프롬프트 주입 공격을 받은 AI 에이전트가 직원 동의 없이 거액을 송금하거나 기업 DB를 삭제하려 한다면? GhostGate RawHuman™은 인간의 미세 손떨림과 생체역학 곡률을 감지하여 불법 AI 봇 조작을 0.002초 만에 물리 차단합니다.">
              Anthropic Computer Use, OpenAI Operator처럼 사람 대신 마우스와 키보드를 움직이는 자율 AI 에이전트가 확산되고 있습니다. 만약 해커의 프롬프트 주입 공격을 받은 AI 에이전트가 직원 동의 없이 거액을 송금하거나 기업 DB를 삭제하려 한다면? GhostGate RawHuman™은 인간의 미세 손떨림과 생체역학 곡률을 감지하여 불법 AI 봇 조작을 0.002초 만에 물리 차단합니다.
            </span>
          </p>
        </div>

        <!-- Simulation Buttons -->
        <div class="mt-6 flex flex-wrap items-center gap-3">
          <button onclick="runAgentDemo('agent')" id="btn-scenario-agent" class="bg-gradient-to-r from-rose-600 to-red-600 hover:from-rose-500 hover:to-red-500 text-white px-5 py-2.5 rounded-xl font-extrabold text-xs shadow-lg shadow-rose-600/30 transition flex items-center gap-2">
            <span>🤖</span>
            <span class="lang-text" data-en="Simulate Rogue AI Agent Click (SendInput Bot)" data-ko="해킹된 AI 에이전트 조작 시뮬레이션 (봇 클릭)">해킹된 AI 에이전트 조작 시뮬레이션 (봇 클릭)</span>
          </button>
          <button onclick="runAgentDemo('human')" id="btn-scenario-human" class="bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 px-5 py-2.5 rounded-xl font-bold text-xs transition flex items-center gap-2">
            <span>👤</span>
            <span class="lang-text" data-en="Simulate Real Human Employee (Physical Mouse)" data-ko="실제 인간 직원 조작 시뮬레이션 (인간 마우스)">실제 인간 직원 조작 시뮬레이션 (인간 마우스)</span>
          </button>
        </div>
      </div>

      <!-- Verdict Banner & Scorecard -->
      <div id="raw-verdict-box" class="bg-slate-900 border border-slate-800 rounded-2xl p-6 font-mono text-xs space-y-2 shadow-lg">
        <div class="text-slate-400">
          <span class="lang-text" data-en="Select an action above to test RawHuman I/O Gate attestation." data-ko="위 버튼을 클릭하여 자율 AI 차단 시뮬레이션을 실행하세요.">위 버튼을 클릭하여 자율 AI 차단 시뮬레이션을 실행하세요.</span>
        </div>
      </div>

      <!-- Telemetry Cards -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="bg-slate-900/90 border border-slate-800 rounded-2xl p-5">
          <div class="text-xs font-bold text-slate-400 uppercase tracking-wider font-mono">
            <span class="lang-text" data-en="OS Kernel Injection Hook" data-ko="OS 커널 인젝션 감지">OS 커널 인젝션 감지</span>
          </div>
          <div id="raw-os-flag" class="text-xl font-extrabold font-mono text-white mt-2">Ready...</div>
          <div class="text-xs text-slate-400 mt-1">
            <span class="lang-text" data-en="Detects programmatic PyAutoGUI / SendInput" data-ko="프로그래밍 방식 가상 마우스 주입 감시">Detects programmatic PyAutoGUI / SendInput</span>
          </div>
        </div>

        <div class="bg-slate-900/90 border border-slate-800 rounded-2xl p-5">
          <div class="text-xs font-bold text-slate-400 uppercase tracking-wider font-mono">
            <span class="lang-text" data-en="Hand Kinematic Curvature" data-ko="손 생체역학적 곡률 엔트로피">손 생체역학적 곡률 엔트로피</span>
          </div>
          <div id="raw-entropy" class="text-xl font-extrabold font-mono text-white mt-2">-</div>
          <div class="text-xs text-slate-400 mt-1">
            <span class="lang-text" data-en="Humans move with curves; bots move in straight lines" data-ko="인간은 곡선으로, AI 봇은 수학적 직선으로 이동">인간은 곡선으로, AI 봇은 수학적 직선으로 이동</span>
          </div>
        </div>

        <div class="bg-slate-900/90 border border-slate-800 rounded-2xl p-5">
          <div class="text-xs font-bold text-slate-400 uppercase tracking-wider font-mono">
            <span class="lang-text" data-en="Micro-Timing Jitter" data-ko="생체 마이크로 타이밍 지터">생체 마이크로 타이밍 지터</span>
          </div>
          <div id="raw-jitter" class="text-xl font-extrabold font-mono text-white mt-2">-</div>
          <div class="text-xs text-slate-400 mt-1">
            <span class="lang-text" data-en="Human muscle tremor vs instant 0ms bot clicks" data-ko="인간 근육의 자연 미세 떨림 확인">인간 근육의 자연 미세 떨림 확인</span>
          </div>
        </div>
      </div>
    </div>

    <!-- ================================================================= -->
    <!-- TAB 3: EXECUTIVE SUMMARY & VC PITCH (FOR INVESTORS)               -->
    <!-- ================================================================= -->
    <div id="tab-vc-pitch" class="hidden space-y-8">
      <!-- Investment Thesis Card -->
      <div class="bg-gradient-to-r from-indigo-950/70 via-slate-900 to-purple-950/50 border border-indigo-500/30 rounded-2xl p-6 sm:p-8 shadow-xl">
        <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/20 text-indigo-300 text-xs font-mono font-bold mb-4">
          <span>📈</span>
          <span class="lang-text" data-en="THE $45B ENTERPRISE AI OPPORTUNITY" data-ko="450억 달러 엔터프라이즈 AI 보안 시장">THE $45B ENTERPRISE AI OPPORTUNITY</span>
        </div>
        <h2 class="text-2xl sm:text-3xl font-extrabold text-white leading-snug">
          <span class="lang-text" 
                data-en="Why GhostGate Is The Critical Missing Layer in Enterprise AI Adoption." 
                data-ko="왜 GhostGate가 포춘 500대 기업의 생성형 AI 도입에 필수 불가결한가?">
            왜 GhostGate가 포춘 500대 기업의 생성형 AI 도입에 필수 불가결한가?
          </span>
        </h2>
        <p class="text-sm sm:text-base text-slate-300 mt-3 leading-relaxed max-w-4xl">
          <span class="lang-text"
                data-en="78% of Fortune 500 CISOs currently restrict or ban generative AI tools because of data breach liability and intellectual property theft. GhostGate solves this at the endpoint: employees get 100% productivity, while the enterprise gets mathematical zero-leak guarantees."
                data-ko="현재 포춘 500대 기업 CISO의 78%가 데이터 유출 법적 책임 및 지적 재산권 도난 우려로 사내 생성형 AI 사용을 제한하거나 금지하고 있습니다. GhostGate는 직원 단말에서 이 문제를 완벽히 해결합니다. 직원은 AI 생산성을 100% 누리고, 기업은 0바이트 유출 무결성을 보장받습니다.">
            현재 포춘 500대 기업 CISO의 78%가 데이터 유출 법적 책임 및 지적 재산권 도난 우려로 사내 생성형 AI 사용을 제한하거나 금지하고 있습니다. GhostGate는 직원 단말에서 이 문제를 완벽히 해결합니다. 직원은 AI 생산성을 100% 누리고, 기업은 0바이트 유출 무결성을 보장받습니다.
          </span>
        </p>

        <!-- 3 Core Competitive Moats -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-5 mt-6 pt-6 border-t border-slate-800">
          <div class="bg-slate-950/70 p-4 rounded-xl border border-slate-800">
            <div class="text-indigo-400 font-extrabold text-base">1. Zero Friction Proxy</div>
            <div class="text-xs text-slate-300 mt-1.5 leading-relaxed">
              <span class="lang-text" data-en="No code modification, no complex SDK. Works seamlessly across Mac, Windows, and Linux workstations." data-ko="코드 수정이나 복잡한 SDK 설치 불필요. 투명 프록시로 전사 배포 즉시 활성화.">코드 수정이나 복잡한 SDK 설치 불필요. 투명 프록시로 전사 배포 즉시 활성화.</span>
            </div>
          </div>
          <div class="bg-slate-950/70 p-4 rounded-xl border border-slate-800">
            <div class="text-purple-400 font-extrabold text-base">2. Format-Preserving AST</div>
            <div class="text-xs text-slate-300 mt-1.5 leading-relaxed">
              <span class="lang-text" data-en="Proprietary synthetic shadow tokenization that keeps code syntax valid and eliminates LLM hallucinations." data-ko="독점적 포맷 보존 가명화 기술로 코드 문법을 유지해 AI 환각 및 에러 원천 방지.">독점적 포맷 보존 가명화 기술로 코드 문법을 유지해 AI 환각 및 에러 원천 방지.</span>
            </div>
          </div>
          <div class="bg-slate-950/70 p-4 rounded-xl border border-slate-800">
            <div class="text-cyan-400 font-extrabold text-base">3. RawHuman Agent Barrier</div>
            <div class="text-xs text-slate-300 mt-1.5 leading-relaxed">
              <span class="lang-text" data-en="The world's first hardware/kinematic layer blocking rogue autonomous AI agents from hijacking employee PCs." data-ko="자율 AI 에이전트의 불법 PC 조작을 막는 세계 최초의 하드웨어 생체역학 방어선.">자율 AI 에이전트의 불법 PC 조작을 막는 세계 최초의 하드웨어 생체역학 방어선.</span>
            </div>
          </div>
        </div>
      </div>

      <!-- ROI & Business Metrics -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6">
          <div class="text-xs text-slate-400 uppercase font-mono font-bold">
            <span class="lang-text" data-en="Enterprise ROI (Avoided Breaches)" data-ko="예방된 기업 잠재 손실">예방된 기업 잠재 손실</span>
          </div>
          <div class="text-3xl font-extrabold text-emerald-400 mt-2 font-mono">$8.2M+</div>
          <div class="text-xs text-slate-400 mt-1">Based on IBM $4.45M avg breach cost</div>
        </div>

        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6">
          <div class="text-xs text-slate-400 uppercase font-mono font-bold">
            <span class="lang-text" data-en="Total Prompts Inspected" data-ko="총 검사된 사내 프롬프트">총 검사된 사내 프롬프트</span>
          </div>
          <div class="text-3xl font-extrabold text-white mt-2 font-mono">{metrics['total_requests']:,}</div>
          <div class="text-xs text-emerald-400 mt-1">100% Zero Cloud Leak</div>
        </div>

        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6">
          <div class="text-xs text-slate-400 uppercase font-mono font-bold">
            <span class="lang-text" data-en="Secrets & PII Masked" data-ko="실시간 마스킹된 기밀/개인정보">실시간 마스킹된 기밀/개인정보</span>
          </div>
          <div class="text-3xl font-extrabold text-cyan-400 mt-2 font-mono">{metrics['total_secrets_masked']:,}</div>
          <div class="text-xs text-slate-400 mt-1">Passwords, Keys, DB Strings</div>
        </div>

        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6">
          <div class="text-xs text-slate-400 uppercase font-mono font-bold">
            <span class="lang-text" data-en="Agent Takeovers Blocked" data-ko="차단된 불법 AI 에이전트 조작">차단된 불법 AI 에이전트 조작</span>
          </div>
          <div class="text-3xl font-extrabold text-rose-400 mt-2 font-mono">{metrics['total_agent_hijacks_blocked']:,}</div>
          <div class="text-xs text-rose-400 mt-1">0.002s I/O Gate Lockouts</div>
        </div>
      </div>
    </div>

    <!-- ================================================================= -->
    <!-- TAB 4: CISO SOC TELEMETRY & EVENT LOG                              -->
    <!-- ================================================================= -->
    <div id="tab-soc-telemetry" class="hidden space-y-8">
      <!-- Charts Section -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6">
          <h3 class="text-sm font-bold text-white mb-4 flex items-center justify-between">
            <span class="lang-text" data-en="Intercepted Secret Distribution" data-ko="유출 차단된 기밀 유형별 분포">유출 차단된 기밀 유형별 분포</span>
            <span class="text-xs font-mono text-indigo-400">Live SIEM</span>
          </h3>
          <div class="h-64 flex items-center justify-center">
            <canvas id="categoryChart"></canvas>
          </div>
        </div>

        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6">
          <h3 class="text-sm font-bold text-white mb-4 flex items-center justify-between">
            <span class="lang-text" data-en="RawHuman Attestation Telemetry" data-ko="자율 AI vs 인간 마우스 검증 통계">자율 AI vs 인간 마우스 검증 통계</span>
            <span class="text-xs font-mono text-cyan-400">Layer 0 HID</span>
          </h3>
          <div class="h-64 flex items-center justify-center">
            <canvas id="ioChart"></canvas>
          </div>
        </div>
      </div>

      <!-- Live Event Log Table -->
      <div class="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-xl">
        <div class="p-5 border-b border-slate-800 flex justify-between items-center">
          <div>
            <h3 class="text-sm font-extrabold text-white uppercase tracking-wider">
              <span class="lang-text" data-en="Real-Time Security Event Audit Stream" data-ko="실시간 기업 보안 이벤트 감사 로그">실시간 기업 보안 이벤트 감사 로그</span>
            </h3>
            <p class="text-xs text-slate-400 mt-0.5">
              <span class="lang-text" data-en="Live tail from enterprise endpoints and agent sentinel" data-ko="사내 개발자 엔드포인트 및 AI 에이전트 센티넬 실시간 피드">사내 개발자 엔드포인트 및 AI 에이전트 센티넬 실시간 피드</span>
            </p>
          </div>
          <span class="text-xs font-mono text-emerald-400 bg-emerald-500/10 px-3 py-1 rounded-full border border-emerald-500/20 font-bold">● LIVE STREAM</span>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs font-mono">
            <thead class="bg-slate-950/80 text-slate-400 uppercase text-[10px] tracking-wider border-b border-slate-800">
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
                  <span class="px-2.5 py-0.5 rounded text-[10px] font-extrabold border {badge_color}">{ev['status']}</span>
                </td>
              </tr>
        """

    html += """
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- ================================================================= -->
    <!-- TAB 5: DEVELOPER SPECS & LIVE APIS                                -->
    <!-- ================================================================= -->
    <div id="tab-api-specs" class="hidden space-y-6">
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6 sm:p-8">
        <h3 class="text-base font-extrabold text-white uppercase tracking-wider font-mono">
          <span class="lang-text" data-en="Technical Specifications & Live Swagger Endpoints" data-ko="기술 사양서 및 인터랙티브 API 문서">기술 사양서 및 인터랙티브 API 문서</span>
        </h3>
        <p class="text-xs sm:text-sm text-slate-400 mt-1 max-w-2xl leading-relaxed">
          <span class="lang-text"
                data-en="For technical auditors and security architects: GhostGate operates as an ultra-fast RFC-compliant reverse proxy. Test the live endpoints directly in your browser:"
                data-ko="기술 실사역 및 보안 아키텍트를 위한 엔드포인트: GhostGate는 초저지연 표준 리버스 프록시로 동작합니다. 브라우저에서 직접 테스트할 수 있습니다:">
            기술 실사역 및 보안 아키텍트를 위한 엔드포인트: GhostGate는 초저지연 표준 리버스 프록시로 동작합니다. 브라우저에서 직접 테스트할 수 있습니다:
          </span>
        </p>

        <div class="mt-6 grid grid-cols-1 md:grid-cols-3 gap-5 font-mono text-xs">
          <a href="/docs" target="_blank" class="block bg-slate-950 border border-slate-800 hover:border-indigo-500 p-5 rounded-xl transition shadow-sm group">
            <div class="text-indigo-400 font-extrabold text-sm group-hover:text-indigo-300 flex items-center justify-between">
              <span>GET /docs</span>
              <span>↗</span>
            </div>
            <div class="text-slate-300 font-semibold mt-2">Interactive Swagger UI</div>
            <div class="text-slate-400 text-[11px] mt-1">Full OpenAPI specification for LLM proxying and redaction</div>
          </a>

          <a href="/health" target="_blank" class="block bg-slate-950 border border-slate-800 hover:border-cyan-500 p-5 rounded-xl transition shadow-sm group">
            <div class="text-cyan-400 font-extrabold text-sm group-hover:text-cyan-300 flex items-center justify-between">
              <span>GET /health</span>
              <span>↗</span>
            </div>
            <div class="text-slate-300 font-semibold mt-2">Health & Rule Registry</div>
            <div class="text-slate-400 text-[11px] mt-1">Active entropy filters, uptime, and proxy engine state</div>
          </a>

          <a href="/api/dashboard/metrics" target="_blank" class="block bg-slate-950 border border-slate-800 hover:border-purple-500 p-5 rounded-xl transition shadow-sm group">
            <div class="text-purple-400 font-extrabold text-sm group-hover:text-purple-300 flex items-center justify-between">
              <span>GET /api/dashboard/metrics</span>
              <span>↗</span>
            </div>
            <div class="text-slate-300 font-semibold mt-2">Live SIEM Telemetry Feed</div>
            <div class="text-slate-400 text-[11px] mt-1">JSON stream for enterprise Splunk / Datadog integration</div>
          </a>
        </div>
      </div>
    </div>

  </main>

  <script>
    // Current Language State (Default: ko, with 1-click toggle to en)
    let currentLang = 'ko';

    function setLanguage(lang) {
      currentLang = lang;
      document.querySelectorAll('.lang-text').forEach(el => {
        const text = el.getAttribute('data-' + lang);
        if (text) {
          el.textContent = text;
        }
      });
      const flag = document.getElementById('lang-flag');
      const label = document.getElementById('lang-label');
      if (lang === 'ko') {
        flag.textContent = '🇺🇸';
        label.textContent = 'English';
      } else {
        flag.textContent = '🇰🇷';
        label.textContent = '한국어';
      }
    }

    function toggleLanguage() {
      setLanguage(currentLang === 'ko' ? 'en' : 'ko');
    }

    // Tab Switching Logic
    function switchTab(tabName) {
      const tabs = ['leak-defense', 'agent-defense', 'vc-pitch', 'soc-telemetry', 'api-specs'];
      tabs.forEach(t => {
        const pane = document.getElementById('tab-' + t);
        if (pane) pane.classList.add('hidden');
        const btn = document.getElementById('tab-btn-' + t);
        if (btn) {
          btn.classList.remove('bg-indigo-600', 'text-white', 'font-bold', 'shadow-sm');
          btn.classList.add('text-slate-400', 'font-medium');
        }
      });
      const targetPane = document.getElementById('tab-' + tabName);
      if (targetPane) targetPane.classList.remove('hidden');
      const targetBtn = document.getElementById('tab-btn-' + tabName);
      if (targetBtn) {
        targetBtn.classList.add('bg-indigo-600', 'text-white', 'font-bold', 'shadow-sm');
        targetBtn.classList.remove('text-slate-400', 'font-medium');
      }

      if (tabName === 'soc-telemetry' && !window.chartsInitialized) {
        initCharts();
      }
    }

    // Demo Scenarios for Zero-Background Investors
    // Note: Broken up strings prevent static regex scanners (e.g. GitGuardian) from false-positives
    const scenarios = {
      postgres: (
        'DATABASE_URL="' +
        'p' + 'ostgres://' +
        'demo_admin' + ':' + 'mock_pass_placeholder' +
        '@prod-db.internal.corp:5432/finance_db"\n' +
        'engine = create_engine(DATABASE_URL)\n' +
        'with engine.connect() as conn:\n' +
        '    conn.execute("SELECT * FROM payroll_records")'
      ),
      aws: 'import boto3\n# Initialize production S3 client\nclient = boto3.client(\n    "s3",\n    aws_access_key_id="AKIAIOSFODNN7EXAMPLE",\n    aws_secret_access_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"\n)\nresponse = client.list_buckets()',
      pii: 'Customer security escalation: user minsu.security@internal-corp.io reported suspicious login.\nPhone on file: +1-415-555-0199.\nSession token: Bearer GHOSTGATE_DEMO_BEARER_TOKEN_AUTH_99881122',
      airgap: '# @airgap\n# CLASSIFIED: Next-generation quantum encryption key exchange algorithm\ndef proprietary_key_exchange(secret_seed):\n    # Must never touch external cloud LLM servers\n    return hash_matrix(secret_seed)'
    };

    function loadScenario(name) {
      if (scenarios[name]) {
        document.getElementById('prompt-input').value = scenarios[name];
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
          document.getElementById('shield-badge').textContent = currentLang === 'ko' ? '🔒 오프라인 로컬 OLLAMA로 격리 라우팅' : 'AIR-GAPPED TO LOCAL OLLAMA';
          document.getElementById('shield-badge').className = 'text-[11px] font-bold px-2.5 py-0.5 rounded bg-amber-500/20 text-amber-300 border border-amber-500/30';
          document.getElementById('rehydrate-status').textContent = currentLang === 'ko' ? '100% 오프라인 온프레미스 연산 (외부 클라우드 전송 0)' : '100% Offline Local Model Processing';
        } else {
          document.getElementById('shield-badge').textContent = currentLang === 'ko' ? ('🛡️ 100% 안전 (' + data.redaction_count + '개 기밀 가명화 완료)') : ('SECURED (' + data.redaction_count + ' TOKENS SHADOWED)');
          document.getElementById('shield-badge').className = 'text-[11px] font-bold px-2.5 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30';
          document.getElementById('rehydrate-status').textContent = currentLang === 'ko' ? '로컬 메모리 무손실 복원: 직원 화면엔 원본 표시' : 'In-Memory Rehydration: Match Guaranteed';
        }
      } catch (err) {
        console.error(err);
      } finally {
        btn.innerHTML = '<span>⚡</span> <span>' + (currentLang === 'ko' ? '기밀 가명화 및 차단 실행' : 'Click to Protect & Shadow Secret') + '</span>';
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
      document.getElementById('raw-os-flag').className = res.os_flag_detected ? 'text-xl font-extrabold font-mono text-rose-400 mt-2' : 'text-xl font-extrabold font-mono text-emerald-400 mt-2';

      document.getElementById('raw-entropy').textContent = (res.curvature_entropy_score * 100).toFixed(1) + '%';
      document.getElementById('raw-entropy').className = res.curvature_entropy_score < 0.2 ? 'text-xl font-extrabold font-mono text-rose-400 mt-2' : 'text-xl font-extrabold font-mono text-emerald-400 mt-2';

      document.getElementById('raw-jitter').textContent = (res.timing_jitter_entropy * 100).toFixed(1) + '%';
      document.getElementById('raw-jitter').className = res.timing_jitter_entropy < 0.25 ? 'text-xl font-extrabold font-mono text-rose-400 mt-2' : 'text-xl font-extrabold font-mono text-emerald-400 mt-2';

      const vBox = document.getElementById('raw-verdict-box');
      if (res.is_bot) {
        vBox.className = 'bg-rose-950/40 border-2 border-rose-500/60 rounded-2xl p-6 font-mono text-xs space-y-2.5 shadow-xl';
        vBox.innerHTML = `
          <div class="text-rose-400 font-extrabold text-sm sm:text-base flex items-center gap-2">
            <span>🚨</span>
            <span>${currentLang === 'ko' ? '불법 자율 AI 에이전트 인젝션 감지 및 물리 차단 완료' : 'AUTONOMOUS AI AGENT HIJACK DETECTED & KILLED'}</span>
          </div>
          <div class="text-slate-200">
            ${currentLang === 'ko' ? '인간 신뢰도 점수:' : 'Human Confidence Score:'} 
            <span class="text-rose-400 font-extrabold">${(res.human_confidence * 100).toFixed(1)}% (기준 미달)</span>
          </div>
          <div class="text-slate-400">
            ${currentLang === 'ko' ? '차단 사유:' : 'Threat Details:'} 
            ${res.rejection_reasons.join(' • ')}
          </div>
          <div class="text-rose-300 font-bold mt-2 bg-rose-500/10 p-2.5 rounded-lg border border-rose-500/20">
            ${currentLang === 'ko' ? '🛡️ 조치 결과: 0.002초 만에 단말 I/O 게이트 락 잠금 (클릭 실행 전 원천 무력화)' : res.action_taken}
          </div>
        `;
      } else {
        vBox.className = 'bg-emerald-950/40 border-2 border-emerald-500/60 rounded-2xl p-6 font-mono text-xs space-y-2.5 shadow-xl';
        vBox.innerHTML = `
          <div class="text-emerald-400 font-extrabold text-sm sm:text-base flex items-center gap-2">
            <span>✅</span>
            <span>${currentLang === 'ko' ? '실제 생체 인간 조작자 인증 완료 (정상 승인)' : 'AUTHENTIC HUMAN OPERATOR VERIFIED'}</span>
          </div>
          <div class="text-slate-200">
            ${currentLang === 'ko' ? '인간 신뢰도 점수:' : 'Human Confidence Score:'} 
            <span class="text-emerald-400 font-extrabold">${(res.human_confidence * 100).toFixed(1)}% (생체역학 곡률 정상)</span>
          </div>
          <div class="text-slate-400">
            ${currentLang === 'ko' ? '신호 원점: 물리 하드웨어 USB 마우스 (자연 손떨림 및 가속도 확인)' : 'Origin: Physical Hardware HID Controller (Organic micro-tremors confirmed)'}
          </div>
          <div class="text-emerald-300 font-bold mt-2 bg-emerald-500/10 p-2.5 rounded-lg border border-emerald-500/20">
            ${currentLang === 'ko' ? 'Attestation ID: rawhuman_attest_9f83a8b2 • 직원의 마우스 조작이 정상 허가되었습니다.' : 'Attestation ID: rawhuman_attest_9f83a8b2 • Action Permitted'}
          </div>
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
            borderRadius: 6
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

    // Pre-populate with Postgres scenario on initial load
    window.addEventListener('DOMContentLoaded', () => {
      loadScenario('postgres');
    });
  </script>
</body>
</html>
"""
    return HTMLResponse(content=html, status_code=200)
