//! # Setup Conlang
//!
//! Setupcl is a Vaeluna module that reads and writes the Setup Conlang file.
//!
//! This file is in json format, with extension `.scl.json`.
//! ### Exemple:
//! ```
//! {
//!    "syllable_struct": "(C)V(F)",
//!    "word_length": 3,
//!    "phonemes": {
//!        "C": ["m", "n", "p", "t", "k", "s", "h", "l", "w", "j"],
//!        "V": ["a", "e", "i", "o", "u"],
//!        "F": ["m", "n", "l", "w", "j"]
//!    },
//!    "extra_params": {
//!        "no_stops_encounter": true
//!    }
//! }
//! ```
//! ## Parameters
//!
//! * ### syllable_struct
//! > This is used to find the phonemes groups in syllables building. Usually,
//! > the letters use are uppercase.
//! >
//! >> `Do not do this`
//! > ```
//! > "syllable_struct": "CVK",
//! > "phonemes": {
//! >     "C": ...,
//! >     "V": ...,
//! >     "F": ...
//! > },
//! > ...
//! > ```
//! >> `Do this`
//! > ```
//! > "syllable_struct": "CVK",
//! > "phonemes": {
//! >     "C": ...,
//! >     "V": ...,
//! >     "K": ...
//! > },
//! > ...
//! > ```
//! >
//! > Some groups coul be marked as `Optional` with the paranteses, what don't have it is mandatory.
//! >
//! > ```
//! > "syllable_struct": "CV(C)",
//! > ...
//! >  ```
//!
//! * ### `word_length`
//! > It tell
//!
//! * ### `phonemes`
//!
//! ## Extra parameters
//!

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

    /// # Errors
    /// what causes the error
    /// # Example
    /// basic usege:
    /// ```
    /// let setup = SetupCL::from_json("MyConlang.scl.json")
    ///
    /// match setup {
    ///     Ok(_) -> ...,
    ///     Err(e) -> println!("Error on reading json")
    /// }
    /// ```
    pub fn from_json(filename: &str) -> Result<SetupCL, Error> {
        let file = read_to_string(filename).expect("Error when opening file");
        let new_setup_cl = serde_json::from_str::<SetupCL>(&file);

        match new_setup_cl {
            Ok(_) => new_setup_cl,
            Err(e) => Err(e),
        }
    }
}

fn copy<K: Clone, V: Clone>(map: &HashMap<K, V>) -> HashMap<K, V> {
    map.clone()
}
