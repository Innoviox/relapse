use crate::board::Board;

mod board;
mod util;

fn main() {
    let board = Board::default();

    println!("{}", board);
}
