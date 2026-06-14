import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MCP = ROOT / "mcp" / "wiki_mcp_server.py"
PROMPT_DIR = ROOT / "agent_messages" / "prompts"
sys.stdin.reconfigure(encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")


def call_tool(name, arguments):
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {"name": name, "arguments": arguments},
    }
    proc = subprocess.run(
        [sys.executable, str(MCP)],
        input=json.dumps(request, ensure_ascii=False),
        text=True,
        capture_output=True,
        encoding="utf-8",
        cwd=str(ROOT),
        check=False,
    )
    payload = json.loads(proc.stdout)
    if "error" in payload:
        raise RuntimeError(payload["error"]["message"])
    return payload["result"]


def build_prompt(question, wiki_context):
    sources = wiki_context.get("sources", [])
    source_text = "\n\n".join(
        f"[{item['slug']}] {item['title']}\n{item['snippet']}"
        for item in sources
    ) or "직접 매칭된 Wiki page가 없습니다."

    source_slugs = ", ".join(item["slug"] for item in sources) or "없음"

    return f"""아래 사용자 메시지에 대해, 채팅 말풍선에 바로 들어갈 자연스러운 한국어 답변만 작성하세요.

스타일:
- 이미지 예시처럼 친근하지만 간결한 Wiki 에이전트 톤으로 답하세요.
- "답변:", "위키 근거:", "유지보수 제안:" 같은 고정 라벨을 붙이지 마세요.
- 사용자가 유지보수/수정/검토를 요청하지 않았다면 유지보수 제안을 하지 마세요.
- 필요한 경우에만 Markdown을 쓰세요. 예: **굵게**, 짧은 bullet, `용어`.
- 마지막에는 Wiki 근거가 있을 때만 한 줄로 붙이세요.
  예: 📍 **위키 출처**: [model-compression] 페이지
- Wiki 근거가 없으면 출처 줄을 붙이지 마세요.
- 영어로 답하지 마세요. "Understood", "I'll answer" 같은 지시 수락 문장을 절대 출력하지 마세요.

대화 규칙:
- 인사에는 짧게 인사하고 머신러닝 Wiki 질문을 유도하세요.
- 사용자가 당신이 누구인지 물으면 "저는 Codex CLI와 MCP Wiki Tool에 연결된 ML Wiki Agent입니다."라고 답하세요.
- 사용자가 자기 이름이나 신원을 물으면 현재 대화 정보만으로는 알 수 없다고 답하세요.
- 머신러닝 또는 Wiki 질문이면 아래 Wiki 근거를 우선 사용하세요.
- 오타가 명확하면 자연스럽게 보정해서 답하세요. 예: transfoemer -> Transformer.
- 최신 동향을 물으면 Wiki 근거에서 확인되는 내용과 일반적 방향을 구분해서 말하세요. 모르는 것을 확정하지 마세요.

사용자 메시지:
{question}

사용 가능한 Wiki 근거 slug:
{source_slugs}

Wiki 근거 본문:
{source_text}

이제 최종 채팅 답변만 작성하세요.
"""


def write_prompt_file(prompt):
    PROMPT_DIR.mkdir(parents=True, exist_ok=True)
    prompt_file = PROMPT_DIR / f"prompt-{int(time.time() * 1000)}.md"
    prompt_file.write_text(prompt, encoding="utf-8")
    return prompt_file


def run_cli_agent(prompt):
    if os.environ.get("WIKI_AGENT_DISABLE_CLI") == "1":
        return None

    prompt_file = write_prompt_file(prompt)
    command_template = os.environ.get("WIKI_AGENT_CLI", "").strip()
    enable_default_codex = os.environ.get("WIKI_AGENT_ENABLE_CODEX_CLI") == "1"
    timeout_seconds = float(os.environ.get("WIKI_AGENT_CLI_TIMEOUT", "8"))

    try:
        file_instruction = f"다음 UTF-8 파일의 지시를 읽고 최종 채팅 답변만 출력하세요: {prompt_file}"

        if not command_template and enable_default_codex and shutil.which("codex"):
            return subprocess.run(
                [
                    "codex",
                    "exec",
                    "--skip-git-repo-check",
                    "--sandbox",
                    "read-only",
                    file_instruction,
                ],
                text=True,
                capture_output=True,
                encoding="utf-8",
                cwd=str(ROOT),
                timeout=timeout_seconds,
                check=False,
            )

        if not command_template:
            return None

        if "{prompt_file}" in command_template:
            command = command_template.replace("{prompt_file}", str(prompt_file))
        elif "{prompt}" in command_template:
            command = command_template.replace("{prompt}", file_instruction.replace('"', '\\"'))
        else:
            command = command_template

        return subprocess.run(
            command,
            input=prompt,
            text=True,
            capture_output=True,
            encoding="utf-8",
            cwd=str(ROOT),
            shell=True,
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        return subprocess.CompletedProcess(
            args=exc.cmd,
            returncode=124,
            stdout=exc.stdout or "",
            stderr=f"CLI agent timed out after {timeout_seconds:g} seconds.",
        )
    finally:
        prompt_file.unlink(missing_ok=True)


def clean_cli_output(text):
    text = re.sub(r"\x1b\[[0-9;]*m", "", text.strip())
    if "\ncodex\n" in text:
        text = text.split("\ncodex\n", 1)[1]
    if "\ntokens used\n" in text:
        text = text.split("\ntokens used\n", 1)[0]
    text = text.strip()
    text = re.sub(r"^(답변|위키 근거|유지보수 제안)\s*:\s*", "", text)
    return text.strip()


def main():
    question = " ".join(sys.argv[1:]).strip() or sys.stdin.read().strip()
    wiki_context = call_tool("ask_wiki", {"question": question})
    prompt = build_prompt(question, wiki_context)
    cli_result = run_cli_agent(prompt)

    if cli_result and cli_result.returncode == 0 and cli_result.stdout.strip():
        result = {
            "answer": clean_cli_output(cli_result.stdout),
            "sources": wiki_context.get("sources", []),
            "agent_mode": "codex-cli",
            "model": "Configured by the user's Codex CLI profile",
        }
    else:
        result = {
            **wiki_context,
            "agent_mode": "mcp-fallback",
            "model": "No local model; fallback uses MCP Wiki search context",
        }
        if cli_result and cli_result.stderr:
            result["cli_error"] = cli_result.stderr.strip()[-800:]

    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
