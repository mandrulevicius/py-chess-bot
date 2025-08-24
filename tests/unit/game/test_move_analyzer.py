"""Tests for move analyzer."""

import pytest
import chess
from src.game.move_analyzer import analyze_move, analyze_move_from_san


class TestMoveAnalyzer:
    """Test the move analyzer functions."""
    
    def test_analyze_normal_move(self):
        """Test analyzing a normal move."""
        board = chess.Board()
        move = board.parse_san('e4')
        
        analysis = analyze_move(board, move)
        
        assert not analysis['is_capture']
        assert not analysis['is_check']
        assert not analysis['is_checkmate']
        assert not analysis['is_castle']
        assert not analysis['is_promotion']
        assert not analysis['is_en_passant']
    
    def test_analyze_capture_move(self):
        """Test analyzing a capture move."""
        # Set up position where white pawn can capture black pawn
        board = chess.Board()
        board.push(chess.Move.from_uci("e2e4"))  # e4
        board.push(chess.Move.from_uci("d7d5"))  # d5
        
        # Now white can capture with exd5
        move = board.parse_san('exd5')
        
        analysis = analyze_move(board, move)
        
        assert analysis['is_capture']
    
    def test_analyze_check_move(self):
        """Test analyzing a move that gives check."""
        # Set up position where we can give check
        board = chess.Board("rnbqkb1r/pppp1ppp/5n2/4p3/2B1P3/8/PPPP1PPP/RNBQK1NR w KQkq - 2 3")
        move = board.parse_san('Bxf7+')  # Bishop takes f7 with check
        
        analysis = analyze_move(board, move)
        
        assert analysis['is_capture']
        assert analysis['is_check']
        assert not analysis['is_checkmate']
    
    def test_analyze_castling_move(self):
        """Test analyzing castling moves."""
        # Set up position where castling is possible
        board = chess.Board("r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1")
        
        # Test kingside castling
        move = board.parse_san('O-O')
        analysis = analyze_move(board, move)
        
        assert analysis['is_castle']
        assert not analysis['is_capture']
        assert not analysis['is_check']
        
        # Test queenside castling  
        board = chess.Board("r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1")
        move = board.parse_san('O-O-O')
        analysis = analyze_move(board, move)
        
        assert analysis['is_castle']
    
    def test_analyze_promotion_move(self):
        """Test analyzing pawn promotion."""
        # Set up position with pawn ready to promote
        board = chess.Board("8/P7/8/8/8/8/8/4K3 w - - 0 1")
        move = board.parse_san('a8=Q')
        
        analysis = analyze_move(board, move)
        
        assert analysis['is_promotion']
        assert not analysis['is_capture']
    
    def test_analyze_en_passant_move(self):
        """Test analyzing en passant capture."""
        # Set up en passant position
        board = chess.Board("rnbqkbnr/ppp1p1pp/8/3pPp2/8/8/PPPP1PPP/RNBQKBNR w KQkq f6 0 3")
        move = board.parse_san('exf6')  # en passant capture
        
        analysis = analyze_move(board, move)
        
        assert analysis['is_en_passant']
        assert analysis['is_capture']
    
    def test_analyze_checkmate_move(self):
        """Test analyzing a checkmate move."""
        # Use a known checkmate position: back rank mate
        board = chess.Board("6k1/5ppp/8/8/8/8/5PPP/R5K1 w - - 0 1")
        move = board.parse_san('Ra8#')
        
        analysis = analyze_move(board, move)
        
        assert analysis['is_checkmate']
        assert analysis['is_check']
    
    def test_analyze_move_from_san_valid(self):
        """Test analyzing move from SAN notation."""
        board = chess.Board()
        
        analysis = analyze_move_from_san(board, 'e4')
        
        assert not analysis['is_capture']
        assert not analysis['is_check']
        assert not analysis['is_checkmate']
        assert not analysis['is_castle']
        assert not analysis['is_promotion']
        assert not analysis['is_en_passant']
    
    def test_analyze_move_from_san_invalid(self):
        """Test analyzing invalid SAN notation."""
        board = chess.Board()
        
        analysis = analyze_move_from_san(board, 'invalid_move')
        
        # Should return all False for invalid moves
        assert not analysis['is_capture']
        assert not analysis['is_check']
        assert not analysis['is_checkmate']
        assert not analysis['is_castle']
        assert not analysis['is_promotion']
        assert not analysis['is_en_passant']
    
    def test_analyze_move_from_san_illegal(self):
        """Test analyzing illegal but valid SAN notation."""
        board = chess.Board()
        
        # Try to move a piece that can't move there
        analysis = analyze_move_from_san(board, 'Ke2')  # King can't move to e2 from starting position
        
        # Should return all False for illegal moves
        assert not analysis['is_capture']
        assert not analysis['is_check']
        assert not analysis['is_checkmate']
        assert not analysis['is_castle']
        assert not analysis['is_promotion']
        assert not analysis['is_en_passant']
    
    def test_analyze_complex_move(self):
        """Test analyzing a move with multiple characteristics."""
        # Set up position where we can have a capturing move that gives check
        board = chess.Board("r1bqk2r/pppp1ppp/2n2n2/2b1p3/2B1P3/3P1N2/PPP2PPP/RNBQK2R w KQkq - 4 4")
        move = board.parse_san('Bxf7+')  # Capture with check
        
        analysis = analyze_move(board, move)
        
        assert analysis['is_capture']
        assert analysis['is_check']
        assert not analysis['is_checkmate']  # Shouldn't be mate
        assert not analysis['is_castle']
        assert not analysis['is_promotion']