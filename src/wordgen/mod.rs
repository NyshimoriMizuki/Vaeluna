//! # WordGenerator
//!

use rand::seq::SliceRandom;
use rand::Rng;
use std::collections::HashMap;

mod formatter;

use crate::setupcl::SetupCL;

#[derive(Debug)]
pub struct WordGenerator<'a> {
    phonemes: HashMap<String, Vec<String>>,
    max_word_length: u32,
    syllable_struct: Vec<&'a str>,
}

impl WordGenerator<'_> {
    /// Constructs a `WordGenerator<'a>` with the parameters setted with
    /// `SetupCL`
    ///
    /// ## Example
    /// ```
    /// let setup = SetupCL::from_json("...").expect("...");
    /// let generator = WordGenerator::new(setup);
    /// ```
    pub fn new<'a>(setup: &'a SetupCL) -> WordGenerator<'a> {
        WordGenerator {
            phonemes: setup.get_phonemes(),
            max_word_length: *setup.get_word_length(),
            syllable_struct: break_into_vec(setup.get_syllable_struct()),
        }
    }

    /// This Function creates a [`Vec<String>`] that contains new words
    ///
    /// `num` tells how many words will be generated
    pub fn generate(self, num: Option<u32>) -> Vec<String> {
        let mut words: Vec<String> = Vec::new();
        let mut rng = rand::thread_rng();

        for _ in 0..num.unwrap_or(1) {
            let number_of_syllables = rng.gen_range(0..self.max_word_length) + 1;
            let stress_position = rng.gen_range(0..number_of_syllables);

            let mut new_word: Vec<String> = Vec::new();
            for i in 0..number_of_syllables {
                new_word.push(self.new_syllable(i == stress_position));
            }
            words.push(new_word.join("·"));
        }

        words
    }

    fn new_syllable(&self, is_stressed: bool) -> String {
        let mut new_syllable = String::new();
        let mut rand_gen = rand::thread_rng();

        for i in &self.syllable_struct {
            let optional_phoneme = i.contains("(");

            if optional_phoneme && rand_gen.gen::<bool>() {
                continue;
            }
            new_syllable.push_str(
                self.phonemes
                    .get(if optional_phoneme { &i[1..2] } else { *i })
                    .expect("Invalid phoneme group")
                    .choose(&mut rand_gen)
                    .expect("Error in choice some phoneme"),
            );
        }
        return format!("{}{}", if is_stressed { "ˈ" } else { "" }, new_syllable);
    }
}

fn break_into_vec(target: &str) -> Vec<&str> {
    use regex::Regex;
    Regex::new(r"\(?[A-Z]\)?")
        .expect("Error on build Regex")
        .captures_iter(target)
        .map(|x| x.get(0).map_or("", |m| m.as_str()))
        .collect::<Vec<&str>>()
}
