module namespace funcs = "com.funcs.catalog";

declare function funcs:top-movies() {
  <movies>{
  for $a in doc("/home/tomasfilipe7/Desktop/Universidade/EDC/Project/webapp/files/movies.xml")//movie
  order by $a/vote_average/text()/xs:double(.) descending
  return (
    <movie>{
      $a/original_title,
      $a/poster_path,
      $a/popularity,
      $a/vote_average,
      $a/id,
      for $c in $a/genres/item
      return $c/name
    }</movie>
  )[position() le 9]
  }</movies>
};
declare function funcs:top-series() {
  <series>{
  for $a in doc("/home/tomasfilipe7/Desktop/Universidade/EDC/Project/webapp/files/series.xml")//serie
  order by $a/vote_average/text()/xs:double(.) descending
  return (
    <serie>{
      $a/original_name,
      $a/poster_path,
      $a/popularity,
      $a/vote_average,
      $a/id,
      for $c in $a/genres/item
      return $c/name
    }</serie>
  )[position() le 9]
  }</series>
};
declare function funcs:get-mgenres() {
  <genres>{
  let $a := doc("/home/tomasfilipe7/Desktop/Universidade/EDC/Project/webapp/files/movies.xml")//movie
  for $b in distinct-values($a/genres/item/name)
  order by $b
  return <genre>{$b}</genre>
  }</genres>
};
declare function funcs:get-sgenres() {
  <genres>{
  let $a := doc("/home/tomasfilipe7/Desktop/Universidade/EDC/Project/webapp/files/series.xml")//serie
  for $b in distinct-values($a/genres/item/name)
  order by $b
  return <genre>{$b}</genre>
  }</genres>
};
declare function funcs:get-genre-movies($g) {
  <movies>{
  for $a in doc("/home/tomasfilipe7/Desktop/Universidade/EDC/Project/webapp/files/movies.xml")//movie
  where ((for $g_item in $g return $g_item = $a/genres/item/name) = true())
  return (
    <movie>{
      $a/original_title,
      $a/poster_path,
      $a/popularity,
      $a/vote_average
    }</movie>
  )
  }</movies>
};

declare function funcs:get-genre-series($g) {
  <series>{
  for $a in doc("/home/tomasfilipe7/Desktop/Universidade/EDC/Project/webapp/files/series.xml")//serie
  where ((for $g_item in $g return $g_item = $a/genres/item/name) = true())
  return (
    <serie>{
      $a/name,
      $a/poster_path,
      $a/popularity,
      $a/vote_average
    }</serie>
  )
  }</series>
};

declare function funcs:get-search-movies($s) {
   <movies>{
        for $m in doc("/home/tomasfilipe7/Desktop/Universidade/EDC/Project/webapp/files/movies.xml")//movie
        where contains(lower-case($m/original_title), lower-case($s))
        return $m
   }</movies>
};
declare function funcs:get-search-series($s) {
   <series>{
        for $m in doc("/home/tomasfilipe7/Desktop/Universidade/EDC/Project/webapp/files/series.xml")//serie
        where contains(lower-case($m/name), lower-case($s))
        return $m
   }</series>
};
declare function funcs:get-search-persons($s) {
   <items>{
        for $mid in doc("/home/tomasfilipe7/Desktop/Universidade/EDC/Project/webapp/files/casts.xml")//cast
        where $mid/cast/item/original_name = $s
        return (
        for $a in doc("/home/tomasfilipe7/Desktop/Universidade/EDC/Project/webapp/files/movies.xml")//movie
          where $a/id = $mid/id
          return $a
        ),
        for $mid in doc("/home/tomasfilipe7/Desktop/Universidade/EDC/Project/webapp/files/casts.xml")//cast
        where $mid/crew/item/original_name = $s
        return (
        for $a in doc("/home/tomasfilipe7/Desktop/Universidade/EDC/Project/webapp/files/movies.xml")//movie
          where $a/id = $mid/id
          return $a
        ),
        for $mid in doc("/home/tomasfilipe7/Desktop/Universidade/EDC/Project/webapp/files/scredits.xml")//cast
        where $mid/cast/item/original_name = $s
        return (
        for $a in doc("/home/tomasfilipe7/Desktop/Universidade/EDC/Project/webapp/files/series.xml")//serie
          where $a/id = $mid/id
          return $a
        ),
        for $mid in doc("/home/tomasfilipe7/Desktop/Universidade/EDC/Project/webapp/files/scredits.xml")//cast
        where $mid/crew/item/original_name = $s
        return (
        for $a in doc("/home/tomasfilipe7/Desktop/Universidade/EDC/Project/webapp/files/series.xml")//serie
          where $a/id = $mid/id
          return $a
        )
   }</items>
};

declare function funcs:get-all-series-ordered-genre($g, $i){
  if ($i = '1') then (
  for $a in funcs:get-genre-series($g)//serie
  order by $a/vote_average/text()/xs:double(.) descending
  return $a
  )
  else if ($i = '2') then (
  for $a in funcs:get-genre-series($g)//serie
  order by $a/popularity/text()/xs:double(.) descending
    return $a
  )
  else if ($i ='3') then (
  for $a in funcs:get-genre-series($g)//serie
  order by $a/name/text()/xs:string(.)
  return $a
  )
};
declare function funcs:get-all-movies-ordered-genre($g, $i){
  if ($i = '1') then (
  for $a in funcs:get-genre-movies($g)//movie
  order by $a/vote_average/text()/xs:double(.) descending
  return $a
  )
  else if ($i = '2') then (
  for $a in funcs:get-genre-movies($g)//movie
  order by $a/popularity/text()/xs:double(.) descending
    return $a
  )
  else if ($i ='3') then (
  for $a in funcs:get-genre-movies($g)//movie
  order by $a/original_title/text()/xs:string(.)
  return $a
  )
};
declare function funcs:get-all-movies-ordered($i){
  if ($i = '1') then (
  for $a in doc("/home/tomasfilipe7/Desktop/Universidade/EDC/Project/webapp/files/movies.xml")//movie
  order by $a/vote_average/text()/xs:double(.) descending
  return $a
  )
  else if ($i = '2') then (
  for $a in doc("/home/tomasfilipe7/Desktop/Universidade/EDC/Project/webapp/files/movies.xml")//movie
  order by $a/popularity/text()/xs:double(.) descending
    return $a
  )
  else if ($i ='3') then (
  for $a in doc("/home/tomasfilipe7/Desktop/Universidade/EDC/Project/webapp/files/movies.xml")//movie
  order by $a/original_title/text()/xs:string(.)
  return $a
  )
};

declare function funcs:get-all-series-ordered($i){
  if ($i = '1') then (
  for $a in doc("/home/tomasfilipe7/Desktop/Universidade/EDC/Project/webapp/files/series.xml")//serie
  order by $a/vote_average/text()/xs:double(.) descending
  return $a
  )
  else if ($i = '2') then (
  for $a in doc("/home/tomasfilipe7/Desktop/Universidade/EDC/Project/webapp/files/series.xml")//serie
  order by $a/popularity/text()/xs:double(.) descending
    return $a
  )
  else if ($i ='3') then (
  for $a in doc("/home/tomasfilipe7/Desktop/Universidade/EDC/Project/webapp/files/series.xml")//serie
  order by $a/name/text()/xs:string(.)
  return $a
  )
};
declare updating function funcs:insert-review() {

};
declare updating function funcs:delete-review() {

};

declare updating function funcs:update-review() {
  
};
