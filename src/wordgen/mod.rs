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
    pub fn generate(self, num: Option<u32>) {}

    pub fn new_syllable(&self, stress: bool) -> String {
        let mut new_syllable = String::new();

        for i in &self.syllable_struct {
            if i.contains("(") && rand::thread_rng().gen::<bool>() {
                continue;
            }
            let group = if i.contains("(") { &i[1..2] } else { *i };
            println!("{:?}", self.phonemes.get(group).expect("no phoneme"));
            new_syllable.push_str(i);
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
