(* bin/day03.ml *)
let digit_of_char c =
  (Char.code c) - (Char.code '0')

let best_for_line (s : string) : int =
  let len = String.length s in
  let rec loop idx max_tens_opt best =
    if idx >= len then
      best
    else
      let d = digit_of_char s.[idx] in
      match max_tens_opt with
      | None ->
          loop (idx + 1) (Some d) best
      | Some max_tens ->
          let candidate = 10 * max_tens + d in
          let best' = if candidate > best then candidate else best in
          let max_tens' = if d > max_tens then d else max_tens in
          loop (idx + 1) (Some max_tens') best'
  in
  loop 0 None 0

let part1 input =
  let lines =
    input
    |> String.split_on_char '\n'
    |> List.map String.trim
    |> List.filter (fun s -> s <> "")
  in
  let total =
    List.fold_left
      (fun acc line -> acc + best_for_line line)
      0
      lines
  in
  string_of_int total

let best_k_for_line (s : string) (k : int) : string =
  let n = String.length s in
  if n < k then failwith "bank too short for requested k" else
  let buf = Bytes.create k in
  let rec choose pos idx =
    if idx = k then
      Bytes.to_string buf
    else
      let remaining = k - idx in
      let max_start = n - remaining in
      let best_pos = ref pos in
      let best_char = ref s.[pos] in
      for i = pos + 1 to max_start do
        let c = s.[i] in
        if c > !best_char then begin
          best_char := c;
          best_pos := i
        end
      done;
      Bytes.set buf idx !best_char;
      choose (!best_pos + 1) (idx + 1)
  in
  choose 0 0

let best12_for_line s =
  best_k_for_line s 12

let part2 input =
  let lines =
    input
    |> String.split_on_char '\n'
    |> List.map String.trim
    |> List.filter (fun s -> s <> "")
  in
  let total =
    List.fold_left
      (fun acc line ->
         let best_str = best12_for_line line in
         let value = int_of_string best_str in
         acc + value)
      0
      lines
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
    failwith "Usage: day03 <level>";
  let level = int_of_string Sys.argv.(1) in
  let input = read_all_stdin () in
  solve level input |> print_endline
