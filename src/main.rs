pub mod phonex;
pub mod setupcl;
pub mod wordgen;

use setupcl::SetupCL;
use wordgen::WordGenerator;

fn main() {
    let setup = SetupCL::from_json("samples/test.scl.json").expect("File don't exists");
    let generator = WordGenerator::new(&setup);

    println!("{:#?}", generator.generate(Some(5)));
}
