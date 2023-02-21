//! # Setup Conlang
//!
//! Setupcl is a Vaeluna module that reads and writes the Setup Conlang file.
//!
//! This file is in json format, with extension `.scl.json`.
//! ### Exemple:
//! ```
//! {
//!    "syllable_struct": "(C)V(C)",
//!    "word_length": 3,
//!    "phonemes": {
//!        "C": ["m", "n", "p", "t", "k", "s", "h", "l", "w", "j"],
//!        "V": ["a", "e", "i", "o", "u"]
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
//! > Some groups could be marked as `Optional` with the paranteses, what don't have it is mandatory.
//! >
//! > ```
//! > "syllable_struct": "CV(C)",
//! > ...
//! >  ```
//!
//! * ### `word_length`
//! > It tells who long can a word be in this conlang.
//! >
//! > In this case, the maximun word length is 3, with maximun of 3 syllables in one word.
//! > ```
//! > "word_length": 3,
//! > ...
//! >  ```
//!
//! * ### `phonemes`
//! > This sets the groups used in `syllable_struct`, linsting the phonemes in each group.
//! >
//! > ```
//! > "phonemes": {
//! >     "C": ["m", "n", "p", "t", "k", "s", "h", "l", "w", "j"],
//! >     "V": ["a", "e", "i", "o", "u"],
//! >     "F": ["m", "n", "l", "w", "j"],
//! > }
//! >  ```
//!
//! ## Extra parameters
//! > There is som extra parameters to a best word generation (this is being inplemented)
//!
//! > Somo of thes parameters are:
//! > * no_stops_encounter
//! > * is_tonal_lang
//! > * generate_roots

use serde::{Deserialize, Serialize};
use serde_json::{self, Error};
use std::collections::HashMap;
use std::fs::read_to_string;

/// # SetupCL
///
/// > This is a struct that builds all settings for a Vaeluna project, includes informations
/// > of how build a word, what phonemes it will use. <br>
/// > It also includes some optional extra parameter, like `is_tonal_lang` for when will use
/// > tones instead of a stress system.
///
/// # Example
/// ```
/// ...
///
/// let setup = Setup::from_json("MyConlang.scl.json").expect("File don't existe");
/// ```
#[derive(Deserialize, Serialize, Debug)]
pub struct SetupCL {
    syllable_struct: String,
    word_length: u32,
    phonemes: HashMap<String, Vec<String>>,
    extra_params: Option<HashMap<String, bool>>,
}

impl SetupCL {
    /// returns the phonemes from a SetupCL
    ///
    /// # Example
    /// ```
    /// ...
    ///
    /// let setup = Setup::from_json("...").expect("File don't existe");
    /// let phonemes = setup.get_phonemes();
    /// ```
    pub fn get_phonemes(&self) -> HashMap<String, Vec<String>> {
        copy(&self.phonemes)
    }

    /// returns the word_length from a SetupCL
    ///
    /// # Example
    /// ```
    /// ...
    ///
    /// let setup = Setup::from_json("...").expect("File don't existe");
    /// let phonemes = setup.get_word_length();
    /// ```
    pub fn get_word_length(&self) -> &u32 {
        &self.word_length
    }

    /// returns the syllable_struct from a SetupCL
    ///
    /// # Example
    /// ```
    /// ...
    ///
    /// let setup = Setup::from_json("...").expect("File don't existe");
    /// let phonemes = setup.get_syllable_struct();
    /// ```
    pub fn get_syllable_struct(&self) -> &str {
        &self.syllable_struct[..]
    }

    /// Builds a new SetupCL with a json file
    ///
    /// # Errors
    /// Raise an error when could not read the json file
    ///
    /// # Example
    /// basic usege:
    /// ```
    /// ...
    ///
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

/// Function used to clone a `HashMap`
fn copy<K: Clone, V: Clone>(map: &HashMap<K, V>) -> HashMap<K, V> {
    map.clone()
}
