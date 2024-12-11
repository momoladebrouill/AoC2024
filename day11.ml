let rec read_lines f =
  try
    let line = input_line f in
    line :: read_lines f
  with End_of_file -> []

let soc c s =
    let q = String.split_on_char c s in
    let q = List.filter (fun e -> e <> "") q in
    q

let h = Hashtbl.create 200     

let rec evolve_one (n,x) = 
    if n == 0 then 1 else
    if x == 0 then evolve_one_memo (n-1,1)
    else if String.length (string_of_int x) mod 2 == 0 then 
        begin
            let s = string_of_int x in
            let len = String.length s in
            let p1  = String.sub s 0 (len/2) in 
            let p2  = String.sub s (len/2) (len/2) in 
            evolve_one_memo (n-1,int_of_string p1) 
            + evolve_one_memo (n-1,int_of_string p2)
        end
    else
        evolve_one_memo (n-1,x*2024)

    and evolve_one_memo x =
    try 
        Hashtbl.find h x
    with Not_found -> 
        let y = evolve_one x in
        Hashtbl.add h x y;
        y

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

    let iter n l =
        let l = ref l in
        for i = 0 to n - 1 do
            l:= evolve !l
        done;
        !l
    in 
    Printf.printf "\n";
    List.fold_left (+) 0 (List.map (fun x -> evolve_one_memo (75,x)) l)

let () =
    let sol2 = solution () in
    Printf.printf "Partie 2 : %d\n" sol2
