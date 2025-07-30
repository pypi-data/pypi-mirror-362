"""
Slack notification service for RedOpt AI.
"""

import json
import logging
import re
import urllib.parse
import urllib.request
from typing import Optional, Tuple

logger = logging.getLogger(__name__)


class SlackNotifier:
    """Service for sending notifications to Slack via webhook."""
    
    def __init__(self, webhook_token: Optional[str] = None):
        """
        Initialize the Slack notifier.
        
        Args:
            webhook_token: Slack webhook token (without the base URL)
        """
        self.webhook_token = webhook_token
        self.base_url = "https://hooks.slack.com/services"
    
    def is_configured(self) -> bool:
        """Check if Slack notifications are properly configured."""
        return self.webhook_token is not None

    def _extract_repo_info(self, pr_url: str) -> Tuple[str, str, str, str]:
        """
        Extract repository information from a GitHub/GitLab PR URL.

        Args:
            pr_url: URL of the pull request

        Returns:
            Tuple of (owner, repo, pr_number, repo_display_name)
        """
        # Match GitHub URLs like https://github.com/redis/redis/pull/14200
        github_match = re.match(r'https://github\.com/([^/]+)/([^/]+)/pull/(\d+)', pr_url)
        if github_match:
            owner, repo, pr_number = github_match.groups()
            repo_display_name = f"{owner}/{repo}"
            return owner, repo, pr_number, repo_display_name

        # Match GitLab/Valkey URLs like https://github.com/valkey-io/valkey/pull/2300
        valkey_match = re.match(r'https://github\.com/([^/]+)/([^/]+)/pull/(\d+)', pr_url)
        if valkey_match:
            owner, repo, pr_number = valkey_match.groups()
            repo_display_name = f"{owner}/{repo}"
            return owner, repo, pr_number, repo_display_name

        # Fallback for other URLs
        url_parts = pr_url.split('/')
        if len(url_parts) >= 5:
            owner = url_parts[-4] if len(url_parts) > 4 else "unknown"
            repo = url_parts[-3] if len(url_parts) > 3 else "unknown"
            pr_number = url_parts[-1] if url_parts[-1].isdigit() else "unknown"
            repo_display_name = f"{owner}/{repo}"
            return owner, repo, pr_number, repo_display_name

        return "unknown", "unknown", "unknown", "unknown"

    def _create_action_buttons(self, pr_url: str, repo_display_name: str, pr_number: str) -> list:
        """
        Create action buttons for PR notifications.

        Args:
            pr_url: URL of the pull request
            repo_display_name: Repository name in format owner/repo
            pr_number: PR number

        Returns:
            List of Slack attachment with action buttons
        """
        # Check if this is a Redis repository
        is_redis_repo = "redis/redis" in repo_display_name.lower()

        # Base actions available for all repositories
        actions = [
            {
                "type": "button",
                "text": "📋 Create JIRA Task",
                "name": "create_jira",
                "value": f"jira:{pr_url}",
                "style": "primary",
                "url": f"https://your-jira-instance.atlassian.net/secure/CreateIssue.jspa?summary=Performance%20Review:%20{repo_display_name}%20PR%20{pr_number}&description=Review%20performance%20impact%20of%20{pr_url}"
            },
            {
                "type": "button",
                "text": "🚀 Trigger Benchmark",
                "name": "trigger_benchmark",
                "value": f"benchmark:{pr_url}",
                "style": "default",
                "url": f"https://your-ci-system.com/trigger-benchmark?pr={pr_url}"
            }
        ]

        # Add GitHub comment button for Redis repositories
        if is_redis_repo:
            actions.insert(1, {
                "type": "button",
                "text": "💬 Comment on PR",
                "name": "comment_pr",
                "value": f"comment:{pr_url}",
                "style": "default",
                "url": f"{pr_url}#issuecomment-new"
            })

        return [{
            "fallback": f"Actions for {repo_display_name} PR #{pr_number}",
            "color": "#36a64f",
            "attachment_type": "default",
            "actions": actions
        }]
    
    def send_message(
        self,
        message: str,
        channel: str = "#perf-ci",
        username: str = "RedOpt AI",
        icon_emoji: str = ":robot_face:",
        attachments: Optional[list] = None
    ) -> bool:
        """
        Send a message to Slack.

        Args:
            message: The message to send
            channel: The Slack channel (default: #perf-ci)
            username: The username to display (default: RedOpt AI)
            icon_emoji: The emoji icon to use (default: :robot_face:)
            attachments: Optional list of Slack attachments for interactive elements

        Returns:
            True if message was sent successfully, False otherwise
        """
        if not self.is_configured():
            logger.warning("Slack webhook not configured - message not sent")
            return False
        
        # Construct webhook URL
        webhook_url = f"{self.base_url}/{self.webhook_token}"
        
        # Prepare the payload
        payload = {
            "channel": channel,
            "text": message,
            "username": username,
            "icon_emoji": icon_emoji
        }

        # Add attachments if provided
        if attachments:
            payload["attachments"] = attachments
        
        try:
            # Convert payload to JSON
            data = json.dumps(payload).encode('utf-8')
            
            # Create request
            req = urllib.request.Request(
                webhook_url,
                data=data,
                headers={'Content-Type': 'application/json'}
            )
            
            # Send request
            with urllib.request.urlopen(req) as response:
                if response.status == 200:
                    logger.info(f"Message sent successfully to {channel}")
                    return True
                else:
                    logger.error(f"Failed to send message. Status: {response.status}")
                    return False
                    
        except Exception as e:
            logger.error(f"Error sending message to Slack: {e}")
            return False
    
    def send_performance_alert(
        self,
        pr_url: str,
        impact_percentage: float,
        affected_commands: list,
        details: str
    ) -> bool:
        """
        Send a performance impact alert to Slack.

        Args:
            pr_url: URL of the GitHub PR
            impact_percentage: Estimated performance impact percentage
            affected_commands: List of affected Redis commands
            details: Additional details about the impact

        Returns:
            True if alert was sent successfully, False otherwise
        """
        # Extract repository information
        owner, repo, pr_number, repo_display_name = self._extract_repo_info(pr_url)

        # Format the affected commands
        commands_str = ", ".join(affected_commands[:5])  # Limit to first 5 commands
        if len(affected_commands) > 5:
            commands_str += f" and {len(affected_commands) - 5} more"

        # Create a more detailed alert message with better formatting
        alert_message = f"""🚨 **Performance Impact Alert**

**Repository:** `{repo_display_name}`
**Pull Request:** <{pr_url}|#{pr_number}>
**Estimated Impact:** {impact_percentage:.1f}%
**Affected Commands:** `{commands_str}`

**Analysis Details:**
{details}

⚠️ This PR may have significant performance implications. Please review carefully.

**Actions:**
• Review the PR: {pr_url}
• Check performance benchmarks
• Consider impact on production workloads"""

        # Create action buttons
        action_buttons = self._create_action_buttons(pr_url, repo_display_name, pr_number)

        return self.send_message(
            message=alert_message,
            channel="#perf-ci",
            username="RedOpt AI - Performance Alert",
            icon_emoji=":warning:",
            attachments=action_buttons
        )
    
    def send_analysis_summary(
        self,
        pr_url: str,
        summary: str,
        impact_level: str = "low",
        affected_commands: Optional[list] = None,
        functions_changed: Optional[list] = None
    ) -> bool:
        """
        Send a PR analysis summary to Slack.

        Args:
            pr_url: URL of the GitHub PR
            summary: Analysis summary
            impact_level: Impact level (low, medium, high)
            affected_commands: Optional list of affected commands
            functions_changed: Optional list of changed functions

        Returns:
            True if summary was sent successfully, False otherwise
        """
        # Extract repository information
        owner, repo, pr_number, repo_display_name = self._extract_repo_info(pr_url)

        # Choose emoji based on impact level
        emoji_map = {
            "low": ":white_check_mark:",
            "medium": ":warning:",
            "high": ":rotating_light:"
        }
        emoji = emoji_map.get(impact_level, ":information_source:")

        # Format affected commands if provided
        commands_section = ""
        if affected_commands and len(affected_commands) > 0:
            commands_str = ", ".join(f"`{cmd}`" for cmd in affected_commands[:5])
            if len(affected_commands) > 5:
                commands_str += f" and {len(affected_commands) - 5} more"
            commands_section = f"\n**Affected Commands:** {commands_str}"

        # Format changed functions if provided
        functions_section = ""
        if functions_changed and len(functions_changed) > 0:
            functions_str = ", ".join(f"`{func}`" for func in functions_changed[:5])
            if len(functions_changed) > 5:
                functions_str += f" and {len(functions_changed) - 5} more"
            functions_section = f"\n**Functions Changed:** {functions_str}"

        message = f"""{emoji} **PR Analysis: {repo_display_name}#{pr_number}**

**Repository:** `{repo_display_name}`
**Pull Request:** <{pr_url}|#{pr_number}>
**Impact Level:** {impact_level.upper()}{commands_section}{functions_section}

**Analysis Summary:**
{summary}

**View PR:** {pr_url}"""

        # Create action buttons
        action_buttons = self._create_action_buttons(pr_url, repo_display_name, pr_number)

        return self.send_message(
            message=message,
            channel="#perf-ci",
            username="RedOpt AI - Analysis",
            icon_emoji=":mag:",
            attachments=action_buttons
        )
