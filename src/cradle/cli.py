import argparse
import sys
import json
import os
import yaml
from cradle.config import config
from cradle.action import action_manager

def main():
    parser = argparse.ArgumentParser(description="Project Cradle CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Approve command
    approve_parser = subparsers.add_parser("approve", help="Approve a pending action")
    approve_parser.add_argument("id", help="The action ID to approve")

    # Status command
    subparsers.add_parser("status", help="Show Cradle reliability status")

    # Init command
    subparsers.add_parser("init", help="Initialize a default cradle.yml")

    # Daemon command
    daemon_parser = subparsers.add_parser("daemon", help="Manage the standalone Cradle OS daemon")
    daemon_parser.add_argument("action", choices=["start"], help="Start the background OS sentinel")

    args = parser.parse_args()

    if args.command == "approve":
        import asyncio
        result = asyncio.run(action_manager.approve(args.id))
        print(f"✅ Action {args.id} results: {json.dumps(result, indent=2)}")

    elif args.command == "status":
        print("🌌 [Project Cradle] Current Status:")
        print(f"  - Project: {config.get('project')}")
        print(f"  - Model: {config.get('model')}")
        print(f"  - Auto-PR: {config.get('git.auto_pr')}")
        print(f"  - Proactive Monitoring: {config.get('metrics.cpu_threshold')}% CPU Threshold")
        print(f"  - Pending Actions: {len(action_manager.pending_actions)}")

    elif args.command == "init":
        default_yml = {
            "project": "my-app",
            "model": "gpt-4-turbo",
            "action": {
                "require_approval": ["restart", "scale_up"],
                "auto_recover": True
            },
            "metrics": {
                "cpu_threshold": 80.0
            }
        }
        with open("cradle.yml", "w") as f:
            yaml.dump(default_yml, f)
        print("📝 Created default cradle.yml")

    elif args.command == "daemon":
        if args.action == "start":
            print("🌌 [Project Cradle] Starting Standalone OS Daemon Sentinel...")
            import asyncio
            from cradle.core import cradle_agent
            
            async def run_daemon():
                interval = config.get("metrics.interval", 60)
                print(f"🛰️ Daemon is now watching system metrics every {interval}s. Press Ctrl+C to stop.")
                while True:
                    try:
                        await asyncio.sleep(interval)
                        await cradle_agent.check_proactive_reliability(is_background=True, project_override=f"{config.get('project')}-daemon")
                    except asyncio.CancelledError:
                        break
                    except Exception as e:
                        print(f"❌ Daemon Error: {e}")
            
            try:
                asyncio.run(run_daemon())
            except KeyboardInterrupt:
                print("🛑 Daemon stopped.")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
