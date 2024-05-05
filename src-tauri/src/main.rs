// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

const CONSONANTS: [&str; 21] = ["b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "y", "z"];
const VOWELS: [&str; 5] = ["a", "e", "i", "o", "u"];
const SPECIAL_CHARACTERS: [&str; 8] = ["/", ".", ",", "?", "#", "=", "!", "-"];

fn generate_a_syllable() -> String {
    let mut return_buffer = String::new();

    let index_of_a_random_consonant = fastrand::usize(..CONSONANTS.len());
    return_buffer.push_str(CONSONANTS[index_of_a_random_consonant]);

    if fastrand::bool() {
        return_buffer=return_buffer.to_uppercase();
    }

    let index_of_a_random_vowel = fastrand::usize(..VOWELS.len());
    return_buffer.push_str(VOWELS[index_of_a_random_vowel]);

    return return_buffer;
}

#[tauri::command]
fn send_a_password_to_the_frontend( number_of_chunks: u8,
                                    mut number_of_syllables: u8,
                                    mut digits_per_chunk: u8,
                                    include_special_characters: bool,
                                    vary_slightly:bool) -> String {
    let mut return_buffer = String::new();

    for chunks_iterator in 1..=number_of_chunks {

        if vary_slightly {
            if number_of_syllables>1 {
                number_of_syllables=(number_of_syllables as i8 + fastrand::i8(-1..1)) as u8;
            }
        }

        for _syllables_iterator in 1..=number_of_syllables {
            return_buffer=return_buffer+&generate_a_syllable();
        }

        if vary_slightly {
            if digits_per_chunk>1 {
                digits_per_chunk=(digits_per_chunk as i8 + fastrand::i8(-1..2)) as u8;
            }
        }

        for _digits_iterator in 1..=digits_per_chunk {
            return_buffer=return_buffer+&fastrand::u8(0..9).to_string();
        }

        if include_special_characters && chunks_iterator!=number_of_chunks {
            let index_of_a_random_special_character=fastrand::usize(..SPECIAL_CHARACTERS.len());
            return_buffer.push_str(SPECIAL_CHARACTERS[index_of_a_random_special_character]);
        }
    }

    return return_buffer;
}

#[tauri::command]
fn exit_app() {
    std::process::exit(0x0);
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![send_a_password_to_the_frontend,exit_app])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
