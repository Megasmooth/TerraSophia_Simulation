import argparse
import pickle
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd

from core.utils.generic import ROOT


def _infer_agent_type(agent_state: dict) -> str:
    system_prompt = agent_state.get("system_prompt", "") or ""
    if "antagonista direto da primeira lição da Jornada" in system_prompt:
        return "SophistPhilosopher"
    if (
        "exclusivamente sustentar a primeira lição da Jornada" in system_prompt
        or "fundação do entendimento" in system_prompt
    ):
        return "SynapsysPhilosopher"
    return agent_state.get("type", "LLMAgent")


def _safe_str(x: Any) -> Optional[str]:
    if x is None:
        return None
    s = str(x)
    if s.strip() == "" or s.strip() in {"<none>", "None", "nan"}:
        return None
    return s


def _extract_messages(
    ckpt_agents: Dict[str, dict], timestep: int
) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for agent_id, agent_state in ckpt_agents.items():
        history = agent_state.get("history", []) or []
        agent_type = _infer_agent_type(agent_state)

        # Each history entry is "Step {i}" in the agent's own rolling window.
        # Map those entries to an approximate environment timestep using the checkpoint ts.
        # If max_history=1, the last action happened at timestep-1.
        L = len(history)
        for idx, entry in enumerate(history):
            if not isinstance(entry, (list, tuple)) or len(entry) < 3:
                continue
            _past_obs, past_action, past_msg = entry[0], entry[1], entry[2]

            # Oldest -> earliest, newest -> latest (relative to checkpoint time).
            mapped_ts = timestep - (L - idx)

            rows.append(
                {
                    "Timestep": mapped_ts,
                    "Agent_ID": agent_id,
                    "Agent_Type": agent_type,
                    "Message_Content": _safe_str(past_msg),
                    "Action_Taken": _safe_str(past_action),
                }
            )
    return rows


def _extract_artifacts(
    env_state: dict, timestep_fallback: int
) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    artifacts_serial = env_state.get("artifacts", {}) or {}
    expired_serial = env_state.get("expired_artifacts", []) or []

    def iter_artifacts(serial_val: Any):
        if isinstance(serial_val, dict):
            # env_state["artifacts"] is a dict name -> serialized artifact
            yield from serial_val.values()
        elif isinstance(serial_val, list):
            yield from serial_val

    all_artifacts = list(iter_artifacts(artifacts_serial)) + list(
        iter_artifacts(expired_serial)
    )

    for art in all_artifacts:
        if not isinstance(art, dict):
            continue
        if art.get("__type__") != "artifact":
            continue
        data = art.get("data", {}) or {}

        pose = data.get("pose")
        if not isinstance(pose, (list, tuple)) or len(pose) != 2:
            pos_x, pos_y = None, None
        else:
            pos_x, pos_y = pose[0], pose[1]

        creation_time = data.get("creation_time", None)
        try:
            creation_ts = int(creation_time)
        except Exception:
            creation_ts = timestep_fallback

        rows.append(
            {
                "Timestep": creation_ts,
                "Creator_ID": data.get("creator_tag"),
                "Position_X": pos_x,
                "Position_Y": pos_y,
                "Artifact_Text": _safe_str(data.get("payload")),
            }
        )

    return rows


def _extract_energy_economy(env_state: dict) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    logger_data = env_state.get("logger_data", None) or None
    if not isinstance(logger_data, dict):
        return rows

    for donor_id, donor_info in logger_data.items():
        if not isinstance(donor_info, dict):
            continue
        gift_events = donor_info.get("gift", []) or []
        if not isinstance(gift_events, list):
            continue

        for ev in gift_events:
            if not isinstance(ev, dict):
                continue
            rows.append(
                {
                    "Timestep": ev.get("time"),
                    "Donor_ID": donor_id,
                    "Recipient_ID": ev.get("target_tag"),
                    "Energy_Amount": ev.get("amount"),
                }
            )
    return rows


def main():
    parser = argparse.ArgumentParser(
        description="Extract philosophical logs from TerraLingua experiment checkpoints."
    )
    parser.add_argument(
        "--exp_name",
        required=True,
        help="Experiment name, e.g. TerraSophia_Jornada",
    )
    args = parser.parse_args()

    exp_dir = ROOT / "logs" / args.exp_name
    if not exp_dir.exists():
        raise FileNotFoundError(f"Experiment directory not found: {exp_dir}")

    pkl_paths = sorted(exp_dir.rglob("*.pkl"))
    if not pkl_paths:
        raise FileNotFoundError(f"No .pkl files found under: {exp_dir}")

    all_messages: List[Dict[str, Any]] = []
    all_artifacts: List[Dict[str, Any]] = []
    all_energy: List[Dict[str, Any]] = []

    for pkl_path in pkl_paths:
        with open(pkl_path, "rb") as f:
            ckpt = pickle.load(f)

        timestep = ckpt.get("ts", None)
        env_state = ckpt.get("env", {}) or {}
        if timestep is None:
            timestep = env_state.get("step_count", 0) or 0
        try:
            timestep = int(timestep)
        except Exception:
            timestep = 0

        ckpt_agents = ckpt.get("agents", {}) or {}
        all_messages.extend(_extract_messages(ckpt_agents=ckpt_agents, timestep=timestep))
        all_artifacts.extend(_extract_artifacts(env_state=env_state, timestep_fallback=timestep))
        all_energy.extend(_extract_energy_economy(env_state=env_state))

    out_messages = exp_dir / "1_mensagens_agentes.csv"
    out_artifacts = exp_dir / "2_artefatos_criados.csv"
    out_energy = exp_dir / "3_economia_energia.csv"

    pd.DataFrame(all_messages, columns=["Timestep", "Agent_ID", "Agent_Type", "Message_Content", "Action_Taken"]).to_csv(
        out_messages, index=False
    )
    pd.DataFrame(all_artifacts, columns=["Timestep", "Creator_ID", "Position_X", "Position_Y", "Artifact_Text"]).to_csv(
        out_artifacts, index=False
    )
    pd.DataFrame(all_energy, columns=["Timestep", "Donor_ID", "Recipient_ID", "Energy_Amount"]).to_csv(
        out_energy, index=False
    )

    print(f"Saved: {out_messages}")
    print(f"Saved: {out_artifacts}")
    print(f"Saved: {out_energy}")


if __name__ == "__main__":
    main()

