import unittest

import connect_four


class ConnectFourTests(unittest.TestCase):
    def test_create_board_has_six_rows_and_seven_empty_cells_per_row(self):
        board = connect_four.criar_tabuleiro()

        self.assertEqual(len(board), connect_four.LINHAS)
        self.assertTrue(all(len(row) == connect_four.COLUNAS for row in board))
        self.assertTrue(all(cell == 0 for row in board for cell in row))

    def test_insert_piece_stacks_from_the_bottom(self):
        board = connect_four.criar_tabuleiro()

        self.assertTrue(connect_four.inserir_ficha(board, 2, 1))
        self.assertEqual(board[connect_four.LINHAS - 1][2], 1)

    def test_insert_piece_rejects_invalid_or_full_columns(self):
        board = connect_four.criar_tabuleiro()

        self.assertFalse(connect_four.inserir_ficha(board, -1, 1))
        self.assertFalse(connect_four.inserir_ficha(board, connect_four.COLUNAS, 1))
        for _ in range(connect_four.LINHAS):
            self.assertTrue(connect_four.inserir_ficha(board, 0, 1))
        self.assertFalse(connect_four.inserir_ficha(board, 0, 2))

    def test_detects_horizontal_vertical_and_diagonal_wins(self):
        horizontal = connect_four.criar_tabuleiro()
        horizontal[5][0:4] = [1, 1, 1, 1]
        self.assertTrue(connect_four.verificar_vitoria(horizontal, 1))

        vertical = connect_four.criar_tabuleiro()
        for row in range(2, 6):
            vertical[row][3] = 2
        self.assertTrue(connect_four.verificar_vitoria(vertical, 2))

        diagonal = connect_four.criar_tabuleiro()
        for offset in range(4):
            diagonal[5 - offset][offset] = 1
        self.assertTrue(connect_four.verificar_vitoria(diagonal, 1))

    def test_detects_draw_only_when_board_is_full(self):
        board = connect_four.criar_tabuleiro()
        self.assertFalse(connect_four.verificar_empate(board))

        board[:] = [
            [2, 2, 1, 2, 1, 2, 2],
            [2, 2, 2, 1, 1, 2, 1],
            [1, 1, 2, 1, 2, 2, 1],
            [2, 1, 1, 1, 2, 1, 1],
            [1, 2, 1, 2, 1, 1, 2],
            [1, 2, 1, 2, 2, 2, 1],
        ]

        self.assertFalse(connect_four.verificar_vitoria(board, 1))
        self.assertFalse(connect_four.verificar_vitoria(board, 2))
        self.assertTrue(connect_four.verificar_empate(board))


if __name__ == "__main__":
    unittest.main()
