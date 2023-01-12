use serde::{Deserialize, Serialize};
use serde_json::{self, Error};
use std::collections::HashMap;
use std::fs::read_to_string;

#[derive(Deserialize, Serialize, Debug)]
pub struct SetupCL {
    syllable_struct: String,
    word_length: u32,
    phonemes: HashMap<String, Vec<String>>,
    extra_params: Option<HashMap<String, bool>>,
}

impl SetupCL {
    pub fn get_phonemes(&self) -> HashMap<String, Vec<String>> {
        copy(&self.phonemes)
    }
    pub fn get_word_length(&self) -> &u32 {
        &self.word_length
    }
    pub fn get_syllable_struct(&self) -> &str {
        &self.syllable_struct[..]
    }
}

impl SetupCL {
    pub fn from_json(filename: &str) -> Result<SetupCL, Error> {
        let file = read_to_string(filename).expect("Error on opening file");
        let new_setup_cl = serde_json::from_str::<SetupCL>(&file);

        match new_setup_cl {
            Ok(_) => new_setup_cl,
            Err(e) => Err(e),
        }
    }

    pub fn export_as_json() {}
}

fn copy<K: Clone, V: Clone>(map: &HashMap<K, V>) -> HashMap<K, V> {
    map.clone()
}
