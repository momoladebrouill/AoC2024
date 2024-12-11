let rec read_lines f =
  try
    let line = input_line f in
    line :: read_lines f
  with End_of_file -> []

let soc c s =
    let q = String.split_on_char c s in
    let q = List.filter (fun e -> e <> "") q in
    q

let evolve_one x = 
    if x == 0 then [1]
    else if String.length (string_of_int x) mod 2 == 0 then 
        begin
            let s = string_of_int x in
            let len = String.length s in
            let p1  = String.sub s 0 (len/2) in 
            let p2  = String.sub s (len/2) (len/2) in 
            [int_of_string p1;int_of_string p2]
        end
    else
        [x*2024]
            
let rec evolve = function 
    [] -> []
    | x::q -> 

    if x == 0 then 1::evolve q
    else if String.length (string_of_int x) mod 2 == 0 then 
        begin
            let s = string_of_int x in
            let len = String.length s in
            let p1  = String.sub s 0 (len/2) in 
            let p2  = String.sub s (len/2) (len/2) in 
            (int_of_string p1) :: (int_of_string p2) :: (evolve q)
        end
    else
        (x*2024):: evolve q


let solution () = 
    let l = [773;79858;0;71;213357;2937;1;3998391] in
    List.iter (fun e->Printf.printf "%d " e) l;
    let rec iter i =
        if i == 0 then l
        else evolve (iter (i-1))
    in 
    let res = iter 25 in
    Printf.printf "\n";

    List.length res

let () =
    let sol2 = solution () in
    Printf.printf "Partie 2 : %d\n" sol2
