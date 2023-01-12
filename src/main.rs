mod setupcl;
mod wordgen;

use setupcl::SetupCL;
use wordgen::WordGenerator;

fn main() {
    let setup = SetupCL::from_json("samples/test.scl.json").expect("File don't existe");
    let test = WordGenerator::new(&setup);
    println!("{}", test.new_syllable(true));
}
