let rec read_lines f =
  try
    let line = input_line f in
    line :: read_lines f
  with End_of_file -> []

let soc c s =
    let q = String.split_on_char c s in
    let q = List.filter (fun e -> e <> "") q in
    (List.hd q, List.hd (List.tl q))
  
let tri l = 
    List.sort Stdlib.compare l

let rec split = function 
    [] -> []
    | s::q -> (soc ' ' s)::(split q)

let part1 =
    List.fold_left2 (fun s g d -> s + abs (g-d)) 0

let occ l x = List.length (List.filter ((=) x) l)

let part2 lg ld =
    List.fold_left2 (fun s g d -> s + g * occ ld g) 0 lg ld

let solution l = 
    let elems = split l in
    let lg = List.map (fun x -> int_of_string (fst x)) elems in
    let ld = List.map (fun x -> int_of_string (snd x)) elems in
    let lg = List.sort Stdlib.compare lg in
    let ld = List.sort Stdlib.compare ld in
    part1 lg ld, part2 lg ld

let () =
    let file = read_lines (open_in "input.txt") in
    let sol1, sol2 = solution file in
    Printf.printf "Partie 1 : %d\nPartie 2 : %d\n" sol1 sol2
