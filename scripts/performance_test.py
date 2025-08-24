#!/usr/bin/env python3
"""Performance testing script for PyChessBot."""

import time
import statistics
from typing import List
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from game.game_loop import create_game
from ai.stockfish_ai import create_ai
from analysis.position_evaluator import get_position_evaluation


def time_function(func, *args, **kwargs):
    """Time a function call and return (result, duration)."""
    start_time = time.perf_counter()
    result = func(*args, **kwargs)
    end_time = time.perf_counter()
    return result, end_time - start_time


def benchmark_evaluation(runs: int = 10) -> List[float]:
    """Benchmark position evaluation performance."""
    print(f"🔬 Benchmarking position evaluation ({runs} runs)...")
    
    # Setup
    game = create_game()
    ai = create_ai(difficulty=5)  # Medium difficulty for testing
    
    times = []
    for i in range(runs):
        _, duration = time_function(get_position_evaluation, game, ai)
        times.append(duration)
        print(f"  Run {i+1}/{runs}: {duration:.3f}s")
    
    return times


def benchmark_ai_move(runs: int = 5) -> List[float]:
    """Benchmark AI move generation performance."""
    print(f"🤖 Benchmarking AI move generation ({runs} runs)...")
    
    # Setup
    game = create_game()
    ai = create_ai(difficulty=5)
    
    times = []
    for i in range(runs):
        from ai.stockfish_ai import get_ai_move
        _, duration = time_function(get_ai_move, ai, game, time_limit=3.0)
        times.append(duration)
        print(f"  Run {i+1}/{runs}: {duration:.3f}s")
    
    return times


def print_statistics(name: str, times: List[float]):
    """Print timing statistics."""
    print(f"\n📊 {name} Statistics:")
    print(f"  Mean: {statistics.mean(times):.3f}s")
    print(f"  Median: {statistics.median(times):.3f}s")
    print(f"  Min: {min(times):.3f}s")
    print(f"  Max: {max(times):.3f}s")
    if len(times) > 1:
        print(f"  StdDev: {statistics.stdev(times):.3f}s")


def main():
    """Run performance benchmarks."""
    print("🚀 PyChessBot Performance Benchmarking")
    print("=" * 50)
    
    try:
        # Test evaluation performance
        eval_times = benchmark_evaluation(runs=10)
        print_statistics("Position Evaluation", eval_times)
        
        print()
        
        # Test AI move generation
        ai_times = benchmark_ai_move(runs=5)
        print_statistics("AI Move Generation", ai_times)
        
        print()
        print("✅ Performance benchmarking complete!")
        
        # Performance assessment
        avg_eval = statistics.mean(eval_times)
        avg_ai = statistics.mean(ai_times)
        
        print("\n🎯 Performance Assessment:")
        if avg_eval < 0.5:
            print("  ✅ Position evaluation: FAST")
        elif avg_eval < 1.0:
            print("  ⚠️  Position evaluation: MODERATE")
        else:
            print("  🐌 Position evaluation: SLOW")
            
        if avg_ai < 3.0:
            print("  ✅ AI move generation: FAST")
        elif avg_ai < 5.0:
            print("  ⚠️  AI move generation: MODERATE")
        else:
            print("  🐌 AI move generation: SLOW")
    
    except Exception as e:
        print(f"❌ Benchmarking failed: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())