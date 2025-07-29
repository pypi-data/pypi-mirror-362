import os 
import asyncio
import sys
import logging

logger = logging.getLogger(__name__)

def main():
    import argparse
    from .server import start_server
    from .feature_facade import FeatureFacade, set_feature_facade_instance
    from .explore_runner import run_exploration_from_file

    parser = argparse.ArgumentParser(description="Local AI QA Agent CLI. Supports both prompt-based and script-based exploration configs.")
    parser.add_argument("--port", type=int, default=43449, help="Port to run the server on")
    parser.add_argument("--env", type=str, default=".env.prod", help="Path to env file")
    parser.add_argument("--mcp", action="store_true", help="Run as MCP stdin server (future)")
    parser.add_argument("--config_file", type=str, help="Path to exploration config JSON file for one-off run")

    args = parser.parse_args()

    if args.mcp:
        logger.info("MCP mode is not yet implemented.")
        sys.exit(1)
    
    try:
        facade = FeatureFacade(args.env)
        set_feature_facade_instance(facade)
        auth_response = facade.authenticate()
        api_key = auth_response.apiKey
        version_evaluation = auth_response.clientVersionEvaluation
        
        # Handle version evaluation
        if version_evaluation and version_evaluation.result:
            from .feature_facade import VersionEvaluationResult
            
            if version_evaluation.result == VersionEvaluationResult.HAS_NEWER_VERSION:
                logger.info(f"⚠️  Version Update Recommended: {version_evaluation.helpMessage}. Run: pip install --upgrade testchimp-local")
            elif version_evaluation.result == VersionEvaluationResult.IS_UNSUPPORTED_VERSION:
                logger.info(f"❌ Unsupported Version: {version_evaluation.helpMessage}")
                logger.info("Please update to the latest version to continue. Run pip install --upgrade testchimp-local")
                sys.exit(1)
            elif version_evaluation.result == VersionEvaluationResult.UNKNOWN_EVALUATION_RESULT:
                logger.info(f"⚠️  Version Check: {version_evaluation.helpMessage}")
        
        # If config file is provided, run one-off exploration
        if args.config_file:
            logger.info(f"Running one-off exploration with config: {args.config_file}")
            result = asyncio.run(run_exploration_from_file(args.config_file, api_key))
            logger.info(f"Exploration completed: {result}")
            return
        else:
            # Start server mode
            start_server(args, api_key, facade)
            
    except Exception as e:
        logger.info(f"Startup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()