use crate::util::Space;
use std::fmt;

pub struct Board {
    board: Vec<Vec<Space>>,
}

impl Board {
    pub fn default() -> Board {
        let board_string = [
            "..............",
            "..............",
            "S............s",
            "T............t",
            "C...ehhHHE...c",
            "C...ehhHHE...c",
            "T............t",
            "S............s",
            "..............",
            "..............",
        ];

        let mut board = Vec::new();

        for (y, row) in board_string.iter().enumerate() {
            let mut row_vec = Vec::new();
            for (x, space) in row.chars().enumerate() {
                row_vec.push(Space::from_char(space, x, y));
            }
            board.push(row_vec);
        }

        Board { board }
    }
}

impl fmt::Display for Board {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let sep = "-".repeat(1 + 2 * self.board[0].len());

        for row in self.board.iter() {
            write!(f, "{}\n|", sep).expect("fail");
            for space in row {
                write!(f, "{}|", space).expect("fail");
            }
            write!(f, "\n").expect("fail");
        }

        write!(f, "{}", sep)
    }
}