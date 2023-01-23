mod reader;

pub struct Phonex {
    variables: Vec<String>,
}

impl Phonex {
    pub fn build(filename: &str) {
        let text = reader::Reader::from(filename);
        text.tokenize();
    }
}
