#!/usr/bin/env python3
"""Test runner script with support for unit vs integration tests."""

import sys
import subprocess
import argparse


def run_tests(test_type="all", coverage=False, verbose=False):
    """
    Run tests with different configurations.
    
    Args:
        test_type: "unit", "integration", or "all"
        coverage: Enable coverage reporting
        verbose: Enable verbose output
    """
    base_cmd = ["python3", "-m", "pytest"]
    
    if test_type == "unit":
        # Run only unit tests (fast)
        base_cmd.extend(["tests/unit/"])
        print("🚀 Running unit tests (fast)...")
    elif test_type == "integration":
        # Run only integration tests (slow)
        base_cmd.extend(["tests/integration/"])
        print("🐌 Running integration tests (slow, requires external dependencies)...")
    else:
        # Run all tests
        base_cmd.extend(["tests/"])
        print("🔍 Running all tests...")
    
    if coverage:
        base_cmd.extend(["--cov=src", "--cov-report=term-missing"])
        
    if verbose:
        base_cmd.append("-v")
    else:
        base_cmd.extend(["-v", "--tb=short"])
    
    # Run the tests
    try:
        result = subprocess.run(base_cmd, check=True)
        if test_type == "unit":
            print("✅ Unit tests passed!")
        elif test_type == "integration":
            print("✅ Integration tests passed!")
        else:
            print("✅ All tests passed!")
        return 0
    except subprocess.CalledProcessError as e:
        if test_type == "unit":
            print("❌ Unit tests failed!")
        elif test_type == "integration":
            print("❌ Integration tests failed!")
        else:
            print("❌ Tests failed!")
        return e.returncode


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Run PyChessBot tests")
    parser.add_argument("--type", choices=["unit", "integration", "all"], 
                       default="all", help="Type of tests to run")
    parser.add_argument("--coverage", action="store_true",
                       help="Enable coverage reporting")
    parser.add_argument("--verbose", action="store_true",
                       help="Enable verbose output")
    
    args = parser.parse_args()
    
    return run_tests(
        test_type=args.type,
        coverage=args.coverage,
        verbose=args.verbose
    )


if __name__ == "__main__":
    sys.exit(main())