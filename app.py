import argparse
import json
import logging
import random
import re
import sys
from faker import Faker
from typing import Dict, Any
from fastmcp import FastMCP

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger(__name__)

def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for the MCP server."""
    parser = argparse.ArgumentParser(description="MCP Server for RPG Assistant")
    parser.add_argument(
        '--transport',
        choices=['stdio', 'http'],
        default='stdio',
        help='Transport protocol for the MCP server'
    )
    parser.add_argument(
        '--host',
        default='127.0.0.1',
        help='Host for HTTP transport'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=8080,
        help='Port for HTTP transport'
    )
    return parser.parse_args()

# Initialize MCP server
mcp = FastMCP("RPG Assistant")
logger.info("Initialized MCP server: RPG Assistant")

@mcp.tool()
def check_success(probability: int = 80, critical_success: int = 5, critical_failure: int = None) -> str:
    """
    Check for success based on a given probability and optional critical success/failure rates.
    Returns 'critical success', 'success', 'failure', or 'critical failure'.
    Args:
        probability: The chance of success in percentage (1-100), defaults to 80.
        critical_success: The top percentage for critical success (0-50), defaults to 5.
        critical_failure: The bottom percentage for critical failure (0-50), defaults to critical_success.
    """
    try:
        if not isinstance(probability, int) or not (0 <= probability <= 100):
            logger.warning("Invalid probability: %s", probability)
            return "Error: Probability must be an integer between 0 and 100."

        # default failure rate to success rate if not provided
        if critical_failure is None:
            critical_failure = critical_success
            
        if not isinstance(critical_success, int) or not (0 <= critical_success <= 50):
            logger.warning("Invalid critical_success: %s", critical_success)
            return "Error: Critical success must be an integer between 0 and 50."
        if not isinstance(critical_failure, int) or not (0 <= critical_failure <= 50):
            logger.warning("Invalid critical_failure: %s", critical_failure)
            return "Error: Critical failure must be an integer between 0 and 50."

        roll = random.randint(1, 100)
        logger.debug(
            "Roll: %d, Probability: %d, CritSuccess: %d, CritFailure: %d",
            roll, probability, critical_success, critical_failure
        )

        # check critical failure first
        if critical_failure > 0 and roll <= critical_failure:
            return f"Rolled {roll}: Critical Failure!"
        # then critical success
        if critical_success > 0 and roll >= (101 - critical_success):
            return f"Rolled {roll}: Critical Success!"

        # normal success/failure
        if roll <= probability:
            return f"Rolled {roll}: Success!"
        return f"Rolled {roll}: Failure!"
    except Exception as e:
        logger.error("Error in check_success: %s", e)
        return f"Error: {str(e)}"

@mcp.tool()
def roll_dice(expr: str) -> str:
    """
    Roll dice using standard RPG notation (e.g., '1d6', '2d8+3').
    Args:
        expr: Dice expression in the format 'NdM[+/-]K' (e.g., '2d6', '1d20+4').
    """
    try:
        expr = expr.strip()
        m = re.fullmatch(r'(\d+)d(\d+)([+-]\d+)?', expr)
        if not m:
            logger.warning("Invalid dice expression: %s", expr)
            return f"Invalid dice expression: {expr}. Use format like '2d6' or '1d20+4'."

        count, sides, mod = int(m[1]), int(m[2]), int(m[3] or 0)
        if count < 1 or sides < 1:
            logger.warning("Invalid dice parameters: count=%d, sides=%d", count, sides)
            return "Error: Dice count and sides must be positive integers."

        rolls = [random.randint(1, sides) for _ in range(count)]
        total = sum(rolls) + mod
        mod_str = f"{mod:+d}" if mod else ""
        logger.debug("Dice roll: %s -> %s%s = %d", expr, rolls, mod_str, total)
        return f"Rolling {expr}: {rolls}{mod_str} = {total}"
    except Exception as e:
        logger.error("Error in roll_dice: %s", e)
        return f"Error: {str(e)}"

@mcp.tool()
def generate_event() -> str:
    """
    Generate a random RPG event based on subjects, actions, and objects.
    Should be called every time a new event occures and interpreted loosely.
    
    Returns a string describing the event.
    """
    try:
        subjects = [
            # Positive objects
            "Hope", "Desire", "Opportunity", "Knowledge", "Joy", "Trust",
            "Wealth", "Power", "Health", "Wisdom", "Courage",
            # Neutral objects
            "Mystery", "Change", "Choice", "Action", "Surprise", "Balance",
            "Harmony", "Unity", "Creativity", "Innovation", "Exploration",
            # Negative objects
            "Challenge", "Danger", "Conflict", "Fear", "Greed", "Despair",
            "Loss", "Pain", "Lies", "Deceit", "Betrayal"
        ]
        actions = [
            "%s increases", "%s decreases",
            "Attention shifts away from %s", "Attention is drawn towards %s",
            "Meaning of %s is revealed", "Meaning of %s is obscured",
            "Opportunity for %s appears", "Opportunity for %s vanishes",
            "Conflict arises through %s", "Conflict subsides through %s",
            "Support emerges through %s", "%s inspires action"
        ]
        objects = [
            "for player in a positive way", "for player in a negative way",
            "for a new NPC", "for an NPC taking action",
            "as a positive event towards NPC", "as a negative event towards NPC",
            "as a positive setting detail", "as a negative setting detail"
        ]

        sub = random.choice(subjects)
        act = random.choice(actions)
        obj = random.choice(objects)
        event = f"{act % sub} {obj}."
        logger.debug("Generated event: %s", event)
        return event
    except Exception as e:
        logger.error("Error in generate_event: %s", e)
        return f"Error: {str(e)}"

@mcp.tool()
def generate_name(count: int = 1, gender: str = "random", locale: str = "en_US") -> str:
    """
    Generate random modern names.
    Args:
        count: Number of names to generate (default: 1).
        gender: Gender for names - 'male', 'female', or 'random' (default: 'random').
        locale: Locale code for nationality of names - 'en_US', 'es_ES', 'fr_FR', 'de_DE', 'ja_JP',
                'zh_CN', 'ar_SA', 'ru_RU', etc. (default: 'en_US').
    """
    try:
        # Validate inputs
        if not isinstance(count, int) or count < 1:
            logger.warning("Invalid count: %s", count)
            return "Error: Count must be a positive integer."

        gender = gender.lower()
        if gender not in ["male", "female", "random"]:
            logger.warning("Invalid gender: %s", gender)
            return "Error: Gender must be 'male', 'female', or 'random'."

        try:
            fake = Faker(locale)
        except AttributeError:
            logger.warning("Invalid locale: %s", locale)
            return f"Error: Invalid locale '{locale}'. Using default 'en_US'."

        # Generate names
        results = []
        for _ in range(count):
            # Determine gender for this name
            current_gender = gender if gender != "random" else random.choice(["male", "female"])

            # Generate name based on gender
            if current_gender == "male":
                full_name = fake.name_male()
            else:
                full_name = fake.name_female()

            results.append(full_name)

        # Format output
        if count == 1:
            output = results[0]
        else:
            output = "\n".join(f"{i+1}. {name}" for i, name in enumerate(results))

        logger.debug("Generated %d name(s) - Gender: %s, Locale: %s", count, gender, locale)
        return output

    except Exception as e:
        logger.error("Error in generate_name: %s", e)
        return f"Error: {str(e)}"

@mcp.tool()
def generate_address(count: int = 1, locale: str = "en_US") -> str:
    """
    Generate random addresses.
    Args:
        count: Number of addresses to generate (default: 1).
        locale: Locale code for addresses - 'en_US', 'es_ES', 'fr_FR', 'de_DE', 'ja_JP',
                'zh_CN', 'ar_SA', 'ru_RU', etc. (default: 'en_US').
    """
    try:
        # Validate inputs
        if not isinstance(count, int) or count < 1:
            logger.warning("Invalid count: %s", count)
            return "Error: Count must be a positive integer."

        # Initialize Faker with specified locale
        try:
            fake = Faker(locale)
        except AttributeError:
            logger.warning("Invalid locale: %s", locale)
            return f"Error: Invalid locale '{locale}'. Using default 'en_US'."

        # Generate addresses
        results = []
        for _ in range(count):
            address = fake.address()
            results.append(address)

        # Format output
        if count == 1:
            output = results[0]
        else:
            output = "\n\n".join(f"{i+1}. {addr}" for i, addr in enumerate(results))

        logger.debug("Generated %d address(es) - Locale: %s", count, locale)
        return output

    except Exception as e:
        logger.error("Error in generate_address: %s", e)
        return f"Error: {str(e)}"

def main():
    """Main entry point for the MCP server."""
    args = parse_args()
    try:
        if args.transport == 'stdio':
            logger.info("Starting MCP server with STDIO transport")
            mcp.run()
        else:
            logger.info("Starting MCP server with HTTP transport on %s:%d", args.host, args.port)
            mcp.run(transport="http", host=args.host, port=args.port)
    except KeyboardInterrupt:
        logger.info("Shutting down MCP server")
    except Exception as e:
        logger.error("Failed to start MCP server: %s", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
