module namespace funcs = "com.funcs.catalog";

declare function funcs:top-movies() {
  <movies>{
  for $a in doc("/home/marciapires/Desktop/Universidade/4Ano/EDC/EDC_Project/webapp/files/movies.xml")//movie
  order by $a/vote_average/text()/xs:double(.) descending
  return (
    <movie>{
      $a/original_title,
      $a/poster_path,
      $a/popularity,
      $a/vote_average,
      for $c in $a/genres/item
      return $c/name
    }</movie>
  )[position() le 9]
  }</movies>
};
declare function funcs:top-series() {
  <series>{
  for $a in doc("/home/marciapires/Desktop/Universidade/4Ano/EDC/EDC_Project/webapp/files/series.xml")//serie
  order by $a/vote_average/text()/xs:double(.) descending
  return (
    <serie>{
      $a/original_name,
      $a/poster_path,
      $a/popularity,
      $a/vote_average,
      for $c in $a/genres/item
      return $c/name
    }</serie>
  )[position() le 9]
  }</series>
};
declare function funcs:get-mgenres() {
  <genres>{
  let $a := doc("/home/marciapires/Desktop/Universidade/4Ano/EDC/EDC_Project/webapp/files/movies.xml")//movie
  for $b in distinct-values($a/genres/item/name)
  order by $b
  return <genre>{$b}</genre>
  }</genres>
};
declare function funcs:get-sgenres() {
  <genres>{
  let $a := doc("C:/Users/JacintoLuf/Desktop/ua/ano4/edc/projeto/EDC_Project/webapp/files/series.xml")//serie
  for $b in distinct-values($a/genres/item/name)
  return <genre>{$b}</genre>
  }</genres>
};
declare function funcs:get-genre-movies($g) {
  <movies>{
  for $a in doc("C:/Users/JacintoLuf/Desktop/ua/ano4/edc/projeto/EDC_Project/webapp/files/movies.xml")//movie
  where $a/genres/item/name = $g
  return (
    <movie>{
      $a/original_title,
      $a/backdrop_path,
      $a/popularity,
      $a/vote_average
    }</movie>
  )
  }</movies>
};
declare function funcs:get-genre-series($g) {
  <series>{
  for $a in doc("C:/Users/JacintoLuf/Desktop/ua/ano4/edc/projeto/EDC_Project/webapp/files/series.xml")//serie
  where $a/genres/item/name = $g
  return (
    <serie>{
      $a/original_title,
      $a/backdrop_path,
      $a/popularity,
      $a/vote_average
    }</serie>
  )
  }</series>
};

declare updating function funcs:insert-review() {
  
};
declare updating function funcs:delete-review() {
  
};
declare updating function funcs:update-review() {
  
};
