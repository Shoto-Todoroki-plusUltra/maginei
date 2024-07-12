mod print_img;
mod color_code;

use std::env;
use std::path::Path;

fn print_help() {
    println!("Usage: program [-f width] [-i file_path] [file_path]");
    println!("  -f width      Set the width (default: 200)");
    println!("  -i file_path  Specify the input file path");
    println!("  -h, --help    Show this help message");
    println!("If no flags are used, the first argument is treated as the file path.");
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let mut width: u32 = 200;
    let mut file_path: Option<&str> = None;

    if args.len() == 1 || args.contains(&String::from("-h")) || args.contains(&String::from("--help")) {
        print_help();
        return;
    }

    let mut i = 1;
    while i < args.len() {
        match args[i].as_str() {
            "-f" => {
                if i + 1 < args.len() {
                    width = match args[i + 1].parse() {
                        Ok(num) => num,
                        Err(_) => {
                            eprintln!("Error: Width must be a valid u32");
                            std::process::exit(1);
                        }
                    };
                    i += 2;
                } else {
                    eprintln!("Error: -f flag requires a value");
                    std::process::exit(1);
                }
            }
            "-i" => {
                if i + 1 < args.len() {
                    file_path = Some(&args[i + 1]);
                    i += 2;
                } else {
                    eprintln!("Error: -i flag requires a value");
                    std::process::exit(1);
                }
            }
            _ => {
                if file_path.is_none() {
                    file_path = Some(&args[i]);
                }
                i += 1;
            }
        }
    }

    let file_path = match file_path {
        Some(p) => p,
        None => {
            eprintln!("Error: No file path provided");
            print_help();
            std::process::exit(1);
        }
    };

    if !Path::new(file_path).exists() {
        eprintln!("Error: Invalid path. File does not exist: {}", file_path);
        std::process::exit(1);
    }
    
    print_img::print_img(file_path, width);
}
