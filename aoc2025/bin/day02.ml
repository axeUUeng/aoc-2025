let part1 input =
  (* TODO: implement part 1 *)
  String.length input |> string_of_int

let part2 input =
  (* TODO: implement part 2 *)
  (String.length input * 2) |> string_of_int

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
