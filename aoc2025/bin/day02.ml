let is_invalid_id n =
  let s = string_of_int n in
  let len = String.length s in
  if len mod 2 = 1 then
    false
  else
    let half = len / 2 in
    let left = String.sub s 0 half in
    let right = String.sub s half half in
    left = right

let sum_invalid_in_range is_invalid a b =
  let rec loop acc n =
    if n > b then
      acc
    else
      let acc' = if is_invalid n then acc + n else acc in
      loop acc' (n + 1)
  in
  loop 0 a

let parse_one_range s =
  let s = String.trim s in
  if s = "" then
    None
  else
    match String.split_on_char '-' s with
    | [a_str; b_str] ->
        let a = int_of_string a_str in
        let b = int_of_string b_str in
        Some (a, b)
    | _ ->
        failwith ("Bad range: " ^ s)

let parse_ranges line =
  line
  |> String.split_on_char ','
  |> List.filter_map parse_one_range

let part1 input =
  let line = String.trim input in
  let ranges = parse_ranges line in
  let total =
    List.fold_left
      (fun acc (a, b) -> acc + sum_invalid_in_range is_invalid_id a b)
      0
      ranges
  in
  string_of_int total

let is_repeated s =
  let len = String.length s in
  (* try all possible chunk lengths d from 1 to len/2 *)
  let rec try_d d =
    if d > len / 2 then
      false
    else if len mod d <> 0 then
      (* d doesn't divide len, skip *)
      try_d (d + 1)
    else
      (* len = d * k, with k >= 2 because d <= len/2 *)
      let chunk = String.sub s 0 d in
      (* check if repeating chunk (len/d) times gives s *)
      let rec check i =
        if i >= len then
          true
        else if String.sub s i d <> chunk then
          false
        else
          check (i + d)
      in
      if check d then
        true
      else
        try_d (d + 1)
  in
  try_d 1

let is_invalid_id_2 n =
  let s = string_of_int n in
  is_repeated s

let part2 input =
  let line = String.trim input in
  let ranges = parse_ranges line in
  let total =
    List.fold_left
      (fun acc (a, b) -> acc + sum_invalid_in_range is_invalid_id_2 a b)
      0
      ranges
  in
  string_of_int total


let solve level input =
  match level with
  | 1 -> part1 input
  | 2 -> part2 input
  | _ -> failwith "Unknown part"

let read_all_stdin () =
  let buf = Buffer.create 1024 in
  (try
     while true do
       Buffer.add_string buf (input_line stdin);
       Buffer.add_char buf '\n'
     done
   with End_of_file -> ());
  Buffer.contents buf

let () =
  if Array.length Sys.argv < 2 then
    failwith "Usage: dayXX <level>";
  let level = int_of_string Sys.argv.(1) in
  let input = read_all_stdin () in
  solve level input |> print_endline
