const ANSI_256_TABLE: [[u8; 6]; 3] = [
    [0, 95, 135, 175, 215, 255],
    [0, 95, 135, 175, 215, 255],
    [0, 95, 135, 175, 215, 255],
];

pub fn rgb_to_ansi(r: u8, g: u8, b: u8, background: bool) -> String {
    format!("\x1B[{};2;{};{};{}m", if background { 48 } else { 38 }, r, g, b)
}

pub fn rgb_to_ansi_256(r: u8, g: u8, b: u8) -> u8 {
    if r == g && g == b{
        if r<8{16}
        else if r>248 {231}
        else {(((r as f32 -8.0) / 247.0 * 24.0).round() as u8) + 232}
    }
    else {
        16 + 
        36 * (ANSI_256_TABLE[0].binary_search(&r).unwrap_or_else(|x| x - 1) as u8) +
        6 * (ANSI_256_TABLE[1].binary_search(&g).unwrap_or_else(|x| x - 1) as u8) +
        (ANSI_256_TABLE[2].binary_search(&b).unwrap_or_else(|x| x - 1) as u8)
    }
}
