mod setupcl;

use setupcl::setupcl::SetupCL;

fn main() {
    let test = SetupCL::new("samples/test.scl.json").expect("File don't existe");
    println!("{:#?}", test.extra_params)
}
