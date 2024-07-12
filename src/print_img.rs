use image::{GenericImageView, Pixel};
use std::env;
use std::io::{self, Write};
use rayon::prelude::*;

use crate::color_code::{rgb_to_ansi, rgb_to_ansi_256};

pub fn print_img(image_path: &str, width: u32) {
    let img = image::open(image_path).expect("Failed to open image");
    
    let aspect_ratio = img.height() as f32 / img.width() as f32;
    let height = (width as f32 * aspect_ratio).ceil() as u32;
    
    let height = if height % 2 != 0 { height + 1 } else { height };
    
    let img = img.resize_exact(width, height, image::imageops::FilterType::Lanczos3);
    
    let true_color = env::var("COLORTERM").map(|v| v == "truecolor" || v == "24bit").unwrap_or(false);
    let output: Vec<String> = (0..height).into_par_iter().step_by(2).map(|y| {
        let mut line = String::with_capacity(width as usize * 20);
        for x in 0..width {
            let upper_pixel = img.get_pixel(x, y);
            let lower_pixel = img.get_pixel(x, y + 1);
            
            let (r1, g1, b1, _) = upper_pixel.channels4();
            let (r2, g2, b2, _) = lower_pixel.channels4();
            
            if true_color {
                let upper_color = rgb_to_ansi(r1, g1, b1, false);
                let lower_color = rgb_to_ansi(r2, g2, b2, true);
                line.push_str(&format!("{}{}\u{2580}", upper_color, lower_color));
            } else {
                let upper_color = format!("\x1B[38;5;{}m", rgb_to_ansi_256(r1, g1, b1));
                let lower_color = format!("\x1B[48;5;{}m", rgb_to_ansi_256(r2, g2, b2));
                line.push_str(&format!("{}{}\u{2580}", upper_color, lower_color));
            }
        }
        line.push_str("\x1B[0m\n");
        line
    }).collect();
    
    let output = output.join("");
    io::stdout().write_all(output.as_bytes()).unwrap();
    io::stdout().flush().unwrap();   
}
