  for $a in doc("files/movies.xml")//movie
  order by $a/vote_average/text()/xs:double(.) descending
  return (
    $a/original_title,
    $a/backdrop_path,
    $a/popularity,
    $a/vote_average,
    $a/release_date,
    $a/runtime,
    for $c in $a/genres/item
    return $c/name
)