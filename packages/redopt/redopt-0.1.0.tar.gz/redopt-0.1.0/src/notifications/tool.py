"""
Slack notification tool for AI agents.
"""

import logging
import os
from typing import Any, Dict

from agents import function_tool

from ..config import Config
from .slack import SlackNotifier

logger = logging.getLogger(__name__)

# Global notifier instance
_notifier: SlackNotifier = None


def get_slack_notifier() -> SlackNotifier:
    """Get the global Slack notifier instance."""
    global _notifier
    if _notifier is None:
        config = Config.from_env()
        # Try config first, then fall back to environment variable
        token = config.slack_webhook_token or os.getenv("PERFORMANCE_WH_TOKEN")
        _notifier = SlackNotifier(token)
    return _notifier


@function_tool
def send_slack_notification(
    message: str,
    channel: str = "#perf-ci",
    alert_type: str = "info"
) -> Dict[str, Any]:
    """
    Send a general notification message to Slack (NOT for PR analysis).

    Use send_pr_analysis_summary() for PR-related notifications to get action buttons.

    Args:
        message: The message to send to Slack
        channel: The Slack channel to send to (default: #perf-ci)
        alert_type: Type of alert - 'info', 'warning', 'error', 'success' (default: info)

    Returns:
        Dictionary with success status and details
    """
    notifier = get_slack_notifier()
    
    if not notifier.is_configured():
        return {
            "success": False,
            "error": "Slack webhook not configured. Set PERFORMANCE_WH_TOKEN environment variable."
        }
    
    # Choose appropriate emoji and username based on alert type
    emoji_map = {
        "info": ":information_source:",
        "warning": ":warning:",
        "error": ":x:",
        "success": ":white_check_mark:",
        "performance": ":chart_with_downwards_trend:"
    }
    
    username_map = {
        "info": "RedOpt AI",
        "warning": "RedOpt AI - Warning",
        "error": "RedOpt AI - Error",
        "success": "RedOpt AI - Success",
        "performance": "RedOpt AI - Performance Alert"
    }
    
    emoji = emoji_map.get(alert_type, ":robot_face:")
    username = username_map.get(alert_type, "RedOpt AI")
    
    try:
        success = notifier.send_message(
            message=message,
            channel=channel,
            username=username,
            icon_emoji=emoji
        )
        
        if success:
            return {
                "success": True,
                "message": f"Notification sent successfully to {channel}",
                "channel": channel,
                "alert_type": alert_type
            }
        else:
            return {
                "success": False,
                "error": "Failed to send notification to Slack"
            }
            
    except Exception as e:
        logger.error(f"Error in send_slack_notification: {e}")
        return {
            "success": False,
            "error": f"Exception occurred: {str(e)}"
        }


@function_tool
def send_performance_alert(
    pr_url: str,
    impact_percentage: float,
    affected_commands: str,
    details: str,
    functions_changed: str = ""
) -> Dict[str, Any]:
    """
    Send a performance impact alert to Slack for significant PR changes.

    Args:
        pr_url: URL of the GitHub PR
        impact_percentage: Estimated performance impact percentage
        affected_commands: Comma-separated list of affected Redis commands
        details: Additional details about the performance impact
        functions_changed: Optional comma-separated list of changed functions

    Returns:
        Dictionary with success status and details
    """
    notifier = get_slack_notifier()

    if not notifier.is_configured():
        return {
            "success": False,
            "error": "Slack webhook not configured. Set PERFORMANCE_WH_TOKEN environment variable."
        }

    try:
        # Parse affected commands and add context about functions if provided
        commands_list = [cmd.strip() for cmd in affected_commands.split(",") if cmd.strip()]

        # Add functions changed to details if provided
        enhanced_details = details
        if functions_changed:
            functions_list = [func.strip() for func in functions_changed.split(",") if func.strip()]
            if functions_list:
                functions_str = ", ".join(f"`{func}`" for func in functions_list[:5])
                if len(functions_list) > 5:
                    functions_str += f" and {len(functions_list) - 5} more"
                enhanced_details = f"**Functions Changed:** {functions_str}\n\n{details}"

        success = notifier.send_performance_alert(
            pr_url=pr_url,
            impact_percentage=impact_percentage,
            affected_commands=commands_list,
            details=enhanced_details
        )

        if success:
            return {
                "success": True,
                "message": f"Performance alert sent for PR {pr_url}",
                "impact_percentage": impact_percentage,
                "affected_commands": commands_list
            }
        else:
            return {
                "success": False,
                "error": "Failed to send performance alert to Slack"
            }

    except Exception as e:
        logger.error(f"Error in send_performance_alert: {e}")
        return {
            "success": False,
            "error": f"Exception occurred: {str(e)}"
        }


@function_tool
def send_pr_analysis_summary(
    pr_url: str,
    summary: str,
    impact_level: str = "low",
    affected_commands: str = "",
    functions_changed: str = ""
) -> Dict[str, Any]:
    """
    Send a comprehensive PR analysis summary to Slack with repository context and ACTION BUTTONS.

    ALWAYS use this function for PR analysis notifications instead of send_slack_notification.
    Includes interactive buttons for JIRA, GitHub comments (Redis only), and benchmarks.

    Args:
        pr_url: URL of the GitHub PR
        summary: Detailed analysis summary
        impact_level: Impact level - 'low', 'medium', or 'high'
        affected_commands: Comma-separated list of affected Redis commands
        functions_changed: Comma-separated list of changed functions

    Returns:
        Dictionary with success status and details
    """
    notifier = get_slack_notifier()

    if not notifier.is_configured():
        return {
            "success": False,
            "error": "Slack webhook not configured. Set PERFORMANCE_WH_TOKEN environment variable."
        }

    try:
        # Parse affected commands and functions
        commands_list = [cmd.strip() for cmd in affected_commands.split(",") if cmd.strip()]
        functions_list = [func.strip() for func in functions_changed.split(",") if func.strip()]

        success = notifier.send_analysis_summary(
            pr_url=pr_url,
            summary=summary,
            impact_level=impact_level,
            affected_commands=commands_list if commands_list else None,
            functions_changed=functions_list if functions_list else None
        )

        if success:
            return {
                "success": True,
                "message": f"PR analysis summary sent for {pr_url}",
                "impact_level": impact_level,
                "affected_commands": commands_list,
                "functions_changed": functions_list
            }
        else:
            return {
                "success": False,
                "error": "Failed to send PR analysis summary to Slack"
            }

    except Exception as e:
        logger.error(f"Error in send_pr_analysis_summary: {e}")
        return {
            "success": False,
            "error": f"Exception occurred: {str(e)}"
        }
