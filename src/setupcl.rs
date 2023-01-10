pub mod setupcl {
    use serde::{Deserialize, Serialize};
    use serde_json::{self, Error};
    use std::collections::HashMap;
    use std::fs::read_to_string;

    #[derive(Deserialize, Serialize, Debug)]
    pub struct SetupCL {
        syllable_struct: String,
        word_length: u32,
        phonemes: HashMap<String, Vec<String>>,
        pub extra_params: Option<HashMap<String, bool>>,
    }

    impl SetupCL {
        pub fn new(filename: &str) -> Result<SetupCL, Error> {
            let file = read_to_string(filename).expect("Error on opening file");
            let json = serde_json::from_str::<SetupCL>(&file);

            match json {
                Ok(_) => json,
                Err(e) => Err(e),
            }
        }
    }
}

/*

*/
