pub mod setupcl {
    use serde::{Deserialize, Serialize};
    use serde_json::{self, Error};
    use std::collections::HashMap;
    use std::fs::read_to_string;

    #[derive(Deserialize, Serialize, Debug)]
    pub struct SetupCL {
        pub syllable_struct: String,
        pub word_length: u32,
        pub phonemes: HashMap<String, Vec<String>>,
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
