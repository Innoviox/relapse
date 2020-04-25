use std::fmt;

#[derive(Copy, Clone)]
pub enum Color {
    YELLOW,
    RED,
}

#[derive(Copy, Clone)]
pub enum SpaceType {
    EMPTY,
    ENTRY { color: Color },
    HOME { color: Color },
    SQUARE { color: Color },
    CIRCLE { color: Color },
    TRIANGLE { color: Color },
}

#[derive(Copy, Clone)]
pub struct Space {
    space_type: SpaceType,
    x: usize,
    y: usize,
    c: char
}

impl Space {
    pub fn from_char(c: char, x: usize, y: usize) -> Space {
        let space_type = match c {
            'e' => SpaceType::ENTRY { color: Color::YELLOW },
            'E' => SpaceType::ENTRY { color: Color::RED },
            'h' => SpaceType::HOME { color: Color::YELLOW },
            'H' => SpaceType::HOME { color: Color::RED },
            's' => SpaceType::SQUARE { color: Color::YELLOW },
            'S' => SpaceType::SQUARE { color: Color::RED },
            'c' => SpaceType::CIRCLE { color: Color::YELLOW },
            'C' => SpaceType::CIRCLE { color: Color::RED },
            't' => SpaceType::TRIANGLE { color: Color::YELLOW },
            'T' => SpaceType::TRIANGLE { color: Color::RED },
            _ => SpaceType::EMPTY
        };

        Space { space_type, x, y, c }
    }
}

impl fmt::Display for Space {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.c)
    }
}