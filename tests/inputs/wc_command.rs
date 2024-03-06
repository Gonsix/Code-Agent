use clap::Parser;
use std::error::Error;
use std::fs::File;
use std::io::{self, BufRead, BufReader};

#[derive(Debug, Parser)]
#[command(author = "Gonsix", version = "0.6.6", about)]
/// Rust wc
pub struct Args {
    /// Input file(s)
    #[arg(value_name = "FILE", default_value = "-")]
    files: Vec<String>,

    /// Show line count
    #[arg(short = 'l', long = "lines", default_value = "false")]
    lines: bool,

    /// Show word count
    #[arg(short = 'w', long = "words", default_value = "false")]
    words: bool,

    /// Show byte count
    #[arg(
        short = 'c',
        long = "bytes",
        default_value = "false",
        conflicts_with = "chars"
    )]
    bytes: bool,

    /// Show character count
    #[arg(
        short = 'm',
        long = "chars",
        default_value = "false",
        conflicts_with = "bytes"
    )]
    chars: bool,
}

type MyResult<T> = Result<T, Box<dyn Error>>;

pub fn get_args() -> MyResult<Args> {
    let mut args = Args::parse();
    /* 全てのフラグがfalseなら、lines, words, bytes をTrueにする. イテレータ〜は使用しない*/
    if [args.lines, args.words, args.bytes, args.chars] == [false, false, false, false] {
        args.lines = true;
        args.words = true;
        args.bytes = true;
    }
    Ok(args)
}

fn open(filename: &str) -> MyResult<Box<dyn BufRead>> {
    match filename {
        "-" => Ok(Box::new(BufReader::new(io::stdin()))),
        _ => Ok(Box::new(BufReader::new(File::open(filename)?))),
    }
}

/// 条件に応じてカウントを文字列に変換する
fn count_to_string(count: usize, flag: bool) -> String {
    match flag {
        false => String::from(""),
        true => format!("{:>8}", count),
    }
}

pub fn run(args: Args) -> MyResult<()> {
    // println!("{:#?}", args);

    let mut total_line_counts = 0;
    let mut total_word_counts = 0;
    let mut total_byte_counts = 0;
    let mut total_char_counts = 0;

    for filename in &args.files {
        match open(&filename) {
            Err(err) => eprintln!("{}: open: {}", filename, err),
            Ok(mut reader) => {

                // let filename = if filename != "-" { filename } else {String::new("") }
                //TODO:  各カウントに実際の値を入れる. オプションでフラグがアクティブになっていない場合は0を代入. Totalの計算に使用される
                let mut line_count = 0;
                let mut word_count = 0;
                let mut byte_count = 0;
                let mut char_count = 0;

                let mut line = String::new();
                loop {
                    // 改行文字もバイト数にカウントする必要があるので、reader.lines() ではなく、reader.read_line()を利用.
                    let line_bytes = reader.read_line(&mut line)?;
                    if line_bytes == 0 {
                        break;
                    }
                    line_count += 1;
                    word_count += line.split_whitespace().count();
                    byte_count += line_bytes;
                    char_count += line.chars().count();
                    line.clear()
                }

                // Totalに足す
                total_line_counts += line_count;
                total_byte_counts += byte_count;
                total_word_counts += word_count;
                total_char_counts += char_count;

                println!(
                    "{}{}{}{}{}",
                    count_to_string(line_count, args.lines),
                    count_to_string(word_count, args.words),
                    count_to_string(byte_count, args.bytes),
                    count_to_string(char_count, args.chars),
                    if filename != "-"  { format!(" {}", filename) } else { "".to_string() }
                );
            }
        }
    }

    if args.files.len() > 1 {
        /* Show Total counts */
        println!(
            "{}{}{}{} {}",
            count_to_string(total_line_counts, args.lines),
            count_to_string(total_word_counts, args.words),
            count_to_string(total_byte_counts, args.bytes),
            count_to_string(total_char_counts, args.chars),
            "total"
        );
    }

    Ok(())
}
