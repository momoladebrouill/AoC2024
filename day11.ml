let rec read_lines f =
  try
    let line = input_line f in
    line :: read_lines f
  with End_of_file -> []

let soc c s =
    let q = String.split_on_char c s in
    let q = List.filter (fun e -> e <> "") q in
    q


let solution l = 
    let elems = soc " " l in
    List.iter (fun e->Printf.printf "%s" e) elems; 
    0

let () =
    let file = read_lines (open_in "input.txt") in
    let sol2 = solution file in
    Printf.printf "Partie 2 : %d\n" sol2
