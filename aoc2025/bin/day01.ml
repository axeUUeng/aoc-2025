(* bin/day01.ml *)

let wrap100 x = 
  let r = x mod 100 in 
  if r < 0 then r + 100 else r

let step (pos, count) line =
  let len = String.length line in 
  if len = 0 then
    (* empty line*)
    (pos, count)
  else
    let dir = line.[0] in
    let n = int_of_string (String.sub line 1 (len - 1)) in
    let raw =
      match dir with
      | 'L' -> pos - n
      | 'R' -> pos + n
      | _ -> failwith "unexpected direction"
    in
    let new_pos = wrap100 raw in
    let new_count = if new_pos = 0 then count + 1 else count in
    (new_pos, new_count)

let process lines =
  let (_, count) = List.fold_left step (50, 0) lines in
  count

let part1 input =
  let lines =
    input
    |> String.split_on_char '\n'
    |> List.map String.trim
    |> List.filter (fun s -> s <> "")
  in
  let answer = process lines in
  string_of_int answer

let count_hits pos dir n =
  match dir with
  | 'R' ->
      (* a is the first step k (1..n) where (pos + k) mod 100 = 0, if it exists *)
      let a = (100 - (pos mod 100)) mod 100 in
      if a = 0 then
        (* Starting at 0: hit 0 every 100 steps *)
        n / 100
      else if n < a then
        (* We never reach the first zero position *)
        0
      else
        (* First hit at step a, then every 100 steps *)
        1 + (n - a) / 100
  | 'L' ->
      (* b is the first step k (1..n) where (pos - k) mod 100 = 0, if it exists *)
      let b = pos mod 100 in
      if b = 0 then
        (* Starting at 0: hit 0 every 100 steps going left as well *)
        n / 100
      else if n < b then
        (* We never reach 0 on this rotation *)
        0
      else
        (* First hit at step b, then every 100 steps *)
        1 + (n - b) / 100
  | _ -> 0


let step2 (pos, count) line =
  let line = String.trim line in
  if line = "" then (pos, count) else
  let dir = line.[0] in
  let len = String.length line in
  let n = int_of_string (String.sub line 1 (len - 1)) in
  let hits = count_hits pos dir n in
  let new_pos =
    match dir with
    | 'R' -> wrap100 (pos + n)
    | 'L' -> wrap100 (pos - n)
    | _ -> pos
  in

  (new_pos, count + hits)

let process2 lines =
  let (_, count) = List.fold_left step2 (50, 0) lines in
  count

let part2 input =
  let lines =
    input
    |> String.split_on_char '\n'
    |> List.map String.trim
    |> List.filter (fun s -> s <> "")
  in
  process2 lines |> string_of_int

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
    failwith "Usage: day01 <level>";
  let level = int_of_string Sys.argv.(1) in
  let input = read_all_stdin () in
  let answer = solve level input in
  print_endline answer
