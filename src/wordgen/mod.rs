use rand::seq::SliceRandom;
use rand::Rng;
use std::collections::HashMap;

use crate::setupcl::SetupCL;

#[derive(Debug)]
pub struct WordGenerator<'a> {
    phonemes: HashMap<String, Vec<String>>,
    max_word_length: u32,
    syllable_struct: Vec<&'a str>,
}

impl WordGenerator<'_> {
    pub fn new<'a>(setup: &'a SetupCL) -> WordGenerator<'a> {
        WordGenerator {
            phonemes: setup.get_phonemes(),
            max_word_length: *setup.get_word_length(),
            syllable_struct: break_into_vec(setup.get_syllable_struct()),
        }
    }
    pub fn generate(self, num: Option<u32>) -> Vec<String> {
        let mut words: Vec<String> = Vec::new();
        let mut rng = rand::thread_rng();

        for _ in 0..num.unwrap_or(1) {
            let num_of_syllables = rng.gen_range(0..self.max_word_length) + 1;
            let stress_possition = rng.gen_range(0..num_of_syllables);

            let mut new_word: Vec<String> = Vec::new();
            for i in 0..num_of_syllables {
                if i == stress_possition {
                    new_word.push(self.new_syllable(true));
                } else {
                    new_word.push(self.new_syllable(false));
                }
            }
            words.push(new_word.join("·"));
        }

        words
    }

    pub fn new_syllable(&self, stress: bool) -> String {
        let mut new_syllable = String::new();
        let mut rand_gen = rand::thread_rng();

        for i in &self.syllable_struct {
            if i.contains("(") && rand_gen.gen::<bool>() {
                continue;
            }
            let phonemes = self
                .phonemes
                .get(if i.contains("(") { &i[1..2] } else { *i })
                .expect("no phoneme");

            new_syllable.push_str(
                phonemes
                    .choose(&mut rand_gen)
                    .expect("error on choice some phoneme"),
            );
        }
        if stress {
            return format!("ˈ{}", new_syllable);
        }
        new_syllable
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
