use regex::Regex;
use std::collections::HashMap;
use std::fs;

pub struct Reader {
    pub file_content: String,
}

impl Reader {
    pub fn from(filename: &str) -> Reader {
        Reader {
            file_content: fs::read_to_string(filename).expect("error on reading the file"),
        }
    }

    pub fn tokenize(self) {
        let re_phonex: Regex = Regex::new(
            r"^(?P<indent> - |—)?(?P<left>\{.+\}|.+) +(->|>|→) +(?P<right>\{.+\}|[^\n/]+) */? *(?P<case>.+$|$)")
            .expect("error on build a regex");
        let re_stopcomment: Regex =
            Regex::new("@\"(?P<message>.*)\"").expect("error on build a regex");
        let re_label: Regex = Regex::new(r"^(?P<type>filter|rominize)? ?(?P<name>.+):$")
            .expect("error on build a regex");
        let re_group: Regex = Regex::new(
            r"(group|define|def)\s*(?P<name>[A-Z])\s*\{\s*(?P<extend>[A-Z]\+|\+[A-Z])?\s*(?P<value>.+)\s*\}")
            .expect("error on build a regex");

        let mut parsed_text: Vec<Node> = vec![];

        for line in self.file_content.split("\n") {
            if re_stopcomment.is_match(line) {
                let capture = re_stopcomment.captures(line).unwrap();
                println!("{:?}", capture.name("message"));
            }
            if re_label.is_match(line) {
                let capture = re_label.captures(line).unwrap();
                println!("{:?}", capture);
            }
            if re_phonex.is_match(line) {
                let new_phonex = PhonexNode::new(line, &re_phonex);
                let p = re_phonex.captures(line).unwrap();

                parsed_text.push(Node::PhonexNode(new_phonex));
            }
            if re_group.is_match(line) {
                let capture = re_group.captures(line).unwrap();
                println!("{:?}", capture);
            }
        }
    }
}

enum Node {
    PhonexNode(PhonexNode),
    LabelNode(LabelNode),
    GroupNode(GroupNode),
    StopCommentNode(StopCommentNode),
}

#[derive(Debug)]
pub struct PhonexNode {
    case: String,
    left: String,
    right: String,
}
impl PhonexNode {
    fn new(line: &str, pattern: &Regex) -> PhonexNode {
        let capture = pattern.captures(line).unwrap();

        PhonexNode {
            case: capture.name("case").unwrap().as_str().to_string(),
            left: capture.name("left").unwrap().as_str().to_string(),
            right: capture.name("right").unwrap().as_str().to_string(),
        }
    }
}

#[derive(Debug)]
pub struct GroupNode {
    name: String,
    value: Vec<String>,
}
impl GroupNode {
    fn new(line: &str, pattern: &Regex) -> GroupNode {
        let capture = pattern.captures(line).unwrap();

        GroupNode {
            name: capture.name("name").unwrap().as_str().to_string(),
            value: vec![capture.name("name").unwrap().as_str().to_string()],
        }
    }
}

#[derive(Debug)]
pub struct StopCommentNode {
    message: String,
}
impl StopCommentNode {
    fn new(line: &str, pattern: &Regex) -> StopCommentNode {
        let capture = pattern.captures(line).unwrap();

        StopCommentNode {
            message: capture.name("message").unwrap().as_str().to_string(),
        }
    }
}

#[derive(Debug)]
pub struct LabelNode {
    type_: String,
    name: String,
    content: Vec<PhonexNode>,
}
impl LabelNode {
    fn new(line: &str, pattern: &Regex) -> LabelNode {
        let capture = pattern.captures(line).unwrap();
        let vec_phonex: Vec<PhonexNode> = vec![];

        LabelNode {
            type_: capture.name("name").unwrap().as_str().to_string(),
            name: capture.name("name").unwrap().as_str().to_string(),
            content: vec_phonex,
        }
    }

    fn add(&mut self, new_phonex: PhonexNode) {
        self.content.push(new_phonex);
    }
}
