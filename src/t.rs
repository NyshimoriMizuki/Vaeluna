pub fn t() {
    let sentence = String::from("como pode");

    let vowels_number: Vec<_> = sentence
        .chars()
        .filter(|x| {
            [
                'a'.to_lowercase(),
                'e'.to_lowercase(),
                'i'.to_lowercase(),
                'o'.to_lowercase(),
                'u'.to_lowercase(),
            ]
            .contains(x.to_lowercase())
        })
        .collect();

    println!("Number of vowels is {:?}", vowels_number);
}
